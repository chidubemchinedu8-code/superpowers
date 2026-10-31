# PropWire export → Akron off-market call list

**As of 2026-10-31 · source file: `Propwire Export - 10000 Properties - Oct 31, 2026.csv`**
**Every number below is PRELIMINARY — not an offer. Nothing has been called, submitted or offered.**

---

## 1. What the file actually is

| Check | Measured result |
|---|---|
| Rows | **10,000** exactly |
| Geography | 100% Akron, Summit County, OH |
| `Id` sequence | strictly ascending across all 9,999 steps → **an Id-ordered slice, truncated at the 10,000 export cap** |
| Columns | **43**, all assessor/owner fields |
| Estimated value | **absent** |
| Est. equity % / mortgage / free-&-clear flag | **absent** |
| MLS status / list price / DOM | **absent** |

**Consequence, stated plainly: this export cannot be underwritten on its own terms.** There is no value, no debt position, no asking price and no MLS status in it. Every ARV in this report had to be rebuilt from Redfin sold data, and every offer number is an inference, not a read.

**I also cannot confirm which lead type produced it.** The export omits the field that would prove "Free & Clear", so that claim stays unverified. Two tells say a filter *was* applied:
- **max `Year Built` = 1973 across all 10,000 rows** — impossible for an unfiltered Akron pull, which contains new construction
- `141 Grand Ave`, `6090 Manchester Rd` and `82 Aqueduct St` are all **absent** even though their ZIPs (44302, 44319, 44303) are covered

ZIP distribution, which matters more than anything else in this file:

| ZIP | rows | | ZIP | rows |
|---|---|---|---|---|
| 44306 | 1,736 | | 44312 | 450 |
| 44314 | 1,377 | | 44302 | 228 |
| 44320 | 1,370 | | 44304 | 103 |
| 44310 | 1,316 | | 44303 | **83** |
| 44305 | 1,268 | | 44313 | **31** |
| 44301 | 935 | | 44319 / 33 / 21 | **4 total** |
| 44307 | 569 | | 44311 | 530 |

**84% of the file sits in the six ZIPs where renovated retail clears $75K–$115K.** That is the lead-count-maximising, margin-destroying end of the market — the exact failure mode the strategy predicted. Only **449 rows** are in the ZIPs where the 70% rule has a chance.

---

## 2. Data-integrity findings (measured, not assumed)

### 2a. Living area disagrees with MLS by up to 2.0×

Three of my six existing leads appear in the export. Independent comparison, export vs MLS listing data:

| Property | Export `Living Square Feet` | MLS / Redfin | Ratio |
|---|---|---|---|
| 75 E Ido Ave 44301 | **924** | 1,848 | **0.50×** |
| 156 Colony Cres 44305 | **1,080** | 1,944 | 0.56× |
| 838 Fess Ave 44307 | not in file | 1,393 | — |

**2 of 2 checkable properties are understated by roughly half.** Any $/sqft or ARV built on this column would be wrong by ~100%. **No ARV in this report uses the export's square footage.**

### 2b. `Owner Type` is mislabelled

`156 COLONY CRES` is tagged **`BANK`** in `Owner Type` but the owner of record in the very same row is **NATHANIEL YEARGIN**, an individual, 96 months of ownership, owner-occupied mailing address. The field also tags numerous LLCs as `INDIVIDUAL`. **The column was discarded; ownership class was re-derived from the owner name string instead.**

### 2c. `Ownership Length (Months)` has impossible values

Maximum = **1,522 months = 126 years**. Median 139 months. Only 77 of 10,000 rows exceed 30 years, which is not credible for a free-and-clear population. Tenure was used only as a screen to *rank calls*, never as an input to price.

### 2d. A consistency check that *passed*

`Owner Occupied = 1` (7,525 rows) exactly equals the count of rows where the owner mailing address equals the property address (7,525). Two independent computations agree → the occupancy flag is trustworthy, the owner-type flag is not.

### 2e. Cross-reference hit against an existing lead

Earlier I found an active wholesale listing at **1364-1366 Marcy St, 44301, asking $79,999**. The export supplies the owner of record for **1366 Marcy St**: **TANGELA WEST**, 2 units, 242 months, **vacant**. That is a name added to a lead I previously had only as an address — the one concrete thing this file delivered that I could not get elsewhere.

---

## 3. Owner profile of the only ZIPs that matter (44302 + 44303)

311 rows. **113 entity-owned (LLC/trust/corp), 198 individual names.** 37 vacant. 64 multi-unit. Median tenure 131 months; 76 rows at 180+ months.

Of the 198 individual owners, **19 clear a real signal bar** (tenure ≥120 months plus vacancy, absenteeism or multi-unit). Those are below. The 113 entities are not callable targets — they price to a spreadsheet and already know what they own.

---

## 4. The call list — 13 leads, ranked

