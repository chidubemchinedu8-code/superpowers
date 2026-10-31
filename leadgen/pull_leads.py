#!/usr/bin/env python3
"""
pull_leads.py - Cuyahoga acquisition pull -> ranked, dial-ready lead list.

One command, no API key, standard library only:

    python3 leadgen/pull_leads.py

Writes leadgen/out/LEADS_cuyahoga.csv (39 columns), prints the weight table,
the funnel, the drop counts, the signal combos, the top 12 rows and 14
self-checks. Exits non-zero if any self-check FAILs.

Sources of truth used and verified live on 2026-10-31:
  base layer   https://gis.cuyahogacounty.gov/server/rest/services/
               CCFO/Parcel_Fabric_Taxparcels/FeatureServer/0
  field names  read from the layer's own metadata before any `where` is built
  channel hits preforeclosure 2967 + probate 1157 + lien_sold 357 = 4481
  comp universe 8469 sales in the 10 target ZIPs, last 12 months

Two hard constraints the data cannot give you (kept blank by design):
  CASE NUMBER  and  AUCTION DATE.  They are a manual lookup, one per lead.
  See `--print-lookup-paths`.

Modes:
  --source live     (default) hit the county endpoint
  --source fixture  run the same code on leadgen/fixtures/*.json - SYNTHETIC
                    data, never a lead list, never written to out/
  --selftest        prove all 14 checks can actually FAIL (see -h)
  --verify-endpoint probe field names and channel counts only, no pull
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone

# ---------------------------------------------------------------------------
# PART 1 - the ranking rule.  Weights are printed on every run.
# ---------------------------------------------------------------------------

WEIGHTS = [
    ("PRE-FORECLOSURE", "clock_preforeclosure", 40),
    ("PROBATE / HEIR", "clock_probate", 30),
    ("STACKING BONUS - 2 or more clocks", "stacking_bonus", 25),
    ("tax lien sold", "clock_lien_sold", 15),
    ("strong ZIP", "strong_zip", 10),
    ("owes $3,000 or more", "has_lien_over_3k", 8),
    ("out-of-state owner", "out_of_state_owner", 8),
    ("tax delinquent", "clock_delinquent", 5),
    ("ARV over $200,000", "arv_over_200k", 5),
]
W = {key: weight for _label, key, weight in WEIGHTS}

STRONG_ZIPS = {44102, 44109, 44128, 44110}
MIN_LIEN = 3000
ARV_FLOOR = 125_000
MIN_SQFT = 500
WHOLE_FEE = 10_000
# RealVenture buy box - CONFIRMED by the client 2026-10-31 (was ASSUMED).
BUY_BOX = {
    "arv_floor": 125_000,
    "contract_cap": 900_000,
    "ltv_cap": 0.70,
    "close_days": (21, 30),
    "types": ("SFR", "duplex", "multi-family"),
    "condition": "any",
    "financing": ("cash", "seller finance"),
    "verbal_agreement_is_enough_to_submit": True,
    "markets": {
        "Akron, OH": "HOTTEST - small-city pricing next to a major metro",
        "Atlanta, GA": "HOTTEST - institutional buyers active, fast at scale",
        "Birmingham, AL": "HOTTEST - low basis, strong rent ratios",
        "Cleveland, OH": "HOTTEST - low entry prices, heavy rental demand",
        "Columbus, OH": "HOTTEST - growing metro, deep landlord base",
        "Dayton, OH": "HOTTEST - affordable, strong rent-to-price ratios",
        "Decatur, IL": "HOTTEST - cheap basis, good first assignments",
        "Detroit, MI": "HOTTEST - heavy distress, wide spreads, rehab-heavy",
        "Indianapolis, IN": "HOTTEST - landlord-friendly, very deep buyer pool",
        "Jackson, MS": "HOTTEST - low basis, neighbourhood selection critical",
        "Kansas City, MO": "HOTTEST - steady cash-flow buyers",
        "Memphis, TN": "HOTTEST - turnkey rental capital, fast closers",
        "Peoria, IL": "HOTTEST - small market, low competition",
        "St Louis, MO": "HOTTEST - deep investor bench, neighbourhood matters",
        "Toledo, OH": "HOTTEST - cheap doors, steady cash flow",
    },
}
# This pull is Cuyahoga County only. Cleveland OH is in the box; the other 14
# markets are NOT pulled and must not be implied by this file.
PULL_MARKET = "Cleveland, OH"
MY_SIDE = WHOLE_FEE // 2
BUYER_PCT = 0.70
OFFER_LOW_PCT = 0.55
OFFER_HIGH_PCT = 0.60

# ---------------------------------------------------------------------------
# PART 2 - the data pull
# ---------------------------------------------------------------------------

BASE_LAYER = ("https://gis.cuyahogacounty.gov/server/rest/services/"
              "CCFO/Parcel_Fabric_Taxparcels/FeatureServer/0")
BASE_QUERY = BASE_LAYER + "/query"
TARGET_ZIPS = [44102, 44103, 44104, 44105, 44108, 44109, 44110, 44112,
               44127, 44128]

# Fields verified against the layer metadata (142 fields total).
F = {
    "owner": "parcel_owner",
    "addr": "par_addr_all",
    "pin": "parcelpin",
    "zip": "parcel_zip",              # double - cast with int()
    "sqft": "total_res_liv_area",
    "year": "max_age",                # this IS the year built, not an age
    "xfer": "last_transfer_date",     # epoch ms date field
    "price": "last_sales_amount",
    "lien": "grand_total_balance",
    "foreclosure": "foreclosure_flag",
    "cert_sold": "cert_sold_flag",
    "hood": "neighborhood_code",
    "style": "res_styles",
    "market": "tax_market_total",
    "mail_state": "mail_state",
    "pclass": "property_class",
}
REQUIRED_FIELDS = set(F.values())

CHANNEL_FIELDS = [F["pin"], F["addr"], F["zip"], F["owner"], F["mail_state"],
                  F["sqft"], F["year"], F["xfer"], F["price"], F["lien"],
                  F["hood"], F["style"], F["foreclosure"], F["cert_sold"],
                  F["pclass"]]
COMP_FIELDS = [F["pin"], F["zip"], F["sqft"], F["xfer"], F["price"],
               F["hood"], F["style"]]

ZIP_SQL = "(" + ",".join(str(z) for z in TARGET_ZIPS) + ")"


def channel_where(channel: str) -> str:
    head = f"{F['pclass']}='R' AND {F['zip']} IN {ZIP_SQL} AND "
    if channel == "preforeclosure":
        return head + f"{F['foreclosure']} = 1"
    if channel == "probate":
        # OWNER-NAME PROXY - not the probate docket. See README.
        return head + (
            f"({F['owner']} LIKE '%ESTATE%' OR {F['owner']} LIKE '%HEIR%' "
            f"OR {F['owner']} LIKE '%ET AL%' OR "
            f"{F['owner']} LIKE '%LIFE EST%')")
    if channel == "lien_sold":
        return head + f"{F['cert_sold']} = 1"
    if channel == "delinquent":
        return head + f"{F['lien']} >= {MIN_LIEN}"
    raise ValueError(channel)


DEFAULT_CHANNELS = ("preforeclosure", "probate", "lien_sold")


def comp_where(as_of: date) -> str:
    seen = as_of - timedelta(days=365)
    # DATE 'YYYY-MM-DD' - an epoch-ms number returns HTTP 400 on this layer.
    return (f"{F['pclass']}='R' AND {F['zip']} IN {ZIP_SQL} AND "
            f"{F['xfer']} >= DATE '{seen.isoformat()}'")


# ---------------------------------------------------------------------------
# Transport
# ---------------------------------------------------------------------------

class Arcrest:
    """Paged ArcGIS REST reader with a disk cache and honest failure."""

    def __init__(self, cache_dir: str | None, as_of: date, sleep: float = 0.15):
        self.cache_dir = cache_dir
        self.as_of = as_of
        self.sleep = sleep
        self.requests = 0
        if cache_dir:
            os.makedirs(cache_dir, exist_ok=True)

    def _url(self, where: str, out_fields, geometry: bool, offset: int) -> str:
        params = {
            "where": where,
            "outFields": ",".join(out_fields),
            "returnGeometry": "true" if geometry else "false",
            "f": "json",
            "resultOffset": str(offset),
            "resultRecordCount": "1000",
        }
        if geometry:
            params["returnCentroid"] = "true"
            params["outSR"] = "4326"
        return BASE_QUERY + "?" + urllib.parse.urlencode(params, safe="(),'%")

    def _get(self, url: str) -> dict:
        if self.cache_dir:
            path = os.path.join(
                self.cache_dir, hashlib.md5(url.encode()).hexdigest() + ".json")
            if os.path.exists(path):
                with open(path, encoding="utf-8") as fh:
                    return json.load(fh)
        last = None
        for attempt in range(4):
            try:
                req = urllib.request.Request(
                    url, headers={"User-Agent": "leadgen/1.0 (acquisition pull)"})
                with urllib.request.urlopen(req, timeout=90) as resp:
                    payload = json.loads(resp.read().decode("utf-8"))
                if isinstance(payload, dict) and "error" in payload:
                    raise RuntimeError(
                        f"ArcGIS error: {payload['error'].get('message')} "
                        f"for {url}")
                if self.cache_dir:
                    with open(path, "w", encoding="utf-8") as fh:
                        json.dump(payload, fh)
                self.requests += 1
                return payload
            except (urllib.error.URLError, TimeoutError, OSError,
                    json.JSONDecodeError, RuntimeError) as exc:
                last = exc
                time.sleep(1.5 * (attempt + 1))
        raise SystemExit(
            f"FAILED to fetch after 4 attempts: {url}\n  last error: {last}\n"
            "If this is an SSL/connection error, your network cannot reach "
            "gis.cuyahogacounty.gov. Run this script from a machine that can.")

    def count(self, where: str) -> int:
        url = (BASE_QUERY + "?" + urllib.parse.urlencode(
            {"where": where, "returnCountOnly": "true", "f": "json"},
            safe="(),'"))
        return int(self._get(url).get("count", 0))

    def features(self, where: str, out_fields, geometry: bool = True) -> list:
        out, offset = [], 0
        while True:
            url = self._url(where, out_fields, geometry, offset)
            payload = self._get(url)
            page = payload.get("features", []) or []
            out.extend(page)
            if len(page) < 1000:
                break
            offset += 1000
            time.sleep(self.sleep)
        return out

    def probe_fields(self) -> list:
        """PART 2 rule 4: read the real field names before writing a where."""
        payload = self._get(BASE_LAYER + "?f=json")
        return [f["name"] for f in payload.get("fields", [])]


# ---------------------------------------------------------------------------
# Geometry + statistics (PART 3)
# ---------------------------------------------------------------------------

RADIUS_LADDER = (0.25, 0.50, 0.75, 1.00, 1.25, 1.50)
RADIUS_CAP = 1.50
MIN_COMPS = 3
SQFT_BAND = 0.30
HAIRCUT = 0.88
MIN_COMP_SQFT = 400
MIN_COMP_PRICE = 20_000
PPSF_MIN, PPSF_MAX = 20.0, 300.0


def miles(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Equirectangular - accurate at this scale, no library."""
    dlat = (lat2 - lat1) * 69.0
    dlon = (lon2 - lon1) * 69.0 * math.cos(math.radians((lat1 + lat2) / 2.0))
    return math.hypot(dlat, dlon)


