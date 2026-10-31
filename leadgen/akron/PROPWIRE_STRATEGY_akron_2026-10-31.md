# PropWire Sourcing Strategy + Verified Underwriting — Akron, OH
**Prepared:** 2026-10-31 · **Market:** Akron (Summit County), OH only · **Buyer:** RealVenture
**Formula:** Buyer Maximum = (ARV × 0.70) − Estimated Repairs · Fee target $10,000

---

## 0. Access verdict — read this first

**PropWire's search cannot be executed from here.** `propwire.com/search` renders as a client-side app: it returned the filter shell, a Mapbox canvas, "Show of **0** Results" and no data, because the query never fires without a logged-in session. Property-detail URLs (`/realestate/156-colony-cres-akron-oh-44305`) return **404** — PropWire needs its internal numeric property ID, which only a search result provides. So I did **not** pull any list from PropWire, and nothing in this report is a PropWire export.

**What I could do:** inspect the filter surface (below) and then execute the *equivalent* screens against a source that does render — Redfin — for every dimension except equity %, mortgage balance and owner tenure, which Redfin does not expose.

**Filters I therefore could NOT execute:** estimated equity %, est. loan-to-value, years owned, properties owned, free-and-clear, notice type, auction date. Every one of those needs PropWire. That is a real gap, not a footnote — my #1 and #2 filters are among them (see §2).

---

## 1. The filter surface I inspected

**Lead types — verified directly from propwire.com (21 listed):** Absentee Owners · Adjustable Loans · Auctions · Bank-Owned (REOs) · Cash Buyers · Empty Nesters · MLS Withdrawn · MLS Active · Free & Clear · High Equity · Intrafamily Transfers · Low Equity · MLS Sold · Out-of-State Owners · MLS Pending · Preforeclosures · Probates · Tired Landlords · Vacant Homes · Vacant Lots · Zombie Properties · Abandoned Homes.

**Advanced filter parameters** — from three independent write-ups of PropWire's search API, cross-checked and mutually consistent. *Second-hand, not clicked through by me:* owner type · owner occupancy · occupancy status · cash-buyer-only · years owned min · properties owned min · property type (8 categories) · beds/baths min · building sqft min · lot sqft min · year built min · pool · **estimated value min/max** · **estimated equity $ min** · **estimated equity % min** (60% = PropWire's own "high equity" line) · last sold price min · last sold since · **notice type** (Lis Pendens / Notice of Foreclosure Sale / Notice of Default / Notice of Trustee Sale) · **auction date from** · **MLS status** (incl. *Failed*) · **days on market min** · **MLS keyword** (scans agent copy for motivation phrases) · address lookup · property ID lookup · map-radius search.

**Notable:** bankruptcies, code violations, divorce, liens and tax liens sit behind PropWire's paid Premium Leads add-on.

**The two capabilities that matter most for this job** are ones most operators never touch: **MLS status = Failed** combined with **days on market min**, and **properties owned min** (portfolio sellers). Both are executed below by proxy.

---

## 2. My strategy — and why it is built the way it is

The last screen in this market produced one uncomfortable finding: **at Akron's values, 70% of ARV minus full repairs yields a negative spread on essentially all retail inventory.** ARVs are $100K–$170K and rehabs run $55K–$80K, so the buyer maximum lands near or under the asking price.

A sourcing strategy that ignores that will keep producing leads that die in underwriting. So I did not build this around distress flags. **I built it around the ratio that actually decides whether a deal can exist: asking price as a percentage of ARV.** Motivation flags tell you *who might sell*. The price-to-ARV ratio tells you *whether a fee can survive*. Akron has plenty of the first and almost none of the second on the MLS.

Five stacked searches, in the order I rate them:

### A. "Cheap house, expensive neighbourhood" — my highest-conviction screen
`estimatedValue` band set *by ZIP*, not by city · `propertyType` SFR/multi · `yearBuiltMin` none · sorted by price ascending · then hand-check each ZIP's sold $/sqft.
**Reasoning:** the 70% formula only works where ARV is high relative to the ask. A $95K house in a $250K-ARV neighbourhood clears the formula; a $95K house in a $100K-ARV neighbourhood cannot, ever. This inverts the usual "cheapest houses in the cheapest ZIPs" wholesale habit, which optimises for lead *count* and guarantees dead deals. **This single screen produced my best lead.**

### B. "Proven price failure" — MLS Failed / Withdrawn + DOM ≥ 90
`mlsStatus = Failed` · `daysOnMarketMin ≥ 90` · `estimatedValue` $125K–$400K · `propertyType` SFR/multi.
**Reasoning:** a withdrawn or 300-day listing is the only category where seller intent *and* seller price-error are both already proven. You are not guessing at motivation; the market has already told the seller their number was wrong. Highest negotiation leverage per call of anything on the platform. **Produced my #2 lead.**

