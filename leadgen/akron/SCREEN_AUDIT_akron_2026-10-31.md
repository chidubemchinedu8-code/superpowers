# Do the leads in my tabs hold up? — re-running both screens

**2026-10-31. Direct answer: the properties are real, but the lists were not complete, and I can name exactly what I dropped.**

---

## Short answer first

| Question | Answer |
|---|---|
| Are the on-market leads real? | **Yes.** All 6 are live listings with verified asking prices, agents and phone numbers. 3 of them are already rejected on the numbers and kept as documentation. |
| Are the off-market leads real? | **11 of 13 yes. 1 doesn't belong (1366 Marcy — it's listed). 1 has no signal (544 Stratford).** |
| Did my mistakes wrongly exclude leads? | **Yes — but not the ARV mistakes.** The ARV errors caused *over*-inclusion, not exclusion. The exclusions came from **three screen rules I chose**, and they dropped **584 rows**, including two that would rank #2 and #3. |
| Is either list a complete sweep? | **No.** Neither is. Details below. |

---

## 1. What I re-ran

The off-market screen was: `ZIP in (44302, 44303)` → `individual owner` → `tenure >= 120 months` → `AND (vacant OR absentee OR multi-unit)`.

Re-running it exactly reproduces **14** candidates, not 13. Two in my tab are accounted for differently:

| Property | Status after audit |
|---|---|
| **1366 Marcy St 44301** | **Does not belong.** It's listed at $79,999. It entered via a Redfin search, not the screen. -> on-market. |
| **544 Stratford Ave 44303** | **In the tab, but fails the signal bar.** 282 months owned, but owner-occupant, 1 unit, not vacant, not absentee. Valid property, **no distress signal**. |

And two that should have been there **and weren't**:

| Property | Zestimate | Rent est | **Ceiling @ $0 repairs** | Why I missed it |
|---|---|---|---|---|
| **119 Oakdale Ave 44302** | **$142,600** | **$1,935** | **$89,820** | Vacant 3-unit, 172 months. Skipped on the first pass. **Highest rent on the entire list.** |
| **268 Alhambra Way 44302** | **$121,100** | $1,547 | **$74,770** | 2 units, 210 months. Skipped on the first pass. |

**119 Oakdale would have ranked #2 and 268 Alhambra #3 by ceiling.** Both are now rows 15 and 16. Tab renamed `OFF-MARKET 15 (owners)`.

---

## 2. What the screen rules cost me — measured

| Exclusion rule | Rows dropped | What it contains | Verdict |
|---|---|---|---|
| **ZIP limited to 44302 + 44303** | **512** | Individual owners with the *identical* signal bar in other Akron ZIPs: 44306 (110), 44310 (80), 44314 (70), 44320 (64), **44301 (42), 44307 (40), 44305 (33), 44311 (36)** | **The real problem.** See §3. |
| **Entity-owned excluded** | **26** | 44302/44303 LLC/trust-owned with real signals — incl. **233 Crosby St LLC, 3 units, 227 months**; **277 Crosby St LLC, 3 units, 142 months**; **168 Westwood Ave trust, vacant, 320 months**; **341 Silver St Inc, vacant, 203 months** | Defensible for *dialing*, wrong for *sourcing*. They price off a spreadsheet but they still sell. |
| **Tenure >= 120 months** | **46** | Individual owners in 44302/44303 with vacancy or absenteeism who bought inside 10 years | A recent purchase is not "no signal" — it's often a landlord who just overpaid and wants out. |

**Total dropped by screen design: 584 rows.** Two of them sat in the population I *did* screen, so that part is a sorting bug, not a scope choice.

---

## 3. The inconsistency that matters most

My **on-market** leads come from **44305, 44307, 44301, 44319**.
My **off-market** screen only covered **44302, 44303**.

So I was hunting live deals in ZIPs I had explicitly excluded from the owner search. In those excluded ZIPs sit **151** individual owners with the same signal (44301 42 + 44307 40 + 44305 33 + 44311 36). That is the single biggest hole, and it's mine.

It explains something that looked like a coincidence: 156 Colony (44305) and 838 Fess (44307) are my two best on-market leads, and both are in ZIPs the off-market screen never touched.

---

## 4. The ARV mistakes ran the other way

Worth stating plainly, because it's the opposite of what you'd assume:

- I **over**-valued properties (44303 asking prices used on 44302 houses; 44305 sales used to bracket duplexes).
- Over-valuing **inflates** the 70% ceiling, which makes **more** deals look workable.
- So those errors produced **false positives**, not false negatives.

Every correction since has made the lists **shorter or lower**, never longer. The two leads recovered this pass were missed by **logic**, not by valuation.

---

## 5. On-market: valid leads, incomplete sweep

All 6 are real. But the search that produced them was ad-hoc — specific bed counts and price caps on specific ZIPs:

| What I searched | What it returned |
|---|---|
| Redfin 44305, 5+ beds | 156 Colony |
| Redfin 44307, <= $85,000 | 838 Fess |
| Redfin 44303 | 82 Aqueduct |
| Redfin 44302 / 44319 / 44313 | 141 Grand, 6090 Manchester, 75 E Ido |

**I never swept all Akron active listings under a price cap.** Zillow alone reports **25 active listings in 44302** and **27 in 44303**. I looked at a handful. So the on-market tab is **6 properties I happened to find**, not "the 6 best in Akron."

---

## 6. What I recommend, in order

1. **Re-screen 44301, 44305, 44307, 44311 at the same signal bar** — 151 individual owners, in the ZIPs where my on-market leads actually cleared. Highest-value next step.
2. **Add the 26 entity-owned 44302/44303 rows as a separate "portfolio" bucket** — not for cold-dialing, but one letter to an LLC holding 3 units on Crosby beats five cold calls.
3. **Test the 46 recent-buyer rows** against purchase prices — a landlord who bought at the top is a different conversation.
4. **Do a proper Akron-wide active-listing sweep** with a price cap, instead of the ad-hoc Redfin queries.

**Say which you want and I'll run it.** I'm not going to silently expand the list again — that's what caused this.

---

## 7. Standing caveats

- Every value on both tabs is an estimate. Nothing is an offer.
- Zestimate is automated, not an appraisal, and knows nothing about condition.
- No MLS access. Zillow cites MLS Now and prints MLS numbers on closed sales.
- Nothing contacted, nothing submitted, no contract.
