# On-Market Acquisition Screen — Akron, OH
**Prepared:** 2026-10-31 · **Market:** Akron (Summit County), OH only · **Buyer:** RealVenture
**Formula used:** Buyer Maximum = (ARV × 0.70) − Estimated Repairs · Fee target $10,000 whole

---

## 1. Access and method (read this before the numbers)

**Sources actually accessed:**

| Source | Result |
|---|---|
| Redfin (city, ZIP and sold filters) | **Worked.** Active listings, sold comps, detail pages with MLS#, DOM, agent name, email, phone. |
| Redfin detail pages (property record) | **Worked.** Gave property type, year built, lot, sqft, agent contact, DOM, view count. |
| Howard Hanna search results | **Partial.** Its search-page result summaries appeared in web search results; the live page returned a client-side "blocked by an extension" error and could not be read directly. |
| Zillow | **Failed to filter.** The page rendered but every filter URL (`/25000-115000_price/`) returned the same 906 unfiltered results. Not used for numbers. |

**Not available, therefore not used:**

- **Summit County Fiscal Office / auditor records** — no parcel, tax, or deed verification.
- **Interior access, inspection, or contractor bids** — all repair figures below are ESTIMATES from listing copy and photo counts.
- **Original list price / price-reduction history** — Redfin's sale-and-tax history section did not appear in the fetched content. **Days on market is verified; price history is NOT.** No price-reduction claim is made anywhere in this report.
- **Redfin's multifamily sold filter would not apply to ZIP 44303.** Every attempt returned all 14 active homes. So there is **no duplex sold comp inside 44303**, and 82 Aqueduct's ARV is inferred from duplex sales in 44305/44301. Marked LOW confidence.

I did **not** contact any agent, and I have not submitted anything.

---

## 2. The finding that governs this whole exercise

**Akron's on-market asking prices do not produce a spread under 70% − repairs.**

Here is the arithmetic that drives it. Akron's median sale price is reported at **$193,185** (Howard Hanna market page), but the inventory that fits your $125K+ ARV screen sits in neighbourhoods where **renovated retail is $100,000–$170,000** and a heavy rehab on a 1,900 sqft 1919 house runs **$55,000–$80,000**. At those numbers:

> ARV $155,000 → 70% ceiling $108,500 → minus $60,000 repairs = **$48,500 buyer maximum.**
> That is 31% of ARV. No retail seller lists at 31% of ARV.

So the 70%-minus-repairs test is **structurally incompatible with most of Akron's listed inventory.** It only produces a positive spread in two situations:

1. **The ceiling test alone** (70% of ARV, repairs unknown) — which is how your own Cuyahoga file was built, labelled `CEILING ONLY`. On that basis several Akron listings *are* positive.
2. **A deep discount on a stale, as-is or estate listing** — the seller is already at or below 60% of ARV and rehab is light.

I show both tests for every property, because pretending the repair-adjusted number works when it doesn't is how a list gets built that no buyer will fund.

**Practical read:** in Akron the workable buyer band is closer to **78–85% of ARV on light-rehab deals**, not 70% minus full repairs. Either the 70% is a ceiling-before-repairs number, or Akron needs a different buyer. That is a decision for you, not something I should quietly assume.

---

## 3. Ranked table

Repairs are ESTIMATES (visible cosmetic + unknown systems shown separately). Spread is shown **two ways** because the answer flips.