def percentile(values: list, q: float) -> float:
    """Linear interpolation, no library."""
    v = sorted(values)
    if not v:
        raise ValueError("percentile of empty list")
    if len(v) == 1:
        return float(v[0])
    pos = (len(v) - 1) * q
    lo = int(pos)
    hi = min(lo + 1, len(v) - 1)
    return v[lo] + (v[hi] - v[lo]) * (pos - lo)


# ---------------------------------------------------------------------------
# Row model
# ---------------------------------------------------------------------------

COLUMNS = [
    "PRIORITY", "SIGNALS STACKED", "CHANNELS", "CASE NUMBER", "AUCTION DATE",
    "OWNER", "ADDRESS", "ZIP", "OWNERSHIP STAGE", "WHY CONTACT",
    "ARV SCREEN", "ARV STATUS", "ARV BASIS", "COMPS N", "COMP RADIUS MI",
    "COMP NEIGHBOURHOOD", "SUBJECT NEIGHBOURHOOD", "COMP CONFIDENCE",
    "COMP SOURCE", "BUYER MAX (ceiling, 70%)", "OFFER LOW (55% ARV, no repairs)",
    "OFFER HIGH (60% ARV, no repairs)", "FRICTION (buyer max - offer high)",
    "WHOLE FEE", "RV SPLIT", "MY SIDE @50/50", "OFFER STATUS", "REPAIRS",
    "REPAIRS STATUS", "LIENS", "SQFT", "YEAR BUILT", "MAIL STATE",
    "NEXT ACTION", "CALL STATUS", "PHONE", "NOTES", "CALL DATE", "#",
]
assert len(COLUMNS) == 39, len(COLUMNS)

ARV_STATUS_PRICED = "PRELIMINARY - not an offer"
ARV_STATUS_NONE = "NO COMP DATA"
OFFER_STATUS_PRICED = ("CEILING ONLY - no known repairs, this is the max; "
                       "grading can only lower it")
OFFER_STATUS_NONE = "NO COMP DATA"
RV_SPLIT = "50/50 of the fee - CONFIRMED 2026-10-31"

ENTITY_TOKENS = ["LLC", "LTD", "INC", "HOLDINGS", "PROPERTIES", "CORP",
                 "GROUP", "INVESTMENTS", " LP", "L.P.", " CO.", "COMPANY"]
ENTITY_WORD_TOKENS = {"LLC", "LTD", "INC", "CORP", "GROUP"}

INSTITUTION_TOKENS = ["BANK", "MORTGAGE", "MTG", "LOAN", "SERVICING", "FEDERAL",
                      "FANNIE", "FREDDIE", "HUD", "SECRETARY OF", "SHERIFF",
                      "FORF", "US BANK", "WELLS", "CHASE", "CITI",
                      "STATE OF OHIO"]

# Tokens that must match a whole word. Substring matching here is how you
# drop VINCENT, LINCOLN and SPENCER as "INC"/"CORP" owners.
_WORD_RE = {t: re.compile(rf"(?<![A-Z]){re.escape(t)}(?![A-Z])")
            for t in ENTITY_WORD_TOKENS}


def is_entity_owner(owner: str, strict_substring: bool = False) -> bool:
    up = (owner or "").upper()
    if not up:
        return False
    for token in ENTITY_TOKENS:
        if strict_substring:
            if token in up:
                return True
            continue
        if token in ENTITY_WORD_TOKENS:
            if _WORD_RE[token].search(up):
                return True
        elif token in up:
            return True
    return False


def is_institution(owner: str) -> bool:
    up = (owner or "").upper()
    return any(t in up for t in INSTITUTION_TOKENS)


def ownership_stage(owner: str, xfer: date | None, as_of: date) -> str:
    if is_institution(owner):
        return "GONE - institution owns it"
    if xfer is not None and (as_of - xfer).days <= 180:
        return "CHECK - transferred recently"
    return "SELLER STILL OWNS"