ARV = verified sold comps in the same ZIP (comp set in §6). Repairs = scope-based band, **no inspection, no photos**. `Max contract` = buyer max − $10,000 fee. If a seller won't take the top of the range, walk.

| # | Priority | Address | Owner | Tenure | Vac | Units | Est. ARV | Est. repairs | Max contract |
|---|---|---|---|---|---|---|---|---|---|
| 4 | **HIGH** | 182 Westwood Ave 44302 | Robin Henry | 19 yr | – | 2 | $140K–$165K | $45K–$60K | **$28K–$60K** |
| 6 | **HIGH** | 256 Crosby St 44303 | Michael Masters | 10 yr | – | 2 | $140K–$165K | $45K–$60K | **$28K–$60K** |
| 7 | **HIGH** | 647 Crosby St 44302 | Rupesh Singh | **24 yr** | – | 1 | $170K–$200K | $45K–$65K | **$44K–$85K** |
| 8 | **HIGH** | 544 Stratford Ave 44303 | Samira Kakish | **23 yr** | – | 1 | $170K–$200K | $50K–$70K | **$39K–$80K** |
| 10 | **HIGH** | 159 Gale St 44302 | Arthur Andes | **23 yr** | – | 2 | $140K–$165K | $45K–$60K | **$28K–$60K** |
| 11 | **HIGH** | 116 S Balch St 44302 | Markus Vogl | **22 yr** | – | 2 | $140K–$165K | $45K–$60K | **$28K–$60K** |
| 12 | **HIGH** | 43 S Bates St 44303 | Brody Williams | 13 yr | **YES** | 2 | $140K–$165K | $45K–$60K | **$28K–$60K** |
| 13 | MED | 1366 Marcy St 44301 | Tangela West | 20 yr | **YES** | 2 | $120K–$140K | $45K–$60K | $14K–$43K *(already listed $79,999 — passes)* |
| 1 | MED | 239 Crosby St 44303 | Joel Hernandez | **23 yr** | **YES** | 3 | $170K–$190K | $80K–$120K | −$11K–$43K |
| 2 | MED | 163 Beck Ave 44302 | Ricky Lin | 22 yr | – | 3 | $170K–$190K | $80K–$120K | −$11K–$43K |
| 3 | MED | 311 Rhodes Ave 44302 | Towanda Mullins | 19 yr | – | 3 | $170K–$190K | $80K–$120K | −$11K–$43K |
| 5 | MED | 250 Crosby St 44303 | Michael Masters | 10 yr | – | 3 | $170K–$190K | $80K–$120K | −$11K–$43K |
| 9 | MED | 283 Gordon Dr 44302 | Denota Strickland | 17 yr | **YES** | 1 | $120K–$150K | $55K–$75K | −$1K–$40K |

**The single most important pattern in this table:** every 3-unit property fails on the conservative case. A 3-unit at a $170K–$190K ARV cannot absorb $80K–$120K of rehab and still leave a fee. Duplexes and small SFRs survive; triplexes do not.

---

## 5. Three detailed underwrites

### 5.1 `647 Crosby St, 44302` — highest max contract, and it is a real cold call not a distress play

- **Owner:** Rupesh Singh · **26513 Basswood Ave, Rancho Palos Verdes, CA 90275** · 293 months (24.4 yr) · not occupied by owner
- **Property:** 2 bed / 2 bath, assessed 973 sf, built **1894**, single family, no vacancy flag
- **Comps (verified sold, same ZIP):** 137 N Rose Blvd (3/1, 1,320 sf) **$200,000**; 817 Weber Ave (3/1.5, 1,450 sf) **$200,000**; 612 Ardleigh Dr (3/2, 1,180 sf) **$255,000**; 556 Royal Ave (3/2, 1,551 sf) **$220,000**
- **ARV band:** $170,000–$200,000 — **low confidence**: 2/2 is a smaller bed count than every comp, and the export's square footage is unreliable (§2a)
- **Repairs:** $45,000–$65,000. Visible/known: none. Scope assumed for a 1894 structure with one bath count per floor: roof, furnace, electrical service, kitchen, two baths, flooring, paint. **All inspection-dependent. Nothing here is from a photo.**
- **Buyer max:** $54,000–$95,000 → **max contract $44,000–$85,000**

**Honest read:** a 24-year California absentee on a 130-year-old house is a plausible tired-landlord seller. But the required discount is 55–75% off renovated retail. Expect "no". Worth one call because the owner is absent, elderly-tenure and the property is not advertised anywhere.

### 5.2 `256 Crosby St` + `250 Crosby St, 44303` — the only true portfolio seller in the file

Two adjacent parcels, **same owner, same 128-month tenure, same mailing address (California Ave, Akron 44314)**, one a 2-unit and one a 3-unit. Single call, two assets, one decision-maker.

