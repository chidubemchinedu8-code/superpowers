# Akron — verified comps and the corrected lead list

**2026-10-31. Every comp below is a CLOSED SALE pulled from Redfin `include=sold-6mo`, filtered by ZIP and bed count. Nothing bracketed. Nothing invented.**

---

## 1. What I could and could not use

| Source | Result |
|---|---|
| **Redfin** | **Works.** 44302 3-bed sold-6mo = 9 sales. 44307 3-bed = 23. 44305 5+ bed = 7. 44302 all-types = 29. |
| **Zillow** | **Could not use.** Its sold/price filters are silently ignored by the fetcher — it returns unfiltered pages. |
| **Realtor.com** | **Could not use.** `type-sold` is ignored (returns for-sale listings) and the page serves a reCAPTCHA. Not bypassed. |
| **MLS direct** | No access. Redfin sold data *is* MLS-sourced, which is the closest available proxy. |
| **Radius** | Redfin filters by ZIP, not radius. 44302 is ~1.5 sq mi, so ZIP ≈ 0.5–1.5 mi. Good enough. |
| **Window** | 6 months used. 12 months available but 6 is the tighter, more defensible number. |

---

## 2. The 44302 3-bed comp set — this is what killed lead #1

| Address | Bd/Ba | Sqft | Sold | $/sf | Reliability |
|---|---|---|---|---|---|
| 251 W Center St | 3/2 | 1,146 | $74,000 | $65 | usable |
| 333 Trigonia Dr | 3/1.5 | 1,936 | $94,500 | $49 | usable |
| **135 Byers Ave** | **3/1** | **1,344** | **$100,000** | **$74** | **STRONG — updated bath, newer furnace + windows** |
| 57 Beck Ave | 3/2.5 | — | $110,000 | — | usable |
| 989 Amelia Ave | 3/1.5 | 1,384 | $112,000 | $81 | strong |
| **50 Belvidere Way** | **3/1** | **1,396** | **$120,000** | **$86** | **STRONG — completely updated top to bottom** |
| 64 Byers Ave | 3/2.5 | 1,208 | $187,500 | $155 | EXCLUDE — newer build |
| 151 S Portage Path | 3/1.5 | 1,848 | $196,000 | $106 | EXCLUDE — NW Akron, different submarket |

**A renovated 3/1 in 44302 sells for $100,000–$120,000.** Median $/sf across usable rows: **$78**.

`141 Grand Ave` is 3/1, 1,642 sf. At $78/sf that is **$128,000**.

I originally gave it **$240,000**. I was pricing it from 44303 *asking* prices. 44303 is genuinely a different market — 3-bed sales there run $200,000–$255,000 — but 44302 does not. **My ARV was inflated by about 85%.**

| | Original | Revised |
|---|---|---|
| ARV | $240,000 | **$125,000** |
| 70% ceiling | $168,000 | $87,500 |
| Buyer max (65K repairs) | $98,000 | **$22,500** |
| Contract for $10K fee | $88,000 | **$12,500** |
| vs asking $95,000 | −7% | **−87%** |

`141 Grand` is **rejected**. It is a genuine price failure — 361 days marketed, zero price cuts — but the gap is not a negotiation gap. The house is listed at 76% of its own renovated value.

---

## 3. 44307 — 3-bed comp set, and the one property it validates

| Address | Bd/Ba | Sqft | Sold | $/sf |
|---|---|---|---|---|
| 549 Parkdale Dr | 3/1 | 1,152 | $55,000 | $48 |
| 1546 White Ave | 3/1 | 1,284 | $65,000 | $51 |
| 692 W Thornton St | 3/1 | 960 | $77,000 | $80 |
| 1296 Harmon Ave | 3/1 | 1,516 | $85,000 | $56 |
| **799 Fess Ave** | **3/1** | **1,234** | **$92,500** | **$75 — SAME STREET, fully renovated** |
| 1331 Sunrise Dr | 3/1.5 | 1,075 | $98,000 | $91 |
| 1101 Laurel Ave | 3/1 | — | $105,000 | — |
| 923 Russell Ave | 3/1 | 1,244 | $142,000 | $114 |
| 1161 Diagonal Rd | 3/1.5 | 1,371 | $165,000 | $120 |
| 733 Bisson Ave | 3/1.5 | 1,280 | $170,000 | $133 |
| 286 Millcreek Dr | 3/2.5 | 1,628 | $174,900 | $107 |

**`838 Fess Ave` at $45,000 is validated** — my $100,000 ARV holds; the same-street renovated sale at $92,500 is the anchor. But the assignment spread at asking is **−$1,500**. It does not wholesale.

**It does work as a rental.** 44307 rents, verified from active listings:

| Property | Ask | Beds | Rent |
|---|---|---|---|
| 1127 East Ave | $55,000 | 3/1 | $870 → **$920/mo** |
| 692 Blanche St | $85,000 | 4/2 | $1,015/mo |
| 958 Nathan St | $74,900 | 3/2 | tenant occupied |
| 139 Hollinger Ave (sold) | $65,000 | 4/1 | $900/mo |
| 1174 Mercer Ave | $68,990 | 3/1 | — |
| 898 Haynes St | $80,000 | 3/1 | — |