def priority_of(channels: set, zip5: int | None, lien: float | None,
                mail_state: str, arv: float | None) -> tuple[int, int]:
    clocks = [c for c in ("preforeclosure", "probate", "lien_sold",
                          "delinquent") if c in channels]
    n_clocks = len(clocks)
    score = 0
    if "preforeclosure" in channels:
        score += W["clock_preforeclosure"]
    if "probate" in channels:
        score += W["clock_probate"]
    if n_clocks >= 2:
        score += W["stacking_bonus"]
    if "lien_sold" in channels:
        score += W["clock_lien_sold"]
    if zip5 in STRONG_ZIPS:
        score += W["strong_zip"]
    if lien is not None and lien >= MIN_LIEN:
        score += W["has_lien_over_3k"]
    if mail_state and mail_state.upper() != "OH":
        score += W["out_of_state_owner"]
    if "delinquent" in channels:
        score += W["clock_delinquent"]
    if arv is not None and arv > 200_000:
        score += W["arv_over_200k"]
    return score, n_clocks


def why_contact(channels: set, lien: float | None, mail_state: str,
                zip5: int | None, n_clocks: int) -> str:
    order = ["preforeclosure", "probate", "lien_sold", "delinquent"]
    names = {"preforeclosure": "pre-foreclosure", "probate": "probate/heir",
             "lien_sold": "tax lien sold", "delinquent": "tax delinquent"}
    parts = [names[c] for c in order if c in channels]
    out = " + ".join(parts)
    if n_clocks >= 2:
        out = f"{n_clocks} clocks: " + out
    if lien and lien >= MIN_LIEN:
        out += f"; owes ${lien:,.0f}"
    if mail_state and mail_state.upper() != "OH":
        out += f"; owner mails from {mail_state.upper()}"
    if zip5 in STRONG_ZIPS:
        out += "; strong ZIP"
    return out


def next_action(n_clocks: int, has_comps: bool) -> str:
    if n_clocks >= 2:
        head = ("CALL FIRST (stacked) - 6 condition questions + "
                "'has a sale date been set?'")
    else:
        head = ("Call - 6 condition questions + sale date, then request the "
                "5 photos")
    if not has_comps:
        head += "; NO COMPS - confirm value before quoting"
    return head


def economics(arv: float, repairs: float = 0.0) -> dict:
    """PART 5 - one model, two percentages. 70% is a CAP, 55-60% is a TARGET
    under the cap, and the gap IS the pay stack. Never deduct the fee twice."""
    buyer_max = int(round(BUYER_PCT * arv - repairs))
    offer_low = int(round(OFFER_LOW_PCT * arv - repairs))
    offer_high = int(round(OFFER_HIGH_PCT * arv - repairs))
    return {"BUYER_MAX": buyer_max, "OFFER_LOW": offer_low,
            "OFFER_HIGH": offer_high, "FRICTION": buyer_max - offer_high,
            "FRICTION_PCT_OF_ARV": (buyer_max - offer_high) / arv}


@dataclass
class Lead:
    key: str
    pin: str
    address: str
    zip5: int | None
    owner: str
    mail_state: str
    sqft: float | None
    year: int | None
    xfer: date | None
    lien: float | None
    subject_hood: str
    style: str
    lat: float | None
    lon: float | None
    channels: set = field(default_factory=set)
    arv: int | None = None
    as_is: int | None = None
    arv_basis: str = ""
    comps_n: int = 0
    comp_radius: float | None = None
    comp_hood: str = ""
    comp_conf: str = "NO COMPS"
    comp_source: str = ""
    comp_dates: list = field(default_factory=list)
    comp_hoods: list = field(default_factory=list)
    priority: int = 0
    n_clocks: int = 0

    def economy(self) -> dict:
        if self.arv is None:
            return {"BUYER MAX (ceiling, 70%)": "", "OFFER LOW (55% ARV, no repairs)": "",
                    "OFFER HIGH (60% ARV, no repairs)": "",
                    "FRICTION (buyer max - offer high)": "",
                    "OFFER STATUS": OFFER_STATUS_NONE,
                    "ARV STATUS": ARV_STATUS_NONE}
        eco = economics(self.arv)
        return {
            "BUYER MAX (ceiling, 70%)": eco["BUYER_MAX"],
            "OFFER LOW (55% ARV, no repairs)": eco["OFFER_LOW"],
            "OFFER HIGH (60% ARV, no repairs)": eco["OFFER_HIGH"],
            "FRICTION (buyer max - offer high)": eco["FRICTION"],
            "OFFER STATUS": OFFER_STATUS_PRICED,
            "ARV STATUS": ARV_STATUS_PRICED,
        }

    def to_row(self) -> dict:
        eco = self.economy()
        row = {
            "PRIORITY": self.priority,
            "SIGNALS STACKED": self.n_clocks,
            "CHANNELS": "+".join(
                c for c in ("preforeclosure", "probate", "lien_sold",
                            "delinquent") if c in self.channels),
            "CASE NUMBER": "",          # manual lookup, one per lead
            "AUCTION DATE": "",         # manual lookup, one per lead
            "OWNER": self.owner,
            "ADDRESS": self.address,
            "ZIP": self.zip5 or "",
            "OWNERSHIP STAGE": "SELLER STILL OWNS",
            "WHY CONTACT": why_contact(self.channels, self.lien,
                                       self.mail_state, self.zip5,
                                       self.n_clocks),
            "ARV SCREEN": self.arv if self.arv is not None else "",
            "ARV STATUS": eco["ARV STATUS"],
            "ARV BASIS": self.arv_basis,
            "COMPS N": self.comps_n if self.comps_n else "",
            "COMP RADIUS MI": self.comp_radius if self.comp_radius is not None else "",
            "COMP NEIGHBOURHOOD": self.comp_hood,
            "SUBJECT NEIGHBOURHOOD": self.subject_hood,
            "COMP CONFIDENCE": self.comp_conf,
            "COMP SOURCE": self.comp_source,
            "BUYER MAX (ceiling, 70%)": eco["BUYER MAX (ceiling, 70%)"],
            "OFFER LOW (55% ARV, no repairs)": eco["OFFER LOW (55% ARV, no repairs)"],
            "OFFER HIGH (60% ARV, no repairs)": eco["OFFER HIGH (60% ARV, no repairs)"],
            "FRICTION (buyer max - offer high)": eco["FRICTION (buyer max - offer high)"],
            "WHOLE FEE": WHOLE_FEE,
            "RV SPLIT": RV_SPLIT,
            "MY SIDE @50/50": MY_SIDE,
            "OFFER STATUS": eco["OFFER STATUS"],
            "REPAIRS": "",              # never quoted without a grade
            "REPAIRS STATUS": "UNGRADED",
            "LIENS": int(self.lien) if self.lien is not None else "",
            "SQFT": int(self.sqft) if self.sqft else "",
            "YEAR BUILT": self.year or "",
            "MAIL STATE": self.mail_state or "",
            "NEXT ACTION": next_action(self.n_clocks, self.comps_n >= MIN_COMPS),
            "CALL STATUS": "new",
            "PHONE": "",
            "NOTES": "",
            "CALL DATE": "",
            "#": 0,                     # filled after sorting
        }
        # Hidden fields, for checks only - never written to CSV.
        row["_pin"] = self.pin
        row["_key"] = self.key
        row["_comp_dates"] = list(self.comp_dates)
        row["_owner"] = self.owner
        return row


# ---------------------------------------------------------------------------
# Pull -> merge -> gates -> ARV -> rank
# ---------------------------------------------------------------------------

def parse_date_ms(value) -> date | None:
    if value in (None, ""):
        return None
    try:
        return datetime.fromtimestamp(float(value) / 1000.0, tz=timezone.utc).date()
    except (TypeError, ValueError, OverflowError, OSError):
        return None