- **256 Crosby:** 2 units, 2/2, 1,029 sf, 1869 → max contract **$28K–$60K**
- **250 Crosby:** 3 units, 3/3, 1,052 sf, 1869 → max contract **−$11K–$43K**
- **Combined max contract: $17,000–$103,000**, and the low end is negative, so **the only workable version is buying the pair at the bottom of the duplex range and treating the triplex as a throw-in.**

Do not lead with a price on this call. Lead with "you own two on the same block, both 1869, both need everything — what would it take to be done with both."

### 5.3 `239 Crosby St, 44303` — best owner signal in the file, worst math

**3 units · 1,433 sf · built 1874 · owned 23.4 years · vacant flag set · owner-occupant on record.**

The vacancy flag and the owner-occupant flag together mean one of two things: the owner lives in one unit and two are empty, or the owner has left and the whole building is empty. Both are strong. This is the best-motivated owner in the file.

**And it still fails.** $170K–$190K ARV against $80K–$120K of rehab on an 1874 three-unit leaves a max contract of $43,000 at the absolute ceiling and **negative** on any conservative case. There is no 3-unit sold comp in 44303 — the bracket is borrowed from 44305, which is a different market.

**Recommendation: call it, do not offer on it.** Ask what the taxes and insurance are and whether the two empty units are rentable. If the owner volunteers a number under $45,000, the deal changes. Otherwise it is a data point on how 1874 triplexes price in Highland Square, and that data point is worth having.

---

## 6. Comp set used (all verified sold, Redfin, same or adjacent ZIP)

**44303 / 44302 renovated 3-bed:**
817 Weber Ave 3/1.5 1,450 sf $200,000 · 137 N Rose Blvd 3/1 1,320 sf $200,000 · 556 Royal Ave 3/2 1,551 sf $220,000 · 736 Wellesley Ave 3/1.5 1,520 sf $244,500 · 612 Ardleigh Dr 3/2 1,180 sf $255,000 · 56 N Highland Ave 3/2 1,672 sf $225,000 · 557 Weber Ave 3/2 1,946 sf $180,000

**44302 / 44303 distressed floor — the discount that makes this possible:**
432 Kathleen St 3/1 1,080 sf **$85,000** · 14 Stewart Way 3/1 1,144 sf **$53,000**

**Duplex / multi (no 44302–44303 duplex comp exists — borrowed, therefore unreliable):**
280 Cluster Ave $184,000 · 1224 Pondview Ave $190,000 · 325 Para Ave $125,000 · 52 E Brookside Ave $117,500 · 31 E Brookside Ave $142,000

**44311 — the ZIP that proves the point:** 829 Yale St 3/1 $57,000 · 798 Amherst St 3/1 $59,000 · 289 Sumner Ct 4/2 1,233 sf $76,000 · 255 Cross St 4/2 ~1,700 sf $80,000 · 651 Kling St 4/1.5 1,691 sf $91,000 · 361 Cross St 4/1 1,036 sf $97,500 · 256 Sues Ct 4/2 1,312 sf $100,000.

44311 has 530 export rows, two vacant long-tenure duplexes at **852 Amherst** and **810 Amherst** owned by the same man (Kenneth Mohler, 28 and 25 years), and a **$95K–$105K renovated ceiling**. At 70% minus a $45K–$60K rehab, max contract there is roughly **$10K–$15K**. The best owner signals in the file sit in the worst-priced ZIP. That single fact is worth more than any lead in this report.

---

## 7. What this changes about the strategy

1. **Screen A (cheap house, expensive ZIP) is confirmed, not replaced.** Arbitrary free-&-clear volume lands you in 44306/44314/44320/44310 where the math is arithmetically impossible. The ZIP selection *is* the strategy.
2. **Free & Clear alone is not sufficient.** It finds the right people — 24-year absentees, 23-year owner-occupants — but Akron's ARV-to-repair ratio still kills the 70% rule on most of them. It is a **calling list generator**, not a deal generator.
3. **Triplexes are a trap in this market.** Four of the six best owner signals are 3-units and all four fail.
4. **Duplexes in 44302/44303 are the real target** and I have **no sold comp for one**. That is the single most valuable thing to fix next: three duplex sold comps in 44302/44303 would let this list be priced instead of bracketed.

---

## 8. What I still cannot do

- **Verify any of these 13 owners is alive, willing, or contactable.** No phone numbers. The export has no phone, email, or skip-trace field. Calling requires a skip trace on the name + mailing address.
- **Confirm the export was filtered by Free & Clear.** Send the export that includes `Estimated Value`, `Equity %` and `MLS Status` and this list can be repriced in one pass instead of bracketed from borrowed comps.
- **Confirm condition on any property.** No photos were available for any of the 13. Every repair figure is a scope assumption.

**No seller has been contacted. No offer has been made. No contract exists.**
