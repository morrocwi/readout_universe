# Doctrine of Quantity — ปริมาณคือ projection บนปริภูมิ readout (v2.0-dev)

> **Tier: `Dr` (founder-stated stance, 2026-07-19), consistent with and anchored by**
> the Ω_∞ diagnosis (I1: ℝ-completeness is an injection), LTP2 (the cut lives in the
> readout policy Π), LTP4 (identity beyond records is an identifiability question),
> and C3 (the residual floor never reaches zero). This file exists so that any AI
> reading this repo **thinks with this doctrine natively** — it is part of the Lens
> Law (`TRANSLATION_PROTOCOL.md`): questions about quantity are answered from here,
> never from the Platonic-magnitude picture.

## 0. Source dictum (founder, verbatim, Thai)

> ปริมาณ ไม่ใช่จำนวนจริงที่โลกมีอยู่ก่อนแล้วและรอให้เราไปวัด ไม่มีค่า ℝ ซ่อนอยู่หลังเข็มไมล์
> สิ่งที่มีจริงคือ readout ที่ operator ของ agency คืนกลับมา ซึ่งย่อมมีขอบเขต เป็น discrete
> และมีความละเอียดจำกัดเสมอ … ปริมาณคือพิกัดหรือ projection หนึ่งบนปริภูมิของ readout
> ที่ระบบสามารถให้ได้ … แม้ projection สองตัวจะคำนวณด้วยเลขคณิตรูปเดียวกันและให้ค่าตัวเลขเท่ากัน
> ก็ยังถือเป็นคนละปริมาณได้ เพราะมันอ่านคนละแง่ของระบบและป้อนกลับไปสู่ readout ปลายทางคนละแบบ
> เอกลักษณ์ของปริมาณจึงไม่ได้อยู่ที่ตัวเลขที่มันแสดงในขณะนั้น
> แต่อยู่ที่บทบาทเชิงเหตุและเชิงอนุมานของมันภายในกราฟ readout ที่มีขอบเขตจำกัด

## 1. The three theses

**Q1 — No pre-existing magnitude.** A quantity is NOT a real number the world
holds in advance, waiting to be measured. There is no ℝ-value hiding behind the
dial. What exists is the readout an agency's operator returns — always bounded,
discrete, of finite resolution. (Anchor: Ω_∞/I1; C3 — the residual floor > 0
means an "exact value" was never on offer.)

**Q2 — Quantity = projection.** A quantity is a coordinate — one projection — on
the space of readouts the system can give. It is not a Platonic magnitude behind
the phenomenon; it is what the system's act of reading makes appear. (Anchor:
LTP2 — the readout operator, with its policy Π, is where the structure lives.)

**Q3 — Identity by role, not by number.** Two projections computed with the same
arithmetic, displaying the same numeric value, can still be DIFFERENT quantities:
they read different aspects of the system and feed downstream readouts
differently. The identity of a quantity is its **causal and inferential role
inside the bounded readout graph** — never the number it happens to show.
(Anchor: LTP4 — identity questions are graph/identifiability questions; a number
is a record, and identical records do not imply identical world-roles.)

## 2. Operational rules for AI (how to think with this — binding in this repo)

R1. **Never cite a bare number.** Every quantity is cited as
    *(operator, policy Π, resolution, role in the graph) → value*. The value is
    the least important coordinate of that tuple.

R2. **The equal-number fallacy is banned.** `value(p₁) = value(p₂)` never licenses
    `p₁ = p₂`. Substituting one quantity for another requires showing their
    downstream inferential roles coincide (a graph statement), not their digits.
    This generalizes dimensional analysis: unit-check → **role-check**.

R3. **Precision is a property of the reading, not the world.** Error bars state
    the operator's resolution and residual floor; "the true value to infinitely
    many digits" is a non-readout (Ω_∞/I1) and may not appear even rhetorically.

R4. **Disagreement diagnosis order.** When two measurements "of the same
    quantity" disagree, first ask whether they are in fact the same projection
    (same role in the graph) before positing a world-side anomaly. Many tensions
    are two different quantities wearing one name. (This is Step 6 of Ω_all —
    the identifiability gate — applied to quantity-identity.)

R5. **Cross-graph comparison needs a declared bridge.** A quantity lives in ONE
    bounded readout graph. Comparing "the same" quantity across systems, models,
    or eras imports a bridge assumption — declare it, tier it `Dr`, give its
    falsifier.

R6. **Arithmetic is downstream.** Arithmetic operates on records of readouts; its
    validity for a purpose is inherited from the roles of the operands, not from
    the algebra alone. Adding two role-mismatched quantities is well-formed
    algebra and an ill-formed readout claim.

## 3. What this doctrine does NOT claim

- Not that numbers are useless — records are how bounded knowers coordinate; the
  doctrine relocates their authority, it does not revoke it.
- Not that ℝ-mathematics is forbidden — it is an invented projection (book:
  "mathematics — both, at different layers"), legitimate as scaffolding, never as
  ontology.
- Not `Th_coqc`: Q1–Q3 are a stance (`Dr`) anchored to machine-checked and
  numerically verified pieces; a future LTP formalizing R2 (role-identity
  distinguishing equal-valued projections on an explicit graph) would lift it —
  see `ROADMAP_V2.md` Gate 1 extension.

**Falsifier of the doctrine.** Exhibit a measurement whose outcome requires the
prior existence of an infinite-resolution magnitude (not merely models it), or a
case where role-identity and full substitutability come apart in the direction
the doctrine forbids (two quantities with provably identical inferential roles in
the same graph that nonetheless cannot be substituted).