def parse_zip(value) -> int | None:
    if value in (None, ""):
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def num(value) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def norm_style(value) -> str:
    up = (value or "").upper().strip()
    return up.split()[0].split(",")[0] if up else ""


def merge_channels(per_channel: dict) -> tuple[dict, int, int]:
    """One row per property. Merge key: parcelpin, else address+ZIP."""
    merged, distinct_keys = {}, set()
    for channel, features in per_channel.items():
        seen = set()
        for feat in features:
            a = feat.get("attributes", feat)
            pin = (a.get(F["pin"]) or "").strip().upper()
            addr = (a.get(F["addr"]) or "").strip().upper()
            zip5 = parse_zip(a.get(F["zip"]))
            key = pin or (f"{addr}|{zip5}" if addr else "")
            if not key:
                continue
            distinct_keys.add(key)
            if (key, channel) in seen:      # same parcel twice in one channel
                continue
            seen.add((key, channel))
            rec = merged.get(key)
            if rec is None:
                rec = merged[key] = {
                    "key": key, "attributes": a, "channels": set(),
                    "centroid": feat.get("centroid") or
                                a.get("centroid") or {}}
            rec["channels"].add(channel)
    return merged, len(distinct_keys), sum(len(v) for v in per_channel.values())


def build_comps(features: list, as_of: date) -> tuple[list, dict]:
    """Screen the comp universe once; index by neighbourhood code."""
    cutoff = as_of - timedelta(days=365)
    usable, dropped = [], {"sqft_or_price": 0, "price_floor": 0,
                           "ppsf": 0, "geometry": 0, "window": 0}
    by_hood: dict[str, list] = {}
    for feat in features:
        a = feat.get("attributes", feat)
        sqft = num(a.get(F["sqft"]))
        price = num(a.get(F["price"]))
        sold = parse_date_ms(a.get(F["xfer"]))
        c = feat.get("centroid") or {}
        lat, lon = c.get("y"), c.get("x")
        if lat is None or lon is None:
            dropped["geometry"] += 1
            continue
        if not sqft or sqft < MIN_COMP_SQFT or not price:
            dropped["sqft_or_price"] += 1
            continue
        if price < MIN_COMP_PRICE:
            dropped["price_floor"] += 1
            continue
        ppsf = price / sqft
        if ppsf < PPSF_MIN or ppsf > PPSF_MAX:
            dropped["ppsf"] += 1
            continue
        if sold is None or sold < cutoff:
            dropped["window"] += 1
            continue
        comp = {"pin": (a.get(F["pin"]) or "").strip().upper(),
                "hood": (a.get(F["hood"]) or "").strip().upper(),
                "style": norm_style(a.get(F["style"])),
                "sqft": sqft, "price": price, "sold": sold,
                "lat": float(lat), "lon": float(lon)}
        usable.append(comp)
        by_hood.setdefault(comp["hood"], []).append(comp)
    return usable, by_hood | {"_dropped": dropped}


def arv_for(lead: Lead, comps_by_hood: dict, as_of: date) -> None:
    """Neighbourhood -> style -> sqft band -> smallest radius with >= 3."""
    pool = [c for c in comps_by_hood.get(lead.subject_hood.upper(), [])
            if c["pin"] != (lead.pin or "").strip().upper()]
    if not pool or not lead.sqft or lead.lat is None:
        return
    band = [c for c in pool
            if abs(c["sqft"] - lead.sqft) / lead.sqft <= SQFT_BAND]
    if not band:
        return
    for radius in RADIUS_LADDER:
        hits = [c for c in band
                if miles(lead.lat, lead.lon, c["lat"], c["lon"]) <= radius]
        if len(hits) < MIN_COMPS:
            continue
        styled = [c for c in hits if c["style"] and c["style"] == lead.style]
        chosen = styled if len(styled) >= MIN_COMPS else hits
        ppsf = [c["price"] / c["sqft"] for c in chosen]
        p75 = percentile(ppsf, 0.75)
        p25 = percentile(ppsf, 0.25)
        lead.arv = int(round(lead.sqft * p75 * HAIRCUT))
        lead.as_is = int(round(lead.sqft * p25 * HAIRCUT))
        lead.comps_n = len(chosen)
        lead.comp_radius = radius
        lead.comp_hood = lead.subject_hood
        lead.comp_conf = "HIGH" if len(chosen) >= 6 else "LOW"
        lead.comp_source = "RADIUS"
        lead.comp_dates = [c["sold"] for c in chosen]
        lead.comp_hoods = [c["hood"] for c in chosen]
        lead.arv_basis = (f"{int(lead.sqft)}sqft x ${p75:,.0f}/sqft p75, "
                          f"n={len(chosen)}, {lead.subject_hood}")
        return
    # under 3 comps at every radius -> NO ARV. Do not widen, do not average.


def run_pipeline(source: str, as_of: date, channels: tuple, strict_entities: bool,
                 cache_dir: str | None) -> tuple[list, dict]:
    per_channel, comp_features = {}, []
    if source == "live":
        api = Arcrest(cache_dir, as_of)
        print(f"[probe] {BASE_LAYER}?f=json")
        fields = api.probe_fields()
        missing = REQUIRED_FIELDS - set(fields)
        if missing:
            raise SystemExit(f"FAILED field probe - missing {sorted(missing)}. "
                             f"The layer changed; fix F before querying.")
        print(f"[probe] {len(fields)} fields, all {len(REQUIRED_FIELDS)} "
              f"required names present")
        for channel in channels:
            where = channel_where(channel)
            print(f"[pull ] {channel}: where={where}")
            per_channel[channel] = api.features(where, CHANNEL_FIELDS)
            print(f"        -> {len(per_channel[channel])} features")
        cwhere = comp_where(as_of)
        print(f"[pull ] comp universe: where={cwhere}")
        comp_features = api.features(cwhere, COMP_FIELDS)
        print(f"        -> {len(comp_features)} raw sales")
    else:
        path = source
        with open(path, encoding="utf-8") as fh:
            fixture = json.load(fh)
        print("!" * 78)
        print("! SYNTHETIC FIXTURE - every row below is fabricated test data.")
        print("! This is a machinery test, NOT a lead list. Do not dial it.")
        print("!" * 78)
        layers = fixture["layers"]
        for channel in channels:
            per_channel[channel] = layers.get(channel, [])
        comp_features = layers.get("comps", [])
        as_of = date.fromisoformat(fixture["meta"]["as_of"])

    merged, distinct_before, raw_hits = merge_channels(per_channel)
    print(f"\n[merge] merged {raw_hits} channel hits -> "
          f"{len(merged)} distinct properties")

    usable_comps, comps_by_hood = build_comps(comp_features, as_of)
    dropped = comps_by_hood.pop("_dropped")
    print(f"[comps] {len(comp_features)} raw sales -> {len(usable_comps)} "
          f"usable comps  (dropped: {dropped})")

    drops = {"entity": 0, "no_living_area": 0, "under_arv_floor": 0,
             "institution": 0, "recent_transfer": 0}
    leads: list[Lead] = []
    for rec in merged.values():
        a = rec["attributes"]
        owner = (a.get(F["owner"]) or "").strip()
        if is_entity_owner(owner, strict_entities):
            drops["entity"] += 1
            continue
        sqft = num(a.get(F["sqft"]))
        if not sqft or sqft < MIN_SQFT:
            drops["no_living_area"] += 1
            continue
        c = rec.get("centroid") or a.get("centroid") or {}
        lead = Lead(
            key=rec["key"], pin=(a.get(F["pin"]) or "").strip(),
            address=(a.get(F["addr"]) or "").strip(),
            zip5=parse_zip(a.get(F["zip"])), owner=owner,
            mail_state=(a.get(F["mail_state"]) or "").strip().upper(),
            sqft=sqft, year=int(num(a.get(F["year"])) or 0) or None,
            xfer=parse_date_ms(a.get(F["xfer"])),
            lien=num(a.get(F["lien"])),
            subject_hood=(a.get(F["hood"]) or "").strip().upper(),
            style=norm_style(a.get(F["style"])),
            lat=c.get("y"), lon=c.get("x"), channels=set(rec["channels"]),
        )
        # Gate order per the spec: entity -> no living area -> ownership
        # stage -> ARV floor. Ordering only affects which bucket a drop is
        # reported in, never which rows survive.
        stage = ownership_stage(owner, lead.xfer, as_of)
        if stage.startswith("GONE"):
            drops["institution"] += 1
            continue
        if stage.startswith("CHECK"):
            drops["recent_transfer"] += 1
            continue
        arv_for(lead, comps_by_hood, as_of)
        if lead.arv is not None and lead.arv < ARV_FLOOR:
            drops["under_arv_floor"] += 1
            continue
        lead.priority, lead.n_clocks = priority_of(
            lead.channels, lead.zip5, lead.lien, lead.mail_state, lead.arv)
        leads.append(lead)

    # Sort: PRIORITY desc, then ARV screen desc; a blank ARV sorts last
    # inside its band, never to the top.
    leads.sort(key=lambda l: (-l.priority,
                              -(l.arv if l.arv is not None else -1)))
    rows = [lead.to_row() for lead in leads]
    for i, row in enumerate(rows, start=1):
        row["#"] = i

    ctx = {"raw_hits": raw_hits, "merged": len(merged),
           "no_comps": sum(1 for r in rows if not isinstance(r["COMPS N"], int)),
           "distinct_before": distinct_before, "kept": len(rows),
           "drops": drops, "comps_raw": len(comp_features),
           "comps_usable": len(usable_comps), "as_of": as_of,
           "comp_drop_detail": dropped}
    return rows, ctx


