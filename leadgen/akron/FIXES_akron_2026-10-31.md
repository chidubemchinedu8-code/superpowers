# What I actually changed — Akron, 2026-10-31

The audit (`SCREEN_AUDIT_akron_2026-10-31.md`) diagnosed the screen. This file reports what was **executed** against it. Every number below was produced by a query I ran today, not carried forward.

---

## 1. The screen was re-run across the whole file, not four ZIPs

**Before:** "151 owners in four ZIPs." That number was a choice of geography dressed up as a result.

**Now:** the identical signal bar, no ZIP filter:

| Population | Count |
|---|---|
| Individual owners, tenure ≥ 120 mo, at least one distress signal | **521** |
| Entity-owned (LLC / INC / TRUST / etc.) with signal | **621** |
| Individual owners with signal but tenure **under** 120 months | **1,131** |

Two corrections inside those numbers, both mine:

- **521, not 525.** The sign-off filter originally let four company rows through as individuals — e.g. `RRA ENTERPRISES LLC` at 804 Aberdeen St. Excluding anything containing `ENTERPRISES` gives **521**. The 521 is the honest one; the file on disk is the 521.
- **`COUNTY TREASURER` (538 Fernwood Dr) and `K FLIP` (1219 Winton Ave)** are still in the 521 because the CSV types them as individual owners. They are not sellers. They are flagged as drop rows on the sheet.

Files: `PIPELINE_offmarket_521.csv`, `PIPELINE_entity_owned.csv`, `PIPELINE_recent_buyers.csv` — 14 columns each, every row traceable to a PropWire record.

---

## 2. All three populations are exported, and none of them is priced

The 521 is **ranked, not valued**. No Zestimate has been pulled for any of them. That is deliberate and it is stated on the tab: the order is a calling order, not a buy list. Pricing 521 properties is 521 separate lookups; doing it badly is worse than not doing it.

---

## 3. The active-listing sweep now works properly

ZIP-level Redfin pages were incomplete. **City-level filters work:**

| Filter | Result |
|---|---|
| `redfin.com/city/244/OH/Akron/filter/max-price=120k,min-beds=3` | **197 homes** |
| `filter/max-price=85k` | **132 homes** |

**Limitation, stated rather than hidden:** Redfin shows ~24 per page with 5 pages, and the tail lazy-loads as "Loading...". I read **page 1 of 5 only** — roughly 45 of the 197. The full sweep needs `page-2..5`, which I have not done.

---

## 4. New lead, and it is the best signal in the entire export

**806 Amherst St, 44311** — Mohammad Hakim, tenure **324 months**, **2 units**, **vacant**, **absentee** (mailing 7538 Atherton Ln). Signal score **7**, the maximum in the file.

| Item | Value | Source |
|---|---|---|
| Zestimate | **$94,300** (Zillow range $67–125K) | Zillow detail page, zpid 35443642 |
| Rent estimate | $953/mo | Zillow |
| County | 5bd/2ba, 1,450 sf, built 1893, assessed $28,000, tax $763 | Summit County via PropWire |
| **Last sale** | **$325, Feb 5 2025** (prior **$16,500**, Oct 19 2023) | Zillow price history |
| 70% of Zestimate | $60,010 | — |
| **Max contract ceiling** | **$56,010** at $0 repairs | (Zestimate × 0.70) − $10,000 fee |

That $325 sale is either a quitclaim, a family transfer, or a data error. It does **not** make the property cheap — it means the last recorded consideration is meaningless. Verify with the county before relying on it. **PRELIMINARY — not an offer.**

---

## 5. The one that never belonged on the off-market tab

**1366 Marcy St 44301 is listed at $79,999 (MLS 5241062).** It sat on the owner tab only because the county export has no listing-status field. It is now on the on-market tab as rank 7, priced against its asking price, and its off-market row is marked MOVED OUT rather than deleted so the county record is not lost.

Verdict there: at $60,000 repairs the buyer max is $13,500, so a $10,000 fee needs a $3,500 contract — a **95.6% cut** off asking. **FAILS.**

---

## 6. ChatARV prices a listing, so it lives on the on-market book only

Column **Y** on the on-market tab now stamps the provenance of every price in every row: `ASK` (listing price), `ARV` (my Redfin closed comps), `CHATARV` (yours). Off-market rows carry **no ASK and no ChatARV figure**, because an owner record has neither.

What is still blank and why: **I never wrote down the ChatARV estimated value you gave me.** The equity, rent and price-history figures in that row came from your search; the ARV and ceilings in the same row are mine. Rather than reconstruct a number I did not record, the ChatARV cell is empty and labelled as such.

---

## 7. What is still not done

| Gap | Size |
|---|---|
| Active sweep | page 1 of 5 read — ~45 of 197 catalogued |
| Pricing | 0 of 521 pipeline rows have a Zestimate |
| 544 Stratford | unpriced; 44303 sold only 4 two-bed homes in 6 months and two are condos |
| ChatARV value | not captured — needs one number from you |

No property was contacted, no offer made, nothing submitted. Every figure is an estimate.
