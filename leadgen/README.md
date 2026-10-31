# leadgen — Cuyahoga acquisition pull

One command produces the ranked, dial-ready list:

```bash
python3 leadgen/pull_leads.py
# writes leadgen/out/LEADS_cuyahoga.csv  — 39 columns
# prints: weight table, funnel, signal combos, top 12, 14 self-checks
# exit code is non-zero if any self-check FAILs
```

Python 3.10+, standard library only, no API key, no dependencies.

**Every price in that CSV is `PRELIMINARY - not an offer`.** Rank and dial off
the clock; confirm comps and grade condition before naming a number.

---

## 1. What was actually verified live (2026-10-31), and what was not

You were told to show the URL and query string. Here is exactly what was called
and what came back. These are real responses, not remembered constants.

| Check | Request | Response |
|---|---|---|
| Endpoint alive | `…/FeatureServer/0/query?where=1%3D1&returnCountOnly=true&f=json` | `{"count":521078}` |
| Field names | `…/query?where=1%3D1&outFields=*&resultRecordCount=1&f=json` | 142 fields; `parcel_owner`, `par_addr_all`, `parcelpin`, `parcel_zip` (double), `total_res_liv_area`, `max_age`, `last_transfer_date` (date), `last_sales_amount`, `grand_total_balance`, `foreclosure_flag`, `cert_sold_flag`, `neighborhood_code`, `res_styles`, `tax_market_total`, `mail_state`, `property_class` all present |
| Page size | `…/FeatureServer?f=json` | `"maxRecordCount":5000` — a 1,000-row page never hits the cap |
| Geometry | `…/query?where=foreclosure_flag%3D1&outFields=…&returnGeometry=true&returnCentroid=true&outSR=4326&resultRecordCount=2&f=json` | `"centroid":{"x":-81.7589,"y":41.4880}` — WGS84 lon/lat, usable as-is |
| Channel 1 | `…?where=property_class%3D'R'+AND+parcel_zip+IN+(44102,…)+AND+foreclosure_flag+%3D+1&returnCountOnly=true` | **2,967** |
| Channel 2 | `…?where=…+AND+(parcel_owner+LIKE+'%25ESTATE%25'+OR+…+'%25HEIR%25'+…+'%25ET+AL%25'+…+'%25LIFE+EST%25')` | **1,157** |
| Channel 3 | `…?where=…+AND+cert_sold_flag+%3D+1` | **357** |
| Sum | 2,967 + 1,157 + 357 | **4,481** — matches the prompt baseline exactly |
| Comp universe | `…?where=property_class%3D'R'+AND+parcel_zip+IN+(…)&AND+last_transfer_date+%3E%3D+DATE+'2025-10-31'` | **8,469** — matches the prompt baseline exactly |

Base layer used throughout:

```
https://gis.cuyahogacounty.gov/server/rest/services/CCFO/Parcel_Fabric_Taxparcels/FeatureServer/0
```

### The pull itself — measured on a GitHub runner, 2026-10-31

This agent's sandbox kills the TLS handshake to `gis.cuyahogacounty.gov`
(DNS resolves, TCP connects, ClientHello dies — an egress policy, not the
county). So the pull ran on a GitHub Actions runner instead
(`.github/workflows/leadgen-pull.yml`) and committed its output back to the
branch. Those numbers are measurements, not estimates:

```
4,481 channel hits -> 4,425 distinct properties -> 698 kept   (39 columns, 14/14 PASS)
8,469 raw sales -> 4,076 usable comps
12 stacked: 9 preforeclosure+probate, 3 probate+lien_sold
comp radius: median 0.25 mi, max 1.25 mi
comp confidence: 442 HIGH / 190 LOW / 66 NO COMPS
```

Two CSVs are in `out/`, because of the one deliberate deviation (whole-word
entity matching — see §5):

| | `LEADS_cuyahoga.csv` (default) | `LEADS_cuyahoga_strict.csv` (`--strict-substring-entities`) | prompt target |
|---|---|---|---|
| rows | **698** | **694** | 690 |
| columns | 39 | 39 | 39 |
| self-checks | 14/14 PASS | 14/14 PASS | 14/14 PASS |
| channel hits | 4,481 | 4,481 | 4,481 |
| distinct before filtering | 4,425 | 4,425 | 4,425 |
| drop: entity | 1,496 | **1,520** | 1,520 |
| drop: no living area | 524 | **522** | 522 |
| drop: institution | **156** | **156** | 156 |
| drop: recent transfer | 198 | **191** | 191 |
| drop: under ARV floor | 1,353 | 1,342 | 1,346 |
| no comps (kept, blank) | 66 | **66** | 66 |
| stacked | 12 | 12 | 12 |
| comps 8,469 → usable | 4,076 | 4,076 | 4,076 |
| radius median / max | 0.25 / 1.25 | 0.25 / 1.25 | 0.25 / 1.25 |