# ---------------------------------------------------------------------------
# PART 6 - the 14 self-checks.  Each compares two independent things, and
# each is proven to FAIL under --selftest when the thing it guards is broken.
# ---------------------------------------------------------------------------

REPAIR_STATUSES = {"UNGRADED", "EXTERIOR ONLY - needs interior", "GRADED",
                   "SELLER-REPORTED - not verified"}
TERMINAL_INSTITUTION_OK = ("SELLER STILL OWNS",)


def _int(v):
    return v if isinstance(v, int) else None


def check_1_no_institutions(rows, ctx):
    bad = [r["#"] for r in rows if is_institution(r["OWNER"])]
    return (not bad), f"{len(bad)} institution-owned rows" + (
        f" at #{bad[:5]}" if bad else "")


def check_2_no_entities(rows, ctx):
    bad = [r["#"] for r in rows if is_entity_owner(r["OWNER"])]
    return (not bad), f"{len(bad)} entity/LLC owners" + (
        f" at #{bad[:5]}" if bad else "")


def check_3_arv_floor(rows, ctx):
    bad = [r["#"] for r in rows
           if isinstance(r["ARV SCREEN"], int) and r["ARV SCREEN"] < ARV_FLOOR]
    return (not bad), f"{len(bad)} rows under ${ARV_FLOOR:,}" + (
        f" at #{bad[:5]}" if bad else "")


def check_4_no_unearned_repairs(rows, ctx):
    bad = []
    for r in rows:
        repairs = r["REPAIRS"]
        if repairs not in ("", None) and r["REPAIRS STATUS"] not in (
                "GRADED", "SELLER-REPORTED - not verified"):
            bad.append(r["#"])
        if r["REPAIRS STATUS"] not in REPAIR_STATUSES:
            bad.append(r["#"])
    return (not bad), f"{len(bad)} rows quote repairs without a grade"


def check_5_sorted(rows, ctx):
    bad = [rows[i + 1]["#"] for i in range(len(rows) - 1)
           if rows[i]["PRIORITY"] < rows[i + 1]["PRIORITY"]]
    # blank ARV must not outrank a priced row inside the same band
    bad += [rows[i + 1]["#"] for i in range(len(rows) - 1)
            if rows[i]["PRIORITY"] == rows[i + 1]["PRIORITY"]
            and rows[i]["ARV SCREEN"] == ""
            and rows[i + 1]["ARV SCREEN"] != ""]
    return (not bad), f"{len(bad)} ordering violations"


def check_6_buyer_cap(rows, ctx):
    bad = [r["#"] for r in rows
           if isinstance(r["ARV SCREEN"], int)
           and isinstance(r["BUYER MAX (ceiling, 70%)"], int)
           and r["BUYER MAX (ceiling, 70%)"] > BUYER_PCT * r["ARV SCREEN"] + 0.5]
    return (not bad), f"{len(bad)} rows where buyer max exceeds 70% of ARV"


def check_7_offer_under_cap(rows, ctx):
    bad = [r["#"] for r in rows
           if isinstance(r["OFFER HIGH (60% ARV, no repairs)"], int)
           and isinstance(r["BUYER MAX (ceiling, 70%)"], int)
           and r["OFFER HIGH (60% ARV, no repairs)"] > r["BUYER MAX (ceiling, 70%)"]]
    bad += [r["#"] for r in rows
            if isinstance(r["OFFER LOW (55% ARV, no repairs)"], int)
            and isinstance(r["OFFER HIGH (60% ARV, no repairs)"], int)
            and r["OFFER LOW (55% ARV, no repairs)"] > r["OFFER HIGH (60% ARV, no repairs)"]]
    return (not bad), f"{len(bad)} rows where an offer exceeds buyer max"


def check_8_no_duplicates(rows, ctx):
    seen, bad = set(), []
    for r in rows:
        k = r["_key"]
        if k in seen:
            bad.append(r["#"])
        seen.add(k)
    return (not bad), f"{len(bad)} duplicate properties"


def check_9_merge_integrity(rows, ctx):
    ok = ctx["merged"] == ctx["distinct_before"]
    return ok, (f"merged {ctx['merged']} vs distinct parcels before filtering "
                f"{ctx['distinct_before']}")


def check_10_same_neighbourhood(rows, ctx):
    bad = [r["#"] for r in rows
           if isinstance(r["COMPS N"], int) and r["COMPS N"] >= MIN_COMPS
           and str(r["COMP NEIGHBOURHOOD"]).strip().upper()
           != str(r["SUBJECT NEIGHBOURHOOD"]).strip().upper()]
    priced_no_hood = [r["#"] for r in rows
                      if isinstance(r["ARV SCREEN"], int)
                      and not str(r["COMP NEIGHBOURHOOD"]).strip()]
    bad += priced_no_hood
    return (not bad), (f"{len(bad)} priced rows used comps outside the "
                       f"subject's own neighbourhood")


def check_11_radius_cap(rows, ctx):
    bad = [r["#"] for r in rows
           if isinstance(r["COMP RADIUS MI"], (int, float))
           and r["COMP RADIUS MI"] > RADIUS_CAP + 1e-9]
    return (not bad), f"{len(bad)} comp radii exceed {RADIUS_CAP} mi"


def check_12_min_comps(rows, ctx):
    bad = [r["#"] for r in rows
           if isinstance(r["COMPS N"], int) and r["COMPS N"] < MIN_COMPS]
    return (not bad), f"{len(bad)} comp sets smaller than {MIN_COMPS}"