| # | Priority | Address | Type | Asking | Est. ARV | Est. Repairs | Buyer max (70%−repairs) | Spread at asking — **ceiling only** | Spread at asking — **after repairs** | DOM | Main signal | Confidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **HIGH** | 156 Colony Cres, 44305 | SFR 5bd/2ba 1,944sf 1919 | $55,000 | $170,000 | $55k–75k | $44,000–$64,000 | **+$64,000** | +$9,000 to −$11,000 | 11 | Estate sale, as-is, cash only, "good ARV value" | MEDIUM |
| 2 | **MEDIUM** | 82 Aqueduct St, 44303 | Duplex 6bd/2ba 2,521sf 1913 | $119,900 | $185,000 | ~$45,000 | $84,500 | **+$9,600** | −$35,400 | 39 | 39 DOM, sold as-is, Highland Square edge, 2 full units + 2 finished attics | LOW–MEDIUM |
| 3 | **MEDIUM** | 838 Fess Ave, 44307 | SFR 3bd/1ba 1,393sf 1919 | $45,000 | $100,000 | ~$35,000 | $35,000 | **+$25,000** | −$10,000 | <1 | Cash, vacant, central HVAC already in | LOW |
| 4 | **MEDIUM** | 1364-1366 Marcy St, 44301 | Duplex 4bd/2ba 1,728sf | $79,999 | $140,000 | ~$45,000 | $53,000 | **+$18,000** | −$27,000 | n/a | Two-unit at a single-family price | LOW |
| 5 | LOW | 372 N Firestone Blvd, 44301 | SFR 5bd/1ba 1,717sf | $99,900 | $150,000 | ~$60,000 | $45,000 | +$5,100 | −$54,900 | n/a | 5bd at $100k, original woodwork | LOW |
| 6 | LOW | 238 Para Ave, 44305 | SFR 4bd/1ba 1,669sf | $110,000 | $155,000 | ~$50,000 | $58,500 | −$1,500 | −$51,500 | n/a | Back on market, seller did repairs | LOW |
| 7 | **REJECT** | 75 E Ido Ave, 44301 | SFR 6bd/2ba 1,848sf 1918 | $109,900 | $155,000 | ~$60,000 | $48,500 | −$1,400 | −$61,400 | 10 | As-is, rented $1,281/mo | — |
| 8 | **REJECT** | 404 other active Akron listings | — | — | — | — | — | — | — | — | See §2: above 70% of ARV before repairs | — |

**Required contract price to clear a $10,000 fee** (contract = buyer max − $10,000):

| Property | Contract needed @ heavy repairs | Contract needed @ light repairs | Discount from asking |
|---|---|---|---|
| 156 Colony Cres | $34,000 | $54,000 | −38% to −2% |
| 82 Aqueduct St | $74,500 | $94,500 | −38% to −21% |
| 838 Fess Ave | $25,000 | $38,000 | −44% to −16% |
| 1364-1366 Marcy St | $43,000 | $58,000 | −46% to −27% |

---

## 4. Detailed analysis — the three worth a call

### 4.1 156 Colony Cres, Akron OH 44305 — **HIGH PRIORITY** (the only genuine one)

| Field | Value |
|---|---|
| Asking | **$55,000** |
| Type / size | Single-family, 5 bd / 2 ba, **1,944 sq ft**, built **1919**, lot 8,799 sq ft |
| Status | Active · **11 days** on Redfin · 146 views · 4 saves |
| MLS | 5254354 (MLSNOW) |
| Listing url | https://www.redfin.com/OH/Akron/156-Colony-Cres-44305/home/66102182 |
| Listing agent | **Jose Medina**, Keller Williams Legacy Group Realty |
| Contact | **jose@josesellshomes.com · 330-595-9811** |
| Signal | *"This home is being sold to settle an Estate… needs a lot of TLC and updating… AS-IS Sale. Cash offers only. Good ARV value."* New furnace approx. 2 yrs, newer water heater 2022. |

**Verified sold comps (all within ~1.5 mi, all sold within 6 months):**