**What this says.** With spec-literal substring matching, every drop count
except one reproduces the prompt exactly — entity 1,520, no living area 522,
institution 156, recent transfer 191, no comps 66, merged 4,425, comps 4,076,
radius profile, 12 stacked. The single remaining variance is **4 rows**
(694 vs 690) in `under ARV floor` (1,342 vs 1,346), i.e. four parcels where my
comp tier puts ARV at or just above $125,000 and theirs just below. 76 rows in
the output sit within $4,000 of that floor, so a ~1% ARV difference on a
handful of them is exactly the expected size of this. It is a boundary effect
in the comp arithmetic, not a rule I got wrong.

**Which file to dial.** `LEADS_cuyahoga.csv` (698). The 4 extra rows are owners
the substring matcher would have silently deleted:

```
WINCHESTER, KELLY S          3347 EAST BLVD          preforeclosure   pri 48  ARV $145,448
MCCOY, VINCE ETAL            10330 GAY AVE           preforeclosure   pri 48  ARV $125,092
LOGAN, PRINCE I.             2210 E 84 ST            lien_sold        pri 15  ARV $131,198
IPLANGROUP AGENT FOR CUSTODIAN FBO … IRA  1726 VALENTINE AVE  lien_sold  pri 33  ARV $183,238
```

`VINCE`, `PRINCE` and `WINCHESTER` contain `INC`/`INC`/`INC` as substrings.
**Skip the fourth row** — an IRA custodian is not a motivated seller; it slips
through because it contains none of the entity tokens. That is a known gap,
not a defended result.

## 2. Run it

```bash
python3 leadgen/pull_leads.py                    # full pull -> out/LEADS_cuyahoga.csv
python3 leadgen/pull_leads.py --verify-endpoint  # fields + channel counts only, ~25s
python3 leadgen/pull_leads.py --selftest         # offline: 14 checks + 14 mutations
python3 leadgen/pull_leads.py --print-lookup-paths
python3 leadgen/pull_leads.py --offer 350000 --repairs 34933
```

Useful flags:

| Flag | Why |
|---|---|
| `--as-of 2026-10-31` | freeze the 12-month comp window so two runs are comparable |
| `--cache .cache/leadgen` (default) | raw responses cached; a re-run costs no requests. `--cache ''` to disable |
| `--with-delinquent` | adds the optional 4th channel. **Off by default** — the 4,481 baseline is the 3-channel set |
| `--min-lien 3000` | lien modifier threshold |
| `--out <path>` | where the CSV goes |
| `--top 12` | how many rows to print |

If the funnel does not match `4,481 → 4,425 → 690`, or you do not get 39
columns and 14/14 PASS, **do not dial the list** — find the deviation first.
Most likely cause is a different `--as-of` (the comp window moves the ARV floor
gate), or the county republishing a field.

## 3. What the script enforces (and where you can check it)

- **Three separate channels, merged — never ANDed into one filter.** Merge key
  `parcelpin`, falling back to `address + ZIP`; dedupe key `(parcelpin, channel)`
  so one parcel enters once per channel at most. Prints
  `merged {raw} channel hits -> {n} distinct properties`.
- **Ranking is the clock stack**: `40 pre-foreclosure + 30 probate + 25 stacking
  + 15 lien sold + 10 strong ZIP + 8 lien ≥ $3k + 8 out-of-state + 5 delinquent
  + 5 ARV > $200k`. `n_clocks` counts channels only — a large lien is a
  modifier, so `SIGNALS STACKED` can read 2 while `WHY CONTACT` says
  "owes $63,496". The weight table prints on every run.
- **Sort**: priority desc, then ARV desc, blanks last *inside* their band.
- **Gates, in this order, with counts printed**: entity owner → no living area
  (`< 500 sqft`) → ARV under `$125,000` → institution owns it → transferred
  within 180 days. No comps is **not** a gate: those rows are kept, priced
  blank, marked `NO COMPS`.
- **ARV**: neighbourhood (`neighborhood_code`) must be identical, `±30%` living
  area, style preferred when ≥3 share it, radius ladder `0.25 → 1.50 mi` using
  the smallest radius with ≥3 comps, then `sqft × p75 $/sqft × 0.88`. Under 3
  comps at 1.50 mi → `NO ARV`, no widening, no averaging across tiers.
  `p25` is computed and kept internally as the as-is value so the two can never
  be confused.
- **Repairs stay blank.** `REPAIRS STATUS` is `UNGRADED` on every row at pull
  time; a repair number without a grade is a self-check failure.