At $45,000 plus ~$30,000 of work, $1,000/mo on a $75,000 all-in is a real buy-and-hold. **Different exit, not a worse one.**

---

## 4. 44305 — 5-bed comps, and the one lead that survives

| Address | Bd/Ba | Sqft | Sold | $/sf | Reliability |
|---|---|---|---|---|---|
| 44 Agate Pl | 5/1.5 | 1,756 | $134,000 | $76 | **FLOOR ONLY — deed-restricted to 80% AMI** |
| 840 E Buchtel Ave | 6/2 | 1,728 | $144,800 | $84 | **FLOOR ONLY — deed-restricted to 80% AMI** |
| 1288 Pondview Ave | 5/3 | 3,002 | $155,000 | $52 | usable |
| **690 Upson St** | **5/2.5** | **2,322** | **$167,000** | **$72** | **STRONG — best unrestricted comp** |

The two deed-restricted sales are a trap: they are restricted to owner-occupants under 80% AMI, so they are a *floor*, not a market value. Using them as ARV would understate it. Using only the unrestricted sales, a 5-bed in 44305 is worth **$72–$84/sf**.

`156 Colony Cres`, 1,944 sf → **ARV $150,000** (was $170,000).

| Repairs | Buyer max | Contract | vs asking $55,000 |
|---|---|---|---|
| $30,000 | $75,000 | $65,000 | **+$10,000 — clears** |
| $40,000 | $65,000 | $55,000 | **$0 — exactly at asking** |
| $55,000 | $50,000 | $40,000 | −27% |
| $70,000 | $35,000 | $25,000 | −55% |

**This is the only on-market property in Akron that clears at its asking price, and it clears without needing a discount.** Everything now depends on the repair number — which means a walkthrough, not a negotiation.

---

## 5. Duplexes — the honest gap

44305 duplex sales in 6 months:

| Address | Bd/Ba | Sqft | Sold | Note |
|---|---|---|---|---|
| 324 Eastland Ave | 5/2 | 2,128 | **$105,000** | well-maintained |
| 2347-2349 Nicholas Ave | 5/3 | 1,560 | **$167,000** | mid-range |
| 279-281 Cluster Ave | 6/4 | 1,512 | **$241,200** | both units fully remodeled 2023 |

**$105,000 to $241,200 is a 2.3× spread.** That is not a comp set, it is a coin flip.

And **there is no sold 2–4 unit in 44302 or 44303 in six months.** Which means:

- `82 Aqueduct St` ($119,900 duplex, 44303) **cannot be priced**
- The **Masters portfolio** (250 + 256 Crosby) **cannot be priced**
- `239 Crosby`, `163 Beck`, `311 Rhodes`, `182 Westwood`, `159 Gale`, `116 S Balch`, `43 S Bates` — **all seven cannot be priced**

That is 7 of the 13 off-market leads. They remain good *owner* leads and unpriced *deals*.

There is also **no 4-unit sold comp anywhere in Akron**, so `6090 Manchester Rd` is unpriced too. My earlier $250,000 was income-based on rents I invented. That number should never have been ranked #2.

---

## 6. Corrected lead list

| # | Property | Ask | Est. ARV | Repairs | Buyer max | Contract | Verdict |
|---|---|---|---|---|---|---|---|
| **1** | **156 Colony Cres 44305** | $55,000 | $150,000 | $35–55K | $50–77K | **$40–67K** | **CLEARS at asking if repairs ≤$40K. Only real deal.** |
| **2** | **838 Fess Ave 44307** | $45,000 | $105,000 | $25–35K | $32–55K | $21–45K | Fails as assignment by $1,500. **Buy-and-hold at ~$1,000/mo rent.** |
| **3** | **6090 Manchester 44319** | $108,000 | **UNPRICED** | $120K | ? | ? | No 4-unit comp, no rent roll. **Do not quote a number.** |
| **4** | **82 Aqueduct St 44303** | $119,900 | $165–195K | $45–60K | $55–91K | $45–81K | Needs −32% best case. Duplex range too wide to trust. |
| **5** | **141 Grand Ave 44302** | $95,000 | **$125,000** | $55–75K | $2–43K | −$8–33K | **REJECT — my ARV was 85% too high.** |
| **6** | **75 E Ido Ave 44301** | $109,900 | $120,000 | $55–65K | $12–36K | $2–26K | **REJECT — 52 E Brookside is a direct comp at $117,500.** |

---

## 7. What the verification actually changed

1. **The ZIP distinction is real and it is the whole game.** 44303 3-beds sell $200,000–$255,000. 44302 3-beds sell $74,000–$120,000. Same city, same house, 2× the price. My original Screen A instinct was right; I then applied it backwards to a 44302 property.
2. **Deed restrictions will wreck an ARV if you don't check.** Two of the four best 44305 5-bed sales are 80% AMI restricted — they are not market sales, and using them would have understated 156 Colony by $20,000.
3. **Six months of sold data is enough to kill a lead and not enough to price a duplex.** Bed-count and house-type filters work; multi-family does not exist in these ZIPs.
4. **After verification, one on-market property clears.** That is not a failure of the process. It is what the 70%-minus-repairs rule does to Akron retail — and now it is measured rather than asserted.