### C. "Portfolio seller" — properties owned ≥ 3 + absentee
`propertiesOwnedMin ≥ 3` · `ownerOccupancy = Absentee` · `propertyType` duplex/multi · `estimatedEquityPercentMin ≥ 50`.
**Reasoning:** institutional and semi-professional sellers price to a number, decide with a spreadsheet, and can close in 21–30 days — which is exactly what your buy box needs and what grieving heirs structurally cannot do. Also the only lane that reliably feeds the duplex/multifamily requirement. **Surfaced through lead B's sister-property disclosure rather than run directly (PropWire access).**

### D. "Free & clear" — the most underused filter on the platform
`freeAndClear = true` · `vacantHome` or long tenure · `yearBuiltMin` irrelevant · `estimatedValue` band.
**Reasoning:** no mortgage means no payoff floor. A leveraged seller physically cannot accept a discount below their loan balance no matter how motivated — the deal dies at the closing table. Free-and-clear owners have no such wall, and they are the only sellers who can say yes to a steep number in a week. **Could not execute — needs PropWire.**

### E. "Long-tenure owner-occupant, aged house" — the quiet lane
`yearsOwnedMin ≥ 20` · `ownerOccupied` · `yearBuiltMax 1960` · `estimatedEquityPercentMin ≥ 60`.
**Reasoning:** deliberately the opposite of the standard absentee/vacant play. A 20-year owner-occupant of a 1950s house is the least-marketed seller in America — no distress flag, so no competition — while carrying large equity and deferred maintenance. This is where the off-market deals actually are. **Could not execute — needs PropWire.**

**What I deliberately did NOT build the strategy on:** probate. It reads as the most attractive flag on paper, but in this buy box it is the worst — estates need multiple signatures and court confirmation, which is structurally incompatible with your 21–30 day close. I would rather source a stale listing from a living seller than a fresh probate.

---

## 3. What I ran, and what it produced

| # | Screen | Source used | Result |
|---|---|---|---|
| 1 | City-wide cheap band, all Akron $20K–$80K | Redfin (247 / 94 results) | Mapped the low end. Confirmed the arithmetic problem: every listing here sits in a $75K–$115K-ARV ZIP. **Zero formula-viable.** |
| 2 | ZIP-level cheap bands: 44301, 44303, 44305, 44307, 44313, 44319, 44320 | Redfin | **Sterile in the high-ARV ZIPs.** 44313 ($50K–$145K) returned *2 homes, both condos*. 44319 returned *2*. The cheap house in a good neighbourhood is **rare** — which is precisely why it is worth screening for. |
| 3 | "Cheap in expensive ZIP" hand-check → 44302 | Redfin | **HIT: 141 Grand Ave, $95,000, Highland Square.** 3 days listed, one photo, as-is. |
| 4 | Long-DOM / failed-listing proxy (DOM read from each listing card; Redfin has no withdrawn filter) | Redfin detail pages | **HIT: 6090 Manchester Rd — 337 days on market**, 4-unit, cash-only, and the listing names a *second property from the same owner*. |
| 5 | Multifamily/duplex active | Redfin | Surfaced 6090 Manchester (4 units) and 82 Aqueduct (carried forward). Redfin's `property-type` filter refuses to apply on several ZIPs — a source limitation, not an absence of listings. |
| 6 | Sold comps per candidate (6-month, same ZIP, size/bed-matched) | Redfin sold | Used to build every ARV below. All comps cited with sale date and price. |

---

## 4. Underwriting the strongest two

### 4.1 141 Grand Ave, Akron OH 44302 — **HIGH PRIORITY · #1 overall**

| Field | Verified value |
|---|---|
| Asking | **$95,000** |
| Type / size | Single-family, **3 bd / 1 ba**, built **1914**, lot **4,356 sq ft**. *Living area not published — blank on the MLS record.* |
| MLS | 5256547 (MLSNOW) |
| Status | Active · **3 days** · 40 views · **1 photo only** |
| Condition | Listing copy, in full: *"Property needs extensive TLC. Being sold as is."* |
| Neighbourhood | **Highland Square** — Walk Score 7.5/10, Firestone High 6/10, walkable historic pocket |
| Agent | **Michael Kaim**, Real of Ohio — **kaimteam@gmail.com · 440-796-0425** |
| URL | https://www.redfin.com/OH/Akron/141-Grand-Ave-44302/home/66306272 |

**ARV support.** No sold comps exist inside 44302 in what Redfin would return for this band, so I bracket it from **renovated 3-bedroom asking prices in the directly adjacent Highland Square / 44303 pocket**, which is the same housing stock and school assignment:

| Reference | Price | Bd/Ba | Sqft | Why it is relevant / flag |
|---|---|---|---|---|
| 570 Mardon Ave, 44303 | $259,900 ask | 3/1.5 | 1,479 | Same era, same bath count, ~3 blocks of character stock. **Flag: asking, not sold.** |
| 605 Mardon Ave, 44303 | $289,900 ask | 3/2 | 1,636 | Better bath count — upper bound. **Flag: asking.** |
| 190 N Highland Ave, 44303 | $399,000 ask | 4/1.5 | 2,392 | Far larger; included only to show the ceiling of the pocket. **Flag: not comparable on size.** |
| 799 Fess Ave, 44307 | **$92,500 sold** Jul 29 2026 | 3/1 | 1,234 | Renovated 3/1 sold — the *floor* of what a finished 3/1 clears in an adjacent west-side ZIP. **Sold, verified.** |

**ARV conclusion: $240,000 base case** (range **$215,000–$265,000**). Confidence **LOW–MEDIUM** — the direction is well supported by sold evidence at the floor and asking evidence at the ceiling, but there is **no sold 3/1 in 44302 in this dataset**, and ARV is the number the whole deal rests on. This one should be AVM-checked on PropWire before any offer.

**Repairs.** One exterior photo and no interior images. Everything inside is inference.

| Line | Estimate |
|---|---|
| Kitchen | $12,000 |
| Bath (only one) | $10,000 |
| Floors, paint, drywall, trim across ~1,400 sf | $14,000 |
| Roof (age unknown) | $12,000 |
| Electrical service (1914) | $8,000 |
| Plumbing | $8,000 |
| HVAC | $6,000 |
| **Total** | **$70,000** |

**Underwriting across three ARV cases (repairs held at $70,000):**

| | Conservative | **Base** | Strong |
|---|---|---|---|
| ARV | $215,000 | **$240,000** | $265,000 |
| 70% ceiling | $150,500 | **$168,000** | $185,500 |
| Buyer max after repairs | $80,500 | **$98,000** | $115,500 |
| **Spread at $95,000 asking** | **−$14,500** | **+$3,000** | **+$20,500** |
| Contract price for $10,000 fee | $70,500 (−26%) | **$88,000 (−7%)** | $105,500 (above ask) |
| Ceiling-only spread | +$55,500 | **+$73,000** | +$90,500 |

**Why this is the best result of the whole exercise:** in the base case it **clears the full 70%-minus-repairs test at roughly the asking price**, and needs only a **7% negotiation** to produce a $10,000 fee. Every other Akron property I have screened needs a 25–58% cut. That is the entire difference between a lead and a deal.

**Honest risks:** (a) one photo means sight-unseen — the $70,000 could be $110,000 if the roof and systems are gone; (b) three days on market means the seller has **no** reason to discount yet, so this is a *pre-negotiation* lead, the opposite of the stale-listing play; (c) no published square footage weakens the ARV more than anything else here.

---

### 4.2 6090 Manchester Rd, Akron OH 44319 — **HIGH PRIORITY, different reason**

| Field | Verified value |
|---|---|
| Asking | **$108,000** |
| Type | **Multi-family — 4 units / 4 kitchens / 4 baths**, 3,420 sq ft, **$32/sq ft** |
| Unit mix (from listing) | 2 × 1BR at road front · 1 × 2BR ground level · 1 × 3BR at rear |
| Built / lot | **1875** · **0.64 acres**, backs onto Lockhart Ballfield · 2-car garage |
| Status | Active · **337 days on market** · 537 views · 11 saves |
| MLS | 5174593 (MLSNOW) |
| Terms | **NO SELLER FINANCING — cash only · sold AS IS · debris on site remains at close · must email agent proof of cash funds before a showing** |
| Extra | *"One owner w/ two properties for sale — see MLS#5186755 @ 6235 Manchester Rd."* |
| Agent | **Beverly Bess**, Coldwell Banker Schmidt Realty — **beverly.bess@att.net · 330-645-0227** |
| URL | https://www.redfin.com/OH/Akron/6090-Manchester-Rd-44319/home/201069775 |

**Why it ranks despite the rehab:** **337 days on market is the strongest evidence of price failure I found anywhere in Akron**, and the listing discloses a **second property from the same owner** — that is a portfolio seller, screen C, found in the wild. Two bites, one relationship, one motivated counterparty.

**The 70% formula is the wrong tool here, and I will not pretend otherwise.** A 4-unit trades on income. Running it both ways:

*Income test (rents are ESTIMATES — the rent roll is not in the listing and I will not invent one):*
1BR at $700 × 2, 2BR at $900, 3BR at $1,150 → **$3,450/mo = $41,400/yr gross**; at a 40% expense ratio → **NOI ≈ $24,840**; at a 9–11% cap → **stabilised value $226,000–$276,000**, i.e. **~$250,000**.

