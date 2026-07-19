# Forced Identification — วิกฤต "ฟิสิกส์พัง" ยุคนี้มีโครงสร้างเดียว (v2.0-dev)

> **Thesis [Dr; n=4 case studies, 2026-07-19].** วิกฤตระดับแนวหน้าของฟิสิกส์ยุคปัจจุบัน
> — Hubble tension, DESI evolving dark energy, muon g−2, JWST early massive
> galaxies — มีโครงสร้างเดียวกันใต้เลนส์:
>
> **ปริมาณชื่อเดียวกันจากคนละ chain ถูก "บังคับให้เป็นตัวเดียวกัน" ใต้ closure ของ
> โมเดล แล้วเสียงขัดแย้งของ chain ถูกอ่านผิดเป็นเสียงของโลก**
>
> เราเรียกกลไกนี้ว่า **forced identification** — การละเมิด Q3 (identity-by-role,
> `DOCTRINE_OF_QUANTITY.md`) ในระดับทั้งสนาม ไม่ใช่ความผิดพลาดของใครคนใดคนหนึ่ง
> แต่เป็นผลของธรรมเนียมการตั้งชื่อ + การรายงานที่ไม่พก chain มากับตัวเลข

## 1. กลไก ในภาษา RD

ให้สอง grammar A₁, A₂ (สองท่อการวัด/อนุมาน — คนละ posit ledger, คนละ Π) ต่างอ่าน
โลกใบเดียวกันแล้วคืน readout ที่*ธรรมเนียม*ตั้งชื่อเหมือนกัน: q₁, q₂ ทั้งที่บทบาท
เชิงเหตุ-อนุมานต่างกัน (Q3: คนละปริมาณ) จากนั้น closure C ของโมเดล (ΛCDM, SM
dispersion, SED posits) **บังคับ q₁ = q₂ โดยนิยาม** — ตรงนี้เองที่ residual ของการ
บังคับ (ซึ่งเป็นสมบัติของ *คู่ chain + closure*) ถูกแปลงร่างเป็น "σ ของ tension"
แล้วรายงานราวกับเป็นการวัดสมบัติของโลก

ผลพยากรณ์เชิงโครงสร้าง (ตรวจได้): tension แบบนี้จะ (ก) ไวต่อการสลับ dataset/
calibration ภายใน chain ผิดปกติ (เพราะมันคือสมบัติของ chain) และ (ข) "ทางแก้" จะ
งอกเป็นครอบครัวพารามิเตอร์ใหม่ที่เปิดทิศ near-null ให้แต่ละ chain ถือค่าของตัวเอง
ต่อไปได้ (CPL, early dark energy, …) — ทั้งสองลายเซ็นปรากฏครบในทุกเคสด้านล่าง

## 2. ตารางเคส (หลักฐานต่อแถว — ทุกแถวมี artifact หรือ record อ้างได้)

| เคส | ปริมาณที่ถูกบังคับรวม | chain ทั้งสอง | ลายเซ็น forced-identification ที่วัดได้ | artifact/หลักฐาน |
|------|----------------------|---------------|----------------------------------------|------------------|
| Hubble tension | `h` | CMB acoustic + ΛCDM closure vs distance-ladder ตรง | ปลด posit เดียว (w) → h วิ่ง 0.62–0.76 โดย θ★ นิ่ง: h_CMB คือพิกัดหลัง closure | `ap/ap1_hubble_identifiability.py` (4 pytest) |
| DESI "evolving DE" | `Ω_m` (และคู่ h) | BAO+ΛCDM closure vs CMB+ΛCDM closure | ตัวเปเปอร์ระบุ driver = 2.3σ BAO↔CMB; จุด SN-inclusive near-null ใน BAO (0.50%) แต่จุด BAO+CMB-only เหลือ 1.33% — **การอ่าน cross-chain เป็นบางส่วน ไม่ใช่ทั้งหมด**; σ แกว่ง 2.8→4.2 ตาม SN sample | `ap/ap3_desi_mirage.py` (5 pytest, สองจุดทดสอบ) + arXiv:2503.14738 |
| Muon g−2 | `a_μ^SM` | data-driven dispersion (e⁺e⁻) vs lattice QCD | "anomaly กับการทดลอง" สลายเมื่อ lattice เห็นด้วยกับ experiment; ตอนนี้ 4.6σ อยู่*ระหว่างทฤษฎีสองสาย* + CMD-3 ชนข้อมูลเก่าภายใน chain เดียว | arXiv:2606.17323 (final 127ppb), 2603.06806 (lattice, 4.6σ) — ประวัติศาสตร์ตัดสินฝั่ง readout ไปแล้วบางส่วน |
| JWST early galaxies | `M★` vs `M_halo·ε` | photometry→SED (IMF+SFH+dust posits) vs ΛCDM HMF + efficiency posit | posit ชน posit: วรรณกรรมเถียงกันเองว่า IMF ทำให้แย่ลง 3–4× หรือหายไป (posit นั้น load-bearing); Π ใหม่สุดขั้ว + "little red dots"→AGN ปน | arXiv:2601.20864 vs 2507.23742 (ทิศตรงข้ามจาก posit เดียวกัน); gates run 2026-07-19 |