def check_13_window(rows, ctx):
    cutoff = ctx["as_of"] - timedelta(days=365)
    bad = []
    for r in rows:
        for sold in r.get("_comp_dates", []):
            if sold < cutoff:
                bad.append(r["#"])
                break
    return (not bad), (f"{len(bad)} rows used a sale older than "
                       f"{cutoff.isoformat()}")


def check_14_no_invented_arv(rows, ctx):
    bad = [r["#"] for r in rows
           if not isinstance(r["COMPS N"], int)
           and (isinstance(r["ARV SCREEN"], int) or r["ARV BASIS"]
                or r["COMP CONFIDENCE"] != "NO COMPS")]
    return (not bad), f"{len(bad)} unpriced rows carry an invented ARV"


CHECKS = [
    ("no institution-owned rows", check_1_no_institutions),
    ("no entity/LLC owners", check_2_no_entities),
    ("every row clears the ARV floor", check_3_arv_floor),
    ("no repairs quoted without a grade", check_4_no_unearned_repairs),
    ("sorted by priority descending", check_5_sorted),
    ("buyer max never exceeds 70% of ARV", check_6_buyer_cap),
    ("offer never exceeds buyer max", check_7_offer_under_cap),
    ("no duplicate properties in output", check_8_no_duplicates),
    ("merged count == distinct parcels before filtering",
     check_9_merge_integrity),
    ("every priced row used comps from the subject's own neighbourhood",
     check_10_same_neighbourhood),
    ("no comp radius exceeds 1.5 miles", check_11_radius_cap),
    ("no comp set smaller than 3 sales", check_12_min_comps),
    ("every comp sale is inside the 12-month window", check_13_window),
    ("unpriced rows carry no invented ARV", check_14_no_invented_arv),
]


def run_checks(rows, ctx) -> list[tuple[str, bool, str]]:
    out = []
    for name, fn in CHECKS:
        try:
            ok, detail = fn(rows, ctx)
        except Exception as exc:                     # a crash is a FAIL
            ok, detail = False, f"check raised {type(exc).__name__}: {exc}"
        out.append((name, ok, detail))
    return out


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def print_weight_table():
    print("\nRANKING WEIGHTS (priority = sum of clock weights + stacking "
          "+ modifiers)")
    for label, key, weight in WEIGHTS:
        print(f"  +{weight:<4} {label:<38} {key}")
    print("  PRE-FORECLOSURE + PROBATE = 95 beats PRE-FORECLOSURE ALONE = 40")
    print("  PROBATE ALONE = 30 beats lien-sold 15 and delinquency 5")
    print("  strong_zips = 44102, 44109, 44128, 44110; "
          "n_clocks counts channels only")


def print_funnel(ctx):
    d = ctx["drops"]
    print("\nFUNNEL")
    print(f"  {ctx['raw_hits']:,} channel hits -> {ctx['merged']:,} distinct "
          f"properties -> {ctx['kept']:,} kept")
    print(f"  drops: entity {d['entity']:,} | no living area "
          f"{d['no_living_area']:,} | under ARV floor {d['under_arv_floor']:,} "
          f"| institution {d['institution']:,} | recent transfer "
          f"{d['recent_transfer']:,}")
    no_comps = ctx.get("no_comps", 0)
    print(f"  no comps: {no_comps:,} kept and priced blank (still callable)")
    print(f"  comps: {ctx['comps_raw']:,} raw sales -> "
          f"{ctx['comps_usable']:,} usable")


def print_signal_combos(rows):
    from collections import Counter
    combos = Counter(r["CHANNELS"] for r in rows)
    stacked = sum(1 for r in rows if (r["SIGNALS STACKED"] or 0) >= 2)
    print("\nSIGNAL COMBOS")
    for combo, n in combos.most_common():
        print(f"  {n:>4}  {combo}")
    print(f"  stacked (2+ clocks): {stacked}")
    conf = Counter(r["COMP CONFIDENCE"] for r in rows)
    print("  comp confidence: " + " / ".join(
        f"{conf.get(k, 0)} {k}" for k in ("HIGH", "LOW", "NO COMPS")))
    radii = [r["COMP RADIUS MI"] for r in rows
             if isinstance(r["COMP RADIUS MI"], (int, float))]
    if radii:
        print(f"  comp radius: median {percentile(radii, 0.5):.2f} mi, "
              f"max {max(radii):.2f} mi")


def print_top(rows, n=12):
    print(f"\nTOP {n} (PRIORITY desc, then ARV desc)")
    hdr = (f"{'#':>3} {'PRI':>4} {'STK':>3} {'CHANNELS':<26} {'ARV':>9} "
           f"{'OFFER HI':>9} {'SQFT':>5}  ADDRESS")
    print(hdr)
    print("-" * len(hdr))
    for r in rows[:n]:
        arv = r["ARV SCREEN"]
        high = r["OFFER HIGH (60% ARV, no repairs)"]
        arv_s = f"${arv:,}" if isinstance(arv, int) else "NO COMPS"
        high_s = f"${high:,}" if isinstance(high, int) else "-"
        print(f"{r['#']:>3} {r['PRIORITY']:>4} {str(r['SIGNALS STACKED']):>3} "
              f"{r['CHANNELS']:<26} {arv_s:>9} {high_s:>9} "
              f"{str(r['SQFT']):>5}  {r['ADDRESS']}")
    if rows:
        top = rows[0]
        print(f"\ntop row: {top['CHANNELS']} = priority {top['PRIORITY']}")


def print_checks(results) -> bool:
    print("\nSELF-CHECKS")
    ok_all = True
    for i, (name, ok, detail) in enumerate(results, start=1):
        ok_all &= ok
        print(f"  {i:>2} {'PASS' if ok else 'FAIL'}  {name:<62} {detail}")
    print(f"\n{sum(1 for r in results if r[1])}/{len(results)} "
          f"{'PASS' if ok_all else 'FAIL'}")
    return ok_all


def print_buybox(rows):
    """Fit against the CONFIRMED buy box. This is a report, not a gate: the
    box tells you which deals RV can take, not which sellers to call."""
    in_box = sum(1 for r in rows if not r["ADDRESS"].upper().endswith(", FL"))
    above = [r for r in rows if isinstance(r["ARV SCREEN"], int)]
    floor_ok = [r for r in above if r["ARV SCREEN"] >= BUY_BOX["arv_floor"]]
    over_cap = [r for r in rows
                if isinstance(r["OFFER HIGH (60% ARV, no repairs)"], int)
                and r["OFFER HIGH (60% ARV, no repairs)"] > BUY_BOX["contract_cap"]]
    lo, hi = BUY_BOX["close_days"]
    print("\nBUY BOX FIT (confirmed 2026-10-31)")
    print(f"  market: {PULL_MARKET} - in the {len(BUY_BOX['markets'])}-market "
          f"hot list. {in_box}/{len(rows)} rows are in-box on geography.")
    print(f"  ARV >= ${BUY_BOX['arv_floor']:,}: {len(floor_ok)}/{len(above)} "
          f"priced rows clear it (the rest are gated out before output)")
    print(f"  contract under ${BUY_BOX['contract_cap']:,}: "
          f"{len(rows) - len(over_cap)}/{len(rows)} clear it")
    print(f"  close 21-30 days vs a 45-90 day assignment assumption: "
          f"TIGHT. A sale date inside 30 days means you cannot perform - "
          f"ask on the call, never assume.")
    print(f"  types/condition/financing: this data cannot tell you SFR vs "
          f"multi or condition. Grade it on the call.")