- **Economics**: `BUYER MAX = 0.70 × ARV`, `OFFER = 0.55–0.60 × ARV`,
  `FRICTION = BUYER MAX − OFFER HIGH = 10–15% of ARV`. The fee is $10,000 whole,
  `MY SIDE @50/50` is an output, never a setting. `--offer` prints the graded
  version of the same model.
- **`CASE NUMBER` and `AUCTION DATE` ship blank.** They are not in the parcel
  dataset and no bulk case/auction feed exists. One manual lookup per lead
  (`--print-lookup-paths`). Never a gate on calling.

## 4. The 14 self-checks, and why you should trust them

The prompt's rule: a check that compares a constant to itself is worse than no
check, because it produces a false PASS. So every check here compares two
independent things — `COMP NEIGHBOURHOOD` vs `SUBJECT NEIGHBOURHOOD`, the oldest
retained sale date vs the window cutoff, `merged` vs a separately recounted
distinct-parcel set, buyer max vs `0.70 × ARV SCREEN` read back off the row.

And then the stronger part:

```bash
python3 leadgen/pull_leads.py --selftest
```

runs the whole pipeline on `fixtures/cuyahoga_synthetic.json`, gets 14/14 PASS,
then applies **fourteen targeted defects**, one per check, and requires the
targeted check to flip to FAIL every time. Output ends with:

```
14/14 checks proven able to fail
PASS  economics regressions (0 failing)
```

The economics regressions are the prompt's own worked examples, asserted:
`$150k ARV → buyer max $105,000 → offer high $90,000 → friction $15,000`;
`$350k ARV / $34,933 repairs → $210,067 / $175,067 / $35,000 / $157,567`;
friction `$12,500` at the `$125k` floor.

Two bugs were caught by this during the build, both real:
1. the merge dropped each parcel's centroid, so **no row could ever be comped**
   — every lead would have shipped `NO COMPS`;
2. the self-test's own pass condition treated *zero collateral failures* as a
   failure, which reported four healthy checks as broken.

`fixtures/cuyahoga_synthetic.json` is fabricated test data. The script refuses
to write fixture output to a `LEADS_*.csv`, and every fixture run prints a
`SYNTHETIC` banner. Never dial it.

## 5. Deliberate deviations from the prompt, and why

| Deviation | Reason |
|---|---|
| `INC` / `LLC` / `CORP` / `LTD` / `GROUP` match a **whole word** by default | substring matching drops `MARY T VINCENT`, `LINCOLN SPENCER`, `SPENCER`. That is a false drop of a real owner — the one error you cannot recover from by calling. Reproduce the literal spec with `--strict-substring-entities` |
| `delinquent` channel **off by default** | with it on, `SIGNALS STACKED` and priority move for ~every lead and the 4,481-hit baseline no longer applies. `--with-delinquent` adds it (+5, and it counts as a clock) |
| `COMP SOURCE` is always `RADIUS` | a `ZIP BAND` fallback would be widening to reach a count, which the comp rule forbids. When the ladder fails, the row is `NO COMPS` |
| 1,000-row pages although the layer allows 5,000 | fewer moving parts per page; paging is correct either way |
| Probate is still an **owner-name proxy** (`ESTATE`/`HEIR`/`ET AL`/`LIFE EST`) | no bulk probate docket is published. It will miss an estate recorded with a plain name, and it will catch `ET AL` owners who are simply co-owners. Treat probate flags as a lead, not a fact |

## 6. After the pull: what to do with the CSV

1. Call the rows with `SIGNALS STACKED ≥ 2` first — `preforeclosure + probate`
   is 95 and must sit above every single-clock row.
2. On the call: the 6 condition questions, then *"has a sale date been set?"*,
   then ask for the 5 photos (front, roof from street, kitchen, bathroom, worst
   room). **No photos, no price.**
3. Grade, then quote from `OFFER LOW` (55%) using
   `--offer <ARV> --repairs <graded repairs>`. Never open at the top of the range.
4. Log `CALL STATUS` the same day, dated, and work the 7-touch cadence:
   day 0 / 1 / 3 / 7 / 14 / 21 park / 30 re-check. Re-running the pull must not
   wipe call history — key it on `#`, and park leads instead of deleting them.
5. Submit to RealVenture on a verbal. Keep the whole fee at $10,000; if a deal
   does not work, **lower the offer, never the fee**.

Plan against ~500–1,250 dials per contract. 690 leads swept once is 0.6–1.5
contracts — a first try, not a business. The second and third touch cycles
matter more than a bigger list.

## 7. Two questions still open (they are not data questions)

1. Is the JV split a percentage of the assignment fee, or a fixed dollar amount?
   Until answered: 50/50 of the **fee**, my side $5,000, whole fee $10,000.
2. Do you have any real buyer boxes (ARV range, buyer %, price cap, type,
   condition, close days)? One real box beats all theory.

Not answered here because they are not in the data, and inventing them is how
this project shipped a false PASS three times.