หมายเหตุเชิงวิธี: ทั้งสี่เคสถูกไล่ผ่าน `lens.run_gates` จริง (G3/G4/G5 FLAG ตาม
เคส — ดู `VERIFIED_RUNS.md` และ session log 2026-07-19) ไม่ใช่จัดเข้าตารางด้วยมือ

## 3. สิ่งที่ thesis สั่งให้ทำ (reporting standard ที่ตกจากมันตรงๆ)

1. **ทุกตัวเลขพก chain** — รายงาน `(operator, Π, chain) → value` ไม่มี bare number
   (R1 ของ Doctrine); "h_CMB" กับ "h_ladder" ต้องเป็นคนละสัญลักษณ์จนกว่า
   role-equivalence จะถูกพิสูจน์
2. **รายงานพิกัดที่วัดจริง ไม่ใช่พิกัดครอบครัว** — w(z_pivot)±slope แทน (w₀,wₐ);
   ประกาศทิศ null ของ probe อย่างเปิดเผย (ข้อเสนอ AP1)
3. **ก่อนประกาศ tension = โลก** ต้องแสดงว่า: (ก) ทิศที่ขัดแย้ง identifiable จาก
   record ของแต่ละฝั่ง*แยกกัน* (ข) ความไวต่อ dataset-swap ภายใน chain ต่ำกว่า
   สัญญาณข้ามโลก — ไม่ผ่านสองข้อนี้ = ยังเป็นสมบัติของ closure

## 4. Falsifier ของ thesis เอง (ประกาศตามวินัย)

- เคสใดเคสหนึ่งข้างบน**จบลงเป็นฟิสิกส์ใหม่ฝั่งโลกที่ยืนยันอิสระ** เช่น BAO-alone
  full likelihood (h, Ω_m อิสระเต็ม) prefer CPL >~2σ; หรือ dynamical mass จาก
  kinematics ยืนยัน M★ เกินเพดานโดยไม่พึ่ง IMF posit; หรือ MUonE วัด HVP ทางที่สาม
  แล้วเข้าข้าง data-driven — แถวนั้นตาย และถ้าตายเกินครึ่งตาราง thesis ตาย
- **Selection bias ที่ประกาศเอง:** เราเลือกเคสดังสี่เคส ไม่ใช่ sample สุ่มของ
  tension ทั้งหมด; tension ที่*เคย*จบเป็นฟิสิกส์ใหม่จริงมีอยู่ (เช่น neutrino
  oscillations จาก solar-neutrino "deficit") — thesis จึงเป็น *diagnostic ที่ต้องรัน
  ต่อเคส* ไม่ใช่กฎว่า tension ทุกลูกเป็น artifact [ข้อนี้คือเส้นกัน overclaim]

## 5. Not-checked ledger

- n=4 และทั้งสี่เป็น toy-tier/gate-level — ยังไม่มีเคสไหนถูกไล่ถึง full likelihood
- muon g−2: ผมยังไม่ได้อ่าน theory-initiative whitepaper ฉบับล่าสุดเต็ม (อ้างจาก
  abstract 2 ฉบับ); JWST: สถานะ "little red dots" อ้างจากวรรณกรรมที่เคลื่อนเร็ว
- thesis นี้เองเป็น readout ของผู้อ่านขอบเขตจำกัด (Bounded-Judge) — ต้องผ่าน
  adversarial review ก่อน merge (สถานะ review ดูที่ PR) และยังไม่เคยถูกท้าโดย
  นักจักรวาลวิทยามืออาชีพ [Open สำหรับการใช้นอกวง]