def write_csv(rows, path: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS,
                                extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    print(f"\nwrote {path}  ({len(rows)} rows x {len(COLUMNS)} columns)")


def offer_calc(arv: float, repairs: float, pct: float | None) -> int:
    """Quote-time calculator. OFFER = pct x ARV - REPAIRS, capped by buyer max.
    NEVER lower the fee to make a deal work - lower the offer."""
    e = economics(arv, repairs)
    pcts = [pct] if pct is not None else [OFFER_LOW_PCT, OFFER_HIGH_PCT]
    print(f"ARV ${arv:,.0f}   repairs ${repairs:,.0f}   "
          f"whole fee ${WHOLE_FEE:,}   my side @50/50 ${MY_SIDE:,}")
    print(f"BUYER MAX (70% cap)          ${e['BUYER_MAX']:,}")
    print(f"{'offer %':<9}{'offer':>11}{'friction':>11}{'fric % ARV':>12}  covers fee?")
    ok_all = True
    for p_ in pcts:
        offer = int(round(p_ * arv - repairs))
        friction = e["BUYER_MAX"] - offer
        covers = friction >= WHOLE_FEE
        ok_all &= covers and offer <= e["BUYER_MAX"]
        print(f"{p_:<9.0%}{'$' + format(offer, ','):>11}"
              f"{'$' + format(friction, ','):>11}"
              f"{friction / arv:>11.1%}  {'yes' if covers else 'NO - lower the offer'}")
    if not ok_all:
        print("under 10% of ARV: the fee and friction do not both fit. "
              "Lower the OFFER, never the fee.")
    return 0


def print_lookup_paths():
    print("""
CASE NUMBER + AUCTION DATE - manual lookup, one per lead. Both ship blank.

CUYAHOGA COUNTY, OH
  1. cpdocket.cp.cuyahogacounty.gov
       search the owner name (or the address for the owner name), open the
       CV case -> read / copy the CASE NUMBER
  2. cuyahoga.sheriffsaleauction.ohio.gov
       paste the case number -> Status must read "Scheduled"
       read: Sale Date · Status · Opening Bid (~2/3 of judgment) · Judgment
     Both auction sites are login-gated - do not try to script them.

BROWARD COUNTY, FL (only if you add that market)
  1. browardclerk.org -> search by owner -> case number
     NOTE: the Clerk does not index auctions by address.
  2. broward.realforeclose.com -> paste case number -> Sale Date · Status

Then: CALL FIRST. On the call ask "has a sale date been set?" and write it in.
RV closes in 21-30 days, so the window is tight by design.
  > 30 days out   -> normal
  0-30 days out   -> TRIAGE: one fast call, or explain honestly and step back
  date has passed -> the owner may already have lost it. Verify ownership first.
""")
    print("""STEP 1  Call the stacked leads first.
STEP 2  6 condition questions + "has a sale date been set?"
STEP 3  Ask for the 5 photos. No photos, no price.
STEP 4  Grade, then quote from OFFER LOW (55%). Never open at the top.
STEP 5  Log CALL STATUS the same day, dated.
STEP 6  Work the 7-touch cadence.
STEP 7  Submit to RV on a verbal - that is what a verbal is for.
STEP 8  Keep the whole fee at $10,000. The split is RV's, not mine to shrink.
""")


# ---------------------------------------------------------------------------
# --selftest: prove every check can FAIL.  A check that cannot fail is worse
# than no check.  14 mutations, 14 targeted FAILs, no collateral PASSes.
# ---------------------------------------------------------------------------

def _clone(rows):
    return [dict(r) for r in rows]


def _mutation_1(rows, ctx):
    rows[0]["OWNER"] = "WELLS FARGO BANK NA"


def _mutation_2(rows, ctx):
    rows[0]["OWNER"] = "SMITH HOLDINGS LLC"


def _mutation_3(rows, ctx):
    rows[0]["ARV SCREEN"] = ARV_FLOOR - 1


def _mutation_4(rows, ctx):
    rows[0]["REPAIRS"] = 20000
    rows[0]["REPAIRS STATUS"] = "UNGRADED"


def _mutation_5(rows, ctx):
    if len(rows) >= 2:
        rows[0]["PRIORITY"], rows[1]["PRIORITY"] = (
            rows[1]["PRIORITY"], rows[0]["PRIORITY"])


def _mutation_6(rows, ctx):
    for r in rows:
        if isinstance(r["ARV SCREEN"], int):
            r["BUYER MAX (ceiling, 70%)"] = int(r["ARV SCREEN"] * 0.75)
            return
    raise AssertionError("no priced row to mutate")


def _mutation_7(rows, ctx):
    for r in rows:
        if isinstance(r["BUYER MAX (ceiling, 70%)"], int):
            r["OFFER HIGH (60% ARV, no repairs)"] = (
                r["BUYER MAX (ceiling, 70%)"] + 1000)
            return
    raise AssertionError("no priced row to mutate")


def _mutation_8(rows, ctx):
    dup = dict(rows[0])
    dup["#"] = len(rows) + 1
    rows.append(dup)


def _mutation_9(rows, ctx):
    ctx["merged"] = ctx["distinct_before"] + 1


def _mutation_10(rows, ctx):
    for r in rows:
        if isinstance(r["COMPS N"], int):
            r["COMP NEIGHBOURHOOD"] = "ZZ999"
            return
    raise AssertionError("no comped row to mutate")


def _mutation_11(rows, ctx):
    for r in rows:
        if isinstance(r["COMP RADIUS MI"], (int, float)):
            r["COMP RADIUS MI"] = RADIUS_CAP + 0.5
            return
    raise AssertionError("no comped row to mutate")


def _mutation_12(rows, ctx):
    for r in rows:
        if isinstance(r["COMPS N"], int):
            r["COMPS N"] = 2
            return
    raise AssertionError("no comped row to mutate")


def _mutation_13(rows, ctx):
    for r in rows:
        if r.get("_comp_dates"):
            r["_comp_dates"] = [ctx["as_of"] - timedelta(days=400)]
            return
    raise AssertionError("no comped row to mutate")


def _mutation_14(rows, ctx):
    no_comps = [r for r in rows if not isinstance(r["COMPS N"], int)]
    if not no_comps:
        raise AssertionError("fixture produced no unpriced row")
    no_comps[0]["ARV SCREEN"] = 199_000
    no_comps[0]["ARV BASIS"] = "made up"


MUTATIONS = [_mutation_1, _mutation_2, _mutation_3, _mutation_4, _mutation_5,
             _mutation_6, _mutation_7, _mutation_8, _mutation_9, _mutation_10,
             _mutation_11, _mutation_12, _mutation_13, _mutation_14]


def regression_economics() -> int:
    """The two worked examples and the floor table from PART 5, asserted.
    These are independent of any data: if they move, the model is wrong."""
    fails = 0

    def expect(label, got, want):
        nonlocal fails
        ok = got == want
        fails += 0 if ok else 1
        print(f"  {'PASS' if ok else 'FAIL'}  {label:<52} got {got} want {want}")

    print("\nECONOMICS REGRESSIONS")
    e = economics(150_000)                       # the pinned regression
    expect("ARV 150k: buyer max", e["BUYER_MAX"], 105_000)
    expect("ARV 150k: offer high (60%)", e["OFFER_HIGH"], 90_000)
    expect("ARV 150k: friction", e["FRICTION"], 15_000)

    e = economics(350_000, 34_933)               # graded C3, 1600 sqft
    expect("ARV 350k / 34,933 repairs: buyer max", e["BUYER_MAX"], 210_067)
    expect("ARV 350k / 34,933 repairs: offer @60%", e["OFFER_HIGH"], 175_067)
    expect("ARV 350k / 34,933 repairs: friction @60%", e["FRICTION"], 35_000)
    expect("ARV 350k / 34,933 repairs: offer @55%", e["OFFER_LOW"], 157_567)

    expect("ARV 125k: friction @60%", economics(125_000)["FRICTION"], 12_500)
    expect("ARV 125k: friction @55%",
           economics(125_000)["BUYER_MAX"] - economics(125_000)["OFFER_LOW"], 18_750)
    expect("ARV 150k: friction @55%",
           economics(150_000)["BUYER_MAX"] - economics(150_000)["OFFER_LOW"], 22_500)
    expect("ARV 200k: friction @60%", economics(200_000)["FRICTION"], 20_000)

    f = economics(125_000)["FRICTION"]
    ok = f >= WHOLE_FEE
    fails += 0 if ok else 1
    print(f"  {'PASS' if ok else 'FAIL'}  $125k floor friction covers the whole "
          f"fee (${f:,} vs ${WHOLE_FEE:,})")
    ok = MY_SIDE == WHOLE_FEE // 2 and WHOLE_FEE == 10_000
    fails += 0 if ok else 1
    print(f"  {'PASS' if ok else 'FAIL'}  whole fee stays $10,000, my side is an "
          f"output ({MY_SIDE:,})")
    return fails


def selftest(fixture_path: str) -> int:
    as_of = date.fromisoformat(
        json.load(open(fixture_path, encoding="utf-8"))["meta"]["as_of"])
    rows, ctx = run_pipeline(fixture_path, as_of, DEFAULT_CHANNELS, False, None)
    base = run_checks(rows, ctx)
    econ_fails = regression_economics()
    print("\nSELFTEST - baseline on synthetic fixture")
    base_ok = print_checks(base)
    if not base_ok:
        print("baseline already FAILs: fix the pipeline before trusting the "
              "mutations")
        return 1

    print("\nSELFTEST - each mutation must flip exactly the check it targets")
    failures = 0
    for i, mutate in enumerate(MUTATIONS, start=1):
        r2, c2 = _clone(rows), dict(ctx)
        try:
            mutate(r2, c2)
        except AssertionError as exc:
            print(f"  {i:>2} SKIP  mutation could not run: {exc}")
            failures += 1
            continue
        res = run_checks(r2, c2)
        target_ok = res[i - 1][1]
        others = [n for j, (n, ok, _d) in enumerate(res, start=1)
                  if j != i and not ok]
        if target_ok:
            failures += 1
            print(f"  {i:>2} FAIL  check {i} did not detect its own defect "
                  f"(check {i} still PASS; collateral FAILs: {others})")
        else:
            print(f"  {i:>2} PASS  defect {i} -> check {i} FAILs "
                  f"(collateral: {', '.join(others)})")
    print(f"\n{len(MUTATIONS) - failures}/{len(MUTATIONS)} checks proven able "
          f"to fail")
    print(f"{'PASS' if econ_fails == 0 else 'FAIL'}  economics regressions "
          f"({econ_fails} failing)")
    return 0 if (failures == 0 and econ_fails == 0) else 1


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def verify_endpoint(as_of: date) -> int:
    api = Arcrest(None, as_of)
    print(f"[probe] {BASE_LAYER}?f=json")
    fields = api.probe_fields()
    missing = REQUIRED_FIELDS - set(fields)
    print(f"        {len(fields)} fields; required missing: "
          f"{sorted(missing) if missing else 'none'}")
    total = 0
    for channel in DEFAULT_CHANNELS:
        where = channel_where(channel)
        n = api.count(where)
        total += n
        print(f"[count] {channel:<15} {n:>6}  where={where}")
    print(f"[count] channel hits total  {total:>6}  (prompt baseline 4,481)")
    cwhere = comp_where(as_of)
    n = api.count(cwhere)
    print(f"[count] comp universe       {n:>6}  (prompt baseline 8,469)")
    print(f"[count] where={cwhere}")
    return 0 if not missing else 1


def main(argv=None) -> int:
    global MIN_LIEN
    ap = argparse.ArgumentParser(
        description="Cuyahoga pre-foreclosure / probate / lien pull -> 39-column "
                    "ranked lead list.",
        epilog="Exit code is non-zero if any self-check FAILs.")
    ap.add_argument("--source", default="live",
                    help="'live' (default) or a path to a fixture .json")
    ap.add_argument("--out", default=None,
                    help="CSV path (default leadgen/out/LEADS_cuyahoga.csv; "
                         "fixture runs default to leadgen/out/FIXTURE_*.csv)")
    ap.add_argument("--as-of", default=date.today().isoformat(),
                    help="as-of date for the 12-month window (YYYY-MM-DD)")
    ap.add_argument("--with-delinquent", action="store_true",
                    help="add the optional 4th channel "
                         "(grand_total_balance >= 3000). Off by default: the "
                         "4,481-hit baseline is the 3-channel set.")
    ap.add_argument("--min-lien", type=float, default=MIN_LIEN)
    ap.add_argument("--strict-substring-entities", action="store_true",
                    help="match INC/LLC/CORP by substring exactly as the "
                         "spec says. Off by default because 'VINCENT' and "
                         "'LINCOLN' contain INC.")
    ap.add_argument("--cache", default=".cache/leadgen",
                    help="raw-response cache directory ('' to disable)")
    ap.add_argument("--verify-endpoint", action="store_true",
                    help="probe fields + channel counts, then stop")
    ap.add_argument("--selftest", action="store_true",
                    help="run the synthetic fixture and prove all 14 checks "
                         "can FAIL (offline, no network)")
    ap.add_argument("--print-lookup-paths", action="store_true")
    ap.add_argument("--offer", type=float, default=None, metavar="ARV",
                    help="quote calculator: print buyer max / offer low / "
                         "offer high / friction for this ARV")
    ap.add_argument("--repairs", type=float, default=0.0,
                    help="with --offer: repairs from a real grade")
    ap.add_argument("--pct", type=float, default=None,
                    help="with --offer: offer as a fraction of ARV "
                         "(default: show 55% and 60%)")
    ap.add_argument("--top", type=int, default=12)
    args = ap.parse_args(argv)

    MIN_LIEN = args.min_lien
    as_of = date.fromisoformat(args.as_of)

    if args.print_lookup_paths:
        print_lookup_paths()
        return 0
    if args.offer is not None:
        return offer_calc(args.offer, args.repairs, args.pct)
    if args.verify_endpoint:
        return verify_endpoint(as_of)
    if args.selftest:
        here = os.path.dirname(os.path.abspath(__file__))
        return selftest(os.path.join(here, "fixtures",
                                     "cuyahoga_synthetic.json"))

    channels = list(DEFAULT_CHANNELS)
    if args.with_delinquent:
        channels.append("delinquent")

    print("=" * 78)
    print("CUYAHOGA PULL - ranked lead list. Every price is PRELIMINARY.")
    print(f"as-of {as_of.isoformat()}  channels: {', '.join(channels)}")
    print("=" * 78)
    print_weight_table()

    rows, ctx = run_pipeline(args.source, as_of, tuple(channels),
                             args.strict_substring_entities, args.cache or None)
    print_funnel(ctx)
    print_signal_combos(rows)
    print_buybox(rows)
    print_top(rows, args.top)

    if not rows:
        print("\nZERO ROWS KEPT - do not ship an empty list. Check the funnel.")
        return 2

    out = args.out
    if out is None:
        here = os.path.dirname(os.path.abspath(__file__))
        name = ("LEADS_cuyahoga.csv" if args.source == "live"
                else "FIXTURE_synthetic.csv")
        out = os.path.join(here, "out", name)
    if args.source != "live" and os.path.basename(out).startswith("LEADS_"):
        raise SystemExit("refusing to write synthetic fixture data to a "
                         "LEADS_*.csv - pass --out")
    write_csv(rows, out)

    results = run_checks(rows, ctx)
    ok = print_checks(results)
    print_lookup_paths()
    if not ok:
        print("EXITING NON-ZERO: a self-check FAILED. Do not dial this list.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