| Comp | Sold | Price | Bd/Ba | Sqft | $/sqft | Why relevant / flags |
|---|---|---|---|---|---|---|
| 1115 Eastland Ave, 44305 | Oct 16 2026 | $164,000 | 4/2 | 1,136 | $144 | Same ZIP, same era, double lot, well maintained. **Flag:** much smaller, better condition — upper bound only. |
| 470 Sumatra Ave, 44305 | 2026 | $161,600 | 3/2 | 1,617 | $100 | Closest size match to a renovated 5bd. Strongest ARV anchor. |
| 2211 Goodyear Blvd, 44305 | 2026 | $135,000 | 3/1 | 1,372 | $98 | Same Goodyear Heights neighbourhood, average condition. |
| 840 E Buchtel Ave, 44305 | Sep 21 2026 | $144,800 | 6/2 | 1,728 | $84 | Same bed count. **FLAG — unreliable:** listing states *"Sale restricted to owner occupants at or less than 80% AMI."* A deed-restricted sale is **not** an open-market comp; use as a floor only. |
| 81 Cotter Ave, 44305 | Aug 6 2026 | $126,000 | 4/2 | 1,478 | $85 | Fully renovated. Shows the low end of what a renovated 4/2 actually clears here. |

**ARV conclusion:** $170,000 (range $160,000–$180,000) for a fully renovated 5bd/2ba 1,944 sqft. Confidence **MEDIUM** — five sold comps, tight geography, but the $/sqft spread across them is wide ($84–$144) and the AMI-restricted sale drags the low end.

**Repairs — visible vs unknown:**

| Visible from listing | Estimate |
|---|---|
| Kitchen — full replacement | $12,000 |
| 2 full baths | $14,000 |
| Paint, drywall, flooring throughout 1,944 sf | $12,000 |
| Exterior, porch, garage, landscaping | $5,000 |
| **Visible subtotal** | **$43,000** |
| Unknown / inspection-dependent: roof, electrical service, plumbing, windows, basement | $12,000–$32,000 |
| Contingency (already inside the range) | — |
| **Total range** | **$55,000–$75,000** |

New furnace (~2 yrs) and 2022 water heater remove the two biggest mechanical unknowns — that is what makes the moderate case credible.

**The two underwriting cases:**

| | Moderate ($55k repairs) | Heavy ($75k repairs) |
|---|---|---|
| ARV | $170,000 | $170,000 |
| 70% ceiling | $119,000 | $119,000 |
| Buyer max after repairs | **$64,000** | **$44,000** |
| Spread at $55,000 asking | **+$9,000** | −$11,000 |
| Contract for $10,000 fee | $54,000 | $34,000 |

**Read:** this works at roughly **the current asking price** if repairs land near $55,000. It does not work if the roof, electrical and plumbing are all gone. **The entire deal hinges on one number you don't have — the rehab scope.** That is the first thing to establish, before any offer conversation.

**Not wholesale-ready yet.** It is a legitimate candidate to *investigate*, nothing more.

---

### 4.2 82 Aqueduct St, Akron OH 44303 — **MEDIUM PRIORITY**

| Field | Value |
|---|---|
| Asking | **$119,900** |
| Type / size | **Multi-family (duplex)**, 6 bd / 2 ba total, **2,521 sq ft**, built **1913**, lot 1,742 sq ft |
| Layout | Two 3bd/1ba units, **each with a full finished attic** |
| Status | Active · **39 days** on Redfin · 156 views · 9 saves |
| MLS | 5246860 (MLSNOW) |
| Listing url | https://www.redfin.com/OH/Akron/82-Aqueduct-St-44303/home/100652422 |
| Listing agent | **Jennifer Bernzweig**, Century 21 Homestar |
| Contact | **berzweigjennifer@gmail.com · 330-328-9711** |
| Signal | *"Sold as is."* Near Highland Square / downtown / University. Newer windows (2012), some flooring, **one** furnace replaced 2024 (the other is unspecified age). |

**Comps — and an honest gap:**

There are **no duplex sold comps inside 44303** — Redfin's multifamily sold filter would not apply to that ZIP, and I will not invent one. Nearest usable duplex sales:

| Comp | Sold | Price | Bd/Ba | Sqft | Why relevant / flags |
|---|---|---|---|---|---|
| 280 Cluster Ave, 44305 | May 19 2026 | $184,000 | 4/2 | 1,440 | Brick 2-unit, Ellet. **Flag:** different ZIP, ~5 mi, smaller. |
| 325 Para Ave, 44305 | May 22 2026 | $125,000 | 4/2 | 1,512 | Fully renovated duplex. **Flag:** renovated, so a floor not a ceiling. |
| 52 E Brookside Ave, 44301 | Jul 28 2026 | $117,500 | 6/2 | 1,804 | Two occupied units, 6bd — best structural match. **Flag:** Firestone Park, not 44303. |
| 1224 Pondview Ave, 44305 | Jun 5 2026 | $190,000 | 4/4 | 2,256 | **Flag: four-unit**, not a duplex. Included only to bracket the top of the range. |

**ARV conclusion:** $185,000 (range $175,000–$200,000). Confidence **LOW** — no same-ZIP duplex sale, and the Highland Square adjacency is an inference from the listing description, not a measured premium.

**Repairs:** ~$25,000 visible (2 kitchens partial, 2 baths, paint/floor across 2,521 sf, attics) **+ $20,000 unknown** (second furnace, roof, electrical, plumbing in a 1913 building) = **~$45,000**. Two-unit mechanicals are the risk; the 2024 furnace helps one side only.

| | Case |
|---|---|
| 70% ceiling | $129,500 → spread at asking **+$9,600** |
| After $45,000 repairs | Buyer max **$84,500** → spread **−$35,400** |
| Contract for $10,000 fee | **$74,500** (−38%) |

**Read:** at the ceiling test it is marginally positive. At the repair-adjusted test it needs a **38% cut**, which a listing that has only been up 39 days is unlikely to take. Worth a conversation *only* to test flexibility — it is not a deal at $119,900.

---

### 4.3 838 Fess Ave, Akron OH 44307 — **MEDIUM PRIORITY**

| Field | Value |
|---|---|
| Asking | **$45,000** |
| Type / size | Single-family, 3 bd / 1 ba, **1,393 sq ft**, built **1919**, lot 4,948 sq ft |
| Status | Active · listed **less than 24 hours** at time of capture · 39 views |
| MLS | 5257511 (MLSNOW) |
| Listing url | https://www.redfin.com/OH/Akron/838-Fess-Ave-44307/home/75474775 |
| Listing agent | **Jeffrey Schultheis**, Red 1 Realty, LLC |
| Contact | **Jeff@JSREALTORTEAM.com · 419-295-6771** |
| Signal | *"Cash purchase, vacant… blank canvas."* **Central forced-air gas heat and central A/C already installed.** 7-room plan, full basement, wood siding, asphalt roof. |

**Sold comps:**

| Comp | Sold | Price | Bd/Ba | Sqft | Why relevant / flags |
|---|---|---|---|---|---|
| 799 Fess Ave, 44307 | Jul 29 2026 | $92,500 | 3/1 | 1,234 | **Same street**, same bed/bath, fully renovated. The single best comp here. |
| 483 Douglas St, 44307 | Sep 23 2026 | $110,000 | 4/1 | 1,373 | Fully renovated, same ZIP. |
| 1331 Sunrise Dr, 44307 | Jul 10 2026 | $98,000 | 3/1.5 | 1,075 | Renovated, smaller. |
| 1012 Brown St, 44301 | Aug 3 2026 | $101,000 | 4/2 | 1,518 | Light refresh only — shows what a *non*-gutted house clears. |

**ARV conclusion:** $100,000 (range $95,000–$108,000). Confidence **LOW** — good street-level comp, but 44307 renovated sales cluster in a narrow $92k–$110k band, so there is little upside if the rehab is good.

**Repairs:** ~$35,000 total — kitchen $10,000, bath $8,000, paint/floor/drywall $8,000, siding trim + exterior $4,000, unknowns (roof, windows, electrical) $5,000. Existing central HVAC is the reason this is not a $50,000+ job.

