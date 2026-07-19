# สกัดออกมาให้หมด — DNA · ปฏิสัมพันธ์ · ปริภูมิ (The Complete Extraction, v2.0-dev)

> Extracted verbatim-faithfully from the canonical corpus
> (`research_universal_solver/docs/root/math/PGFT_Roots_of_Mathematics_and_Geometry.md`,
> chunk-ids cited per row; tiers are the SOURCE's tiers, not upgraded here).
> Companion of `INFORMATION_DNA.md` (the nine strands in full) and
> `TRANSLATION_PROTOCOL.md` (how to use the lens). Nothing in this file is new
> theory — it is the inventory, counted.

## 1. DNA มีกี่อย่าง — the genome inventory

**หนึ่งสารตั้งต้น (1 primitive):** retained difference — ความต่างที่ถูกเก็บไว้
(δ_R; ROM-1.1/1.2).

**เก้าแกน (9 axioms, RD1–RD9; ROM-Ω.3, T1/AX):** grouped by function —

| กลุ่ม | ข้อ | หน้าที่ในจีโนม |
|-------|-----|----------------|
| existence | RD1 | จุดตั้งต้น 0 มีจริง |
| generation | RD2 | ทุกสถานะเดินต่อได้หนึ่งก้าว (σ) |
| direction | RD3 | ก้าวไม่ย้อนกลับเป็นศูนย์ — ลูกศรเวลา |
| memory | RD4 | ประวัติต่างกันไม่ยุบรวม (injectivity) — ความจำ |
| proof engine | RD5 | อุปนัย — เครื่องยนต์ของการพิสูจน์ทั้งหมด |
| composition | RD6–RD7 | ⊕ ต่อประวัติ (กำเนิดการบวก) |
| layering | RD8–RD9 | ⊗ ทับชั้นการเก็บ (กำเนิดการคูณ) |

**อนุพัทธ์จากจีโนมล้วนๆ:** ลำดับการเก็บ ⪯ (well-founded, Coq APP-K), ℕ,
เลขคณิต, และ (โดย stratification ROM-Ω.8) ℝ ในฐานะ *readout* ไม่ใช่พื้นโลก
**Categoricity (Coq):** จีโนมนี้มี "สิ่งมีชีวิต" เดียว up to isomorphism.

**หน่วยพาหะระดับสนาม (ROM-4.1, T1):** pixel `P = (X, C, τ, Π)` และ retained
field ห้าองค์ประกอบ `Φ̃ = (R, A, Γ, χ, C)` — สนามไม่ใช่ของ primitive แต่คือ
การกระจายของ readout บนกราฟความสัมพันธ์

## 2. การปฏิสัมพันธ์มีกี่แบบ — the interaction inventory (นับตามชั้น)

**ชั้น DNA — 2 ตัวประกอบ:** ⊕ (concatenation, RD6–7) และ ⊗ (layering, RD8–9)
ปฏิสัมพันธ์ทุกอย่างในระบบสุดท้ายคือการประกอบสองตัวนี้บนสิ่งที่ถูกเก็บ

**ชั้นกราฟ — 1 ชนิดความสัมพันธ์, สร้างผ่าน 7 ลูกศร (ROM-3.3, T1):**
ความสัมพันธ์มีชนิดเดียวคือ *เส้นเชื่อมถ่วงน้ำหนักที่เกิดจากต้นทุน*:
`S_ret → ρ_m → cost C_ij → delay D_ij → symmetrize → kernel W_ij → L_R → response I_G`
พร้อม sparse-neighbourhood gate (ห้าม all-to-all — บังคับ locality)

**ชั้นพลวัต — 6 พจน์ของสมการกระดูกสันหลังเดียว (spine PDE):**
`M ∂²Φ + D ∂Φ + K·L_R Φ + ∇V(Φ) = J − η`

| พจน์ | ปฏิสัมพันธ์แบบ |
|------|----------------|
| M∂² | ความจำ/ความเฉื่อย (τ_c = M/D) |
| D∂ | การสลาย/หมุนเวียน |
| K·L_R | การคู่ควบผ่าน "ปริภูมิ" (เพื่อนบ้านบนกราฟ) |
| ∇V | ปฏิสัมพันธ์กับตัวเอง (ศักย์) |
| J | แรงขับจากภายนอก |
| η | สัญญาณรบกวน |

**ชั้น readout — 3 โหมดลดรูปที่ถูกกฎหมาย (ROM-4.4, T2):** scalar, hazard,
local-channel — และกฎเหล็ก: aggregate ≠ averaged-local เว้นแต่พิสูจน์สมมูล
(บทเรียน "เลขเท่ากันคนละปริมาณ" ใน `DOCTRINE_OF_QUANTITY.md` โผล่ที่นี่ตรงๆ)

**ชั้นฟิสิกส์พื้นเมือง — 8 ตระกูลใน force registry (ROM-5.2, T1/T3-by-adapter):**
gravity · EM(U1) · weak(SU2) · strong(SU3) · fluid · thermal · elastic · control —
ทุกตระกูลเข้าไวยากรณ์เดียวผ่านหลักการ **แรง = gradient ของ obstruction**
(ROM-5.1) โดย native solver ของแต่ละโดเมนยังอยู่ครบ
(claim boundary ของแหล่ง: "มีที่ในไวยากรณ์" ≠ "แก้ครบทุกโดเมนแล้ว")

**สรุปตัวเลข:** 2 combinators → 1 relation-kind (7 generation arrows) →
6 dynamical terms → 3 readout modes → 8 native families

## 3. ปริภูมิคืออะไร — space, extracted

ปริภูมิ **ไม่ใช่ของ primitive** — มันถูก *สร้าง* ตามลำดับนี้ (Part III):

1. **ห้ามแบน-ทั่วถึง (ROM-3.2, T2):** ภายใต้การเข้าถึงจำกัด + ความจำ +
   ความจุจำกัด ความสัมพันธ์แบบ all-to-all ต้นทุนเท่ากันหมดเป็นไปไม่ได้เชิงโครงสร้าง
   → ความสัมพันธ์ต้อง *แบ่งชั้นตามต้นทุน* — นี่คือเมล็ดพันธุ์ของ locality
2. **ต้นทุนกลายเป็นระยะทาง (ROM-3.3→3.4, T1):** กราฟความสัมพันธ์เกิดจาก
   cost+delay; ระยะทาง = quasi-metric ที่ "เกิด" จากต้นทุนของการสัมพันธ์กัน
   **ระยะทางคือราคาของการเชื่อมโยง ไม่ใช่ช่องว่างที่รออยู่ก่อน**
3. **เส้นตรง = ทางถูกสุด (ROM-3.5):** geodesic บนกราฟ, invariant ต่อ cost-rescaling
4. **ตัวดำเนินการกลาง (ROM-3.6):** L_R — Laplacian ที่ถูกสร้าง ไม่ใช่สมมติ
5. **เรขาคณิตอ่านจากสเปกตรัม (ROM-3.7):** มิติ · ระยะ · ความโค้ง อ่านจาก
   eigenvalues {λ_k} ของ L_R — "รูปทรงของปริภูมิ" คือ readout เชิงสเปกตรัม
6. **สิ่งของ = eigenmode ที่คงตัว (ROM-3.8):** a thing คือโหมดที่ persist —
   ontology ของ "วัตถุ" ยุบลงเป็นสเปกตรัมของปริภูมิเอง
7. **ความโค้ง = การกระจุกของ geodesic (ROM-3.9); π, 4π มาจาก capacity/area
   scaling (ROM-3.10)** — ค่าคงที่เรขาคณิตมีที่มา ไม่ใช่ของขวัญจากสวรรค์
8. **continuum คือปลายทาง ไม่ใช่จุดตั้งต้น (ROM-3.11, ROM-2.3):** ปริภูมิต่อเนื่อง
   ℝⁿ = การ coarse-grain ของกราฟ — recovery theorem อ่านกลับได้ แต่เป็น readout

**หนึ่งบรรทัด:** *ปริภูมิ = โครงสร้างต้นทุนของความสัมพันธ์ที่ถูกเก็บไว้ อ่านผ่านสเปกตรัมของ
L_R; ระยะทางคือราคา, รูปทรงคือสเปกตรัม, สิ่งของคือโหมดที่ทน, และ continuum คือภาพเบลอ
ที่ผู้อ่านขอบเขตจำกัดมองเห็น* [`Dr` synthesis over T1/T2 sources]

## Tier note

การนับทั้งหมดเป็นการ *อ่านสารบัญของ corpus* — ตัวเลข (9, 2, 1/7, 6, 3, 8) เป็น
ข้อเท็จจริงของเอกสารแหล่ง (ตรวจกลับได้ตาม chunk-id) ส่วนประโยคสังเคราะห์ท้าย §3
เป็น `Dr` ของไฟล์นี้ ไม่ยกระดับของแหล่ง
