# Akron — on-market and off-market are two separate books

**2026-10-31. You were right and I had it wrong. Here is exactly what bled across, and what is now enforced.**

---

## 1. Where I mixed them

| What I wrote | Where | The problem |
|---|---|---|
| One ranked list of "corrected leads" with 156 Colony, 838 Fess, 6090 Manchester, 82 Aqueduct, 141 Grand, 75 E Ido | chat, last message | All six are **live listings with asking prices**. I then used that same list to conclude "one property clears in Akron" — as if that were the whole market. |
| "7 of the 13 off-market leads cannot be priced" in the same breath as duplex verdicts for 82 Aqueduct | report §5 | 82 Aqueduct is **on-market** ($119,900 asking). Masters is **off-market** (no asking price). I gave them the same verdict in one table. |
| "Every ARV in the file was rebuilt from Redfin sold comps" sitting next to 141 Grand / 6090 Manchester / 82 Aqueduct | `START HERE` | Those three are **not in the PropWire file**. Naming them in an off-market data-quality row is a bleed. |
| 44303 **asking** prices used to set 141 Grand's ARV | earlier | Asking prices are not comps. Already corrected, but still the root error. |

**And the worst one, found while fixing this:** the off-market list used **44303 comps to price 44302 houses.** `647 Crosby St` is in 44302, 2bd/2ba, 973 sf — I had priced it at $170,000–$200,000 off 44303 *three-bed* sales. The 44303-vs-44302 distinction is the exact thing that killed 141 Grand, and it had quietly corrupted the off-market book too.

---

## 2. The rule, now enforced in the workbook

| | **ON-MARKET** (`ON-MARKET 6`) | **OFF-MARKET** (`OFF-MARKET 13`) |
|---|---|---|
| Has | asking price, DOM, agent, photos, as-is condition, MLS status | owner name, mailing address, tenure, occupancy flag, vacancy flag, county beds/baths/units |
| Does **not** have | — | **no asking price, no DOM, no agent, no MLS status, no condition** |
| Priced by | closed-sale ARV → (ARV × 0.70) − repairs → −$10,000 fee → compare to asking | closed-sale ARV → (ARV × 0.70) − repairs → −$10,000 fee = **max contract ceiling** |
| Can compute | sale-to-list gap, negotiation discount, spread at asking | **neither** — there is no asking price to discount from |
| Purpose | negotiate | dial, with a ceiling in hand |

**ChatARV prices a listing.** So a ChatARV figure belongs to the on-market book only, labelled by source, and is never used as a comp or applied to an owner record.

**Tabs are renamed** so this cannot silently happen again: `ON-MARKET 6 (live listings)`, `OFF-MARKET 13 (owners)`, plus a scope block at the bottom of each.

---

## 3. Off-market corrections forced by the fix

I pulled 2-bed sold data to check the mispriced rows. 44302 sold **one** two-bed home in six months. 44303 sold four and **two were condos.**

| Rank | Property | Was | Now | Why |
|---|---|---|---|---|
| 7 | **647 Crosby St 44302** (2bd/2ba, 973 sf) | ARV $170K–$200K, max contract **$44K–$85K** | ARV **$120K–$135K**, max contract **$9K–$39.5K** | Only 2-bed SFR sold in 44302: **166 Marvin Ave, 2/2, 1,008 sf, $135,457** (5/16/26). Same ZIP, same bath count. |
| 8 | **544 Stratford Ave 44303** (2bd/1ba, 1,150 sf) | ARV $170K–$200K | **UNPRICED** | No 44303 2-bed SFR sold in 6 months. Bracket $65K–$135K is too wide to underwrite. |
| 9 | **283 Gordon Dr 44302** (3bd/1ba) | ARV $120K–$150K, max contract $9K–$50K | ARV **$95K–$115K**, max contract **−$13.5K–$20.5K** | Recut to 44302 3-bed comps only. |
| 13 | **1366 Marcy St 44301** (2-unit, 4bd/2ba) | listed as off-market | **IT IS LISTED — $79,999** | Already on the market. Belongs in the on-market book. It only sat here because the county export has no listing-status field. |

**9 of 13 remain unpriced** — all duplex/triplex, because there is still no sold 2–4 unit in 44302 or 44303 in six months, and 44305 duplexes span $105,000–$241,200.

---

## 4. On-market book, unchanged by this (it was always on-market)

| # | Property | Ask | Comp ARV | Contract | Verdict |
|---|---|---|---|---|---|
| 1 | 156 Colony Cres 44305 | $55,000 | $150,000 | $40–67K | clears at asking if repairs ≤ $40K |
| 2 | 838 Fess Ave 44307 | $45,000 | $105,000 | $21–45K | rental, not an assignment |
| 3 | 6090 Manchester Rd 44319 | $108,000 | UNPRICED | — | no 4-unit comp, no rent roll |
| 4 | 82 Aqueduct St 44303 | $119,900 | $165–195K | $45–81K | needs −32% best case |
| 5 | 141 Grand Ave 44302 | $95,000 | $125,000 | −$8–33K | rejected |
| 6 | 75 E Ido Ave 44301 | $109,900 | $120,000 | $2–26K | rejected |

---

## 5. What I need from you

**Which property was the ChatARV search on?** I want to write its estimated value / equity / MLS status into the on-market row, labelled `ChatARV (you, on-market)` — a separate column from my comp-derived ARV, so the two never blur again. I am not going to guess which one.

**And say the word if 1366 Marcy should move** to the on-market tab at its $79,999 list price.