| | Case |
|---|---|
| 70% ceiling | $70,000 → spread at asking **+$25,000** |
| After $35,000 repairs | Buyer max **$35,000** → spread **−$10,000** |
| Contract for $10,000 fee | **$25,000** (−44%) |

**Read:** the healthiest ceiling spread in the whole screen, and a genuinely vacant cash-only seller — but ARV is too low to absorb rehab plus a fee. This is a *rental* deal at $45,000, not an assignment.

---

## 5. Rejected, with the reason

| Property | Asking | Why rejected |
|---|---|---|
| **75 E Ido Ave, 44301** — 6bd/2ba, 1,848sf, 1918, as-is, rented at $1,281/mo | $109,900 | 70% of a $155,000 ARV is $108,500 — **below the asking price before a dollar of repairs.** Best comp is 52 E Brookside (6bd/2ba, 1,804sf) at **$117,500**; the house is already priced at that level. Contract would have to be **$38,500 (−65%)**. Not a negotiation, a fantasy. Agent if you ever want it: Debbie Ferrante / Jennifer Ranostay, RE/MAX Edge Realty, debbie@debbieferrante.com, 330-958-8394. |
| **372 N Firestone Blvd, 44301** — 5bd/1ba, 1,717sf | $99,900 | Only **one bathroom** for 5 bedrooms caps the renovated buyer pool; ceiling spread +$5,100 evaporates at the first repair. |
| **238 Para Ave, 44305** — 4bd/1ba, 1,669sf | $110,000 | Negative spread even on the ceiling test (−$1,500). Seller has already done repairs and is re-listing, so there is no distress discount to chase. |
| **141 Grand Ave, 44302** — 3bd/1ba, "extensive TLC", as-is | $95,000 | No ARV support found at that price point with that condition. Listing is 3 days old with one photo set and no condition detail — insufficient evidence, not a rejected deal. |
| **Whole $40k–$115k band, 44314 / 44310 / 44306** | $60k–$110k | Renovated retail in Kenmore, North Hill and East Akron clears **$75,000–$115,000**. At 70% minus repairs the buyer maximum is often **below $40,000** — i.e. below what the seller owes in many cases. Also the highest concentration of city violations and vacant/boarded stock, which the listing copy does not disclose. |

---

## 6. Confirmed facts vs estimates

**Verified (from the listing record):** every address, asking price, MLS number, property type, bed/bath count, square footage, year built, lot size, days on market, agent name, agent email and agent phone in §4. Every sold price and sale date in the comp tables. Every quoted listing sentence.

**Estimated (mine, not the seller's, not an appraisal):** all ARV figures; all repair costs; all buyer maximums; all spreads; all contract-price targets; every priority rating and confidence label.

**Explicitly NOT claimed:** that any of these are wholesale-ready; that any seller is motivated; that a price reduction occurred (price history was unavailable); that repairs are known; that the Highland Square premium on Aqueduct is real. No offer has been made and no agent has been contacted.

---

## 7. What would change the answer

1. **Decide what 70% means.** If 70% is a *ceiling before repairs* (as in your Cuyahoga file), Akron has 4 live candidates. If it is *70% minus full repairs*, Akron on-market produces **zero** workable deals today and the constraint is the formula, not the market.
2. **Get a repair scope on 156 Colony Cres.** One walkthrough decides whether Property #1 is a $9,000 spread or a $11,000 loss. Nothing else in this report is as leveraged.
3. **Summit County auditor pull** on the four shortlisted parcels — delinquent tax, prior sale price, deed history. I could not reach it from here.
4. **Repeat this screen against REO and HUD inventory**, not MLS retail. The estate and REO lanes are where Akron's 60%-of-ARV sellers actually are.

**Awaiting your approval before anything is sent to any agent.**