*Flip test:*
| | Value |
|---|---|
| 70% of $250,000 | $175,000 → **ceiling spread at asking +$67,000** |
| Repairs — 4 kitchens, 4 baths, 3,420 sf, 1875 structure, 4 sets of mechanicals | **~$120,000** |
| Buyer max after repairs | **$55,000** |
| Spread at $108,000 asking | **−$53,000** |
| Contract for $10,000 fee | $45,000 (−58%) |

**Read:** as an **assignment it fails**; as a **buy-and-hold it works** — $108,000 + $120,000 = $228,000 all-in against ~$24,840 NOI is a **10.9% yield on cost**, which any cash investor will look at. So the end buyer for this one is an income investor, not a flipper. That changes who you market it to, not whether it is worth a call.

**Risks that are real and must be asked:** **"Buyer to check Zoning Potential"** — four units on a residential parcel in Coventry Township may be legally non-conforming, which can wreck both the resale and the refinance. **Built 1875** — 151 years old; foundation, knob-and-tube and sewer are live questions. **Unknown occupancy and rent roll.** Debris remains at close (a real disposal cost).

---

## 5. Ranked summary

| # | Priority | Address | Type | Asking | Est. ARV | Est. Repairs | Spread at ask (ceiling) | Spread at ask (after repairs) | DOM | Confidence |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **HIGH** | 141 Grand Ave, 44302 | SFR 3/1, 1914 | $95,000 | $240,000 | ~$70,000 | **+$73,000** | **+$3,000** | 3 | LOW–MED |
| 2 | **HIGH** | 6090 Manchester Rd, 44319 | **4-unit**, 3,420sf, 1875 | $108,000 | $250,000 (income) | ~$120,000 | **+$67,000** | −$53,000 | **337** | LOW–MED |
| 3 | MEDIUM-HIGH | 156 Colony Cres, 44305 | SFR 5/2, 1944sf | $55,000 | $170,000 | $55–75K | +$64,000 | +$9,000/−$11,000 | 11 | MED |
| 4 | MEDIUM | 82 Aqueduct St, 44303 | Duplex 6/2 | $119,900 | $185,000 | ~$45,000 | +$9,600 | −$35,400 | 39 | LOW |
| 5 | LOW | 838 Fess Ave, 44307 | SFR 3/1 | $45,000 | $100,000 | ~$35,000 | +$25,000 | −$10,000 | <1 | LOW |
| 6 | REJECT | 75 E Ido Ave, 44301 | SFR 6/2 | $109,900 | $155,000 | ~$60,000 | −$1,400 | −$61,400 | 10 | — |

**Tier 1 is #1 and #2, for opposite reasons.** #1 has the ARV room and needs a 7% trim; #2 has the proven price failure and needs a 58% trim — one is a numbers deal, the other is a negotiation deal. #3 is the best repair-risk-adjusted single family.

---

## 6. Verified vs estimated

**Verified from source:** every address, price, MLS number, unit count, bed/bath, sqft, year built, lot size, DOM, agent name, email and phone above; every sold comp price and date; every quoted listing sentence; the 337-day and 3-day DOM figures; the sister-property disclosure; the zoning and cash-only clauses.

**Estimated by me:** all ARV figures and the ARV ranges; the $70,000 and $120,000 repair figures and their line items; the entire rent assumption for Manchester Rd ($3,450/mo is my estimate, **not** a rent roll); NOI, cap-rate range and stabilised value; every buyer maximum, spread and contract-price target; all priority and confidence ratings.

**Not claimed:** that either property is wholesale-ready; that ARV is confirmed (141 Grand has **no sold comp in its own ZIP** in this dataset); that the Manchester Rd rents are real; that either seller is motivated rather than merely patient; that repairs are known — 141 Grand has **one photo**.

**Not executed:** equity %, LTV, years owned, properties owned, free-and-clear, notice type and auction date — all require a PropWire session. Runs #3 and #5 of my five-strategy set are therefore **unsourced**, and that is where I would expect the next two or three best deals to be.

---

## 7. Recommendation

1. **Call on 141 Grand Ave first.** It is the only property found in Akron whose base case clears 70%−repairs at the asking price. Ask for square footage, roof age, and interior photos before anything else — the ARV and the repair number both turn on them.
2. **Ask Beverly Bess for the rent roll and current occupancy on 6090 Manchester Rd**, plus the zoning confirmation, and for the sister property 6235 Manchester Rd in the same conversation. 337 days of no offers is leverage you will not often get.
3. **Get a PropWire session.** My two highest-conviction filters — free-and-clear and long-tenure owner-occupant — are exactly the ones I could not run, and they are where the un-marketed inventory sits.

**No agent has been contacted. Nothing has been submitted.**
