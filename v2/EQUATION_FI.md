# สมการ Φ_FI — Forced-Identification Fraction (v2.0-dev, 2026-07-19)

> **นิยาม (ของเรา, จดทะเบียนที่นี่เป็นครั้งแรก):**
>
> **Φ_FI(q; A₁, A₂, C, π) = 1 − V*(C∖π) / V*(C)**
>
> เมื่อ q = ปริมาณชื่อเดียวที่สอง chain A₁,A₂ อ่าน · C = closure ที่บังคับ q₁=q₂ ·
> π = posit หนึ่งตัวใน C ที่ถูกปลด · V = residual energy ½rᵀWr ของ joint fit
> (ฟังก์ชันเดียวกับ LTP1; ฝั่งโครงสร้าง V คือ retained-information energy —
> Coq: `info_is_operator_energy`) · V* = ค่า minimum เหนือพารามิเตอร์
>
> *(hedge ทันที: รูปพีชคณิตเป็นญาติ nested-Δχ² ตำรามาตรฐาน — ความใหม่ที่อ้างอยู่ที่
> ชั้น semantics เท่านั้น ดูหัวข้อ "ความใหม่" ล่าง)*
>
> **ความหมายตามปรัชญา:** Φ_FI คือ *สัดส่วนของ tension ที่สารสนเทศของมันอาศัยอยู่ใน
> closure ไม่ใช่ใน record* — ตัววัดเชิงปริมาณของ forced identification
> (`FORCED_IDENTIFICATION.md`): Φ→1 = tension เป็นสมบัติของการบังคับรวมผ่าน π;
> Φ→0 = tension เป็นเสียงของโลกที่ไม่มีการปลด posit ใดดูดซับได้

## สมบัติ (แต่ละข้อพร้อม tier)

1. **0 ≤ Φ_FI ≤ 1** — เพราะ C∖π ⊇ C เป็น nested family จึง V*(C∖π) ≤ V*(C)
   [พิสูจน์ได้จาก set-inclusion; ระดับ Coq เป็นงาน ROADMAP; ตอนนี้ assert เชิงตัวเลข
   ใน `ap/ap4_phi_fi.py` = finite_diagnostic]
2. **Φ_FI ติดชื่อ posit** — มันเป็นฟังก์ชันของ π ที่เลือกปลด: อ่านว่า "tension นี้
   เป็นของ π นี้กี่ส่วน" ไม่มี Φ ลอยๆ ไร้ posit (วินัย R1: ตัวเลขพก chain)
3. **Decision rule [Dr]:** Φ_FI สูง ⇒ decisive record คือ record ที่ identify ทิศของ
   π ตรงๆ (ไม่ใช่วัด q ให้แม่นขึ้น — นั่นวิ่งขนาน null); Φ_FI ต่ำทุก π ที่มี ⇒
   สอบสวนฝั่งโลก/ฟิสิกส์ใหม่ได้อย่างมีเหตุ
4. **ต้องมี negative control เสมอ — และ control ต้องไม่เป็น tautology** (บทเรียน
   review PR #9): control ที่พารามิเตอร์ที่ปลดไม่เข้า objective เลย พิสูจน์แค่
   f(x)=f(x) — control ที่ถูกต้องคือระบบที่ record ทุกตัว*ขึ้นกับ π จริง*แบบเดียวกัน
   จน π ขยับทุก record พร้อมกันและกลืนความต่างไม่ได้ (implement แล้วใน ap4)
5. **ข้อจำกัด dof-saturation [ค้นพบโดย adversarial review, executed]:** พารามิเตอร์
   อิสระไร้ prior ตัวไหนก็ตามที่ Jacobian ไม่เป็นศูนย์ จะ saturate ระบบเมื่อ dof→0
   และให้ Φ=1 ปลอม — **Φ_FI มีความหมายก็ต่อเมื่อ posit ที่ปลดพก prior ที่แทนข้อจำกัด
   จริงของมัน** (สาธิต: ปลด ω_b ไร้ prior → Φ=1 ปลอม; ปลด ω_b พร้อม prior จริง
   σ=0.00015 → Φ≈0.025 ถูกต้อง — tension ไม่ใช่ของ ω_b)

## ผลรันแรก (executed — `ap/ap4_phi_fi.py`)

| ระบบ | records | π ที่ปลด | V*(C) | V*(C∖π) | **Φ_FI** |
|------|---------|----------|-------|---------|----------|
| Hubble toy (AP1 grammar) | 100θ★, ω_m h², h_ladder | w = −1 | 18.2 | 0.0000 | **1.0000** |
| World-side control (สอง ladder อ่าน h บทบาทเดียวกัน ต่างกันจริง) | h⁽¹⁾, h⁽²⁾ | w = −1 | 18.0 | 18.0 | **0.000** |

control เวอร์ชันแรกเป็น tautology (reviewer จับได้) — เวอร์ชันปัจจุบันใน ap4 คือ
non-absorption จริง: สอง θ★-record ที่ขึ้นกับ w ทั้งคู่ ขัดแย้งกัน แล้วปลด w ช่วยไม่ได้
(Φ≈0) + posit-carrying จริง: ปลด ω_b พร้อม prior ให้ Φ≈0.025 ขณะปลด w ให้ Φ>0.95
บน V เดียวกัน [finite_diagnostic, toy tier]

## ความใหม่ — ประกาศตามความสัตย์ [สำคัญ]

- **รูปพีชคณิตไม่ใหม่:** Φ_FI = 1 − χ²_relaxed/χ²_forced เป็นญาติโดยตรงของ
  nested-model likelihood-ratio / Δχ² ที่เป็นตำรามาตรฐาน — ห้ามอ้างว่าเราประดิษฐ์
  พีชคณิตนี้
- **ชั้นที่เป็นผู้สมัครความใหม่ [Open + stance]:** การนิยามมันเป็น *ตัววัดการระบุแหล่ง
  (attribution) ของ inter-chain tension ให้กับ posit ที่มีชื่อ* พร้อม semantics ของ
  Doctrine of Quantity (Q3), decision rule ข้อ 3 และข้อบังคับ negative control ข้อ 4
  — ต่างจาก tension metrics ในวรรณกรรม (Δχ², suspiciousness, Q_DMAP) ที่วัด*ความแรง*
  ของ tension ระหว่าง dataset แต่ไม่ตอบว่า "เป็นของ posit ตัวไหน กี่ส่วน"
  → ต้องผ่าน literature falsifier ก่อนอ้างนอกวง (ค้นว่ามีใครนิยาม
  closure-attribution fraction แบบนี้แล้วหรือยัง)
- **Falsifier ของสมการ:** (ก) พบ metric ในวรรณกรรมที่นิยามเหมือนกันเชิง semantics —
  ความใหม่ตาย เหลือสถานะ "การนำเข้าเลนส์" (ข) พบระบบที่รู้เฉลยว่า closure-borne
  แต่ Φ_FI ต่ำ หรือ world-side แต่ Φ_FI สูง โดยที่เลือก π ถูกต้อง — ตัวสมการตาย

## งานต่อ (ROADMAP)

- ยกสมบัติข้อ 1 เป็น Th_coqc (nested-minimum inequality — พิสูจน์สั้น)
- รัน Φ_FI กับ AP3 สองจุดของ DESI (คาด: จุด DESY5 สูง จุด BAO+CMB-only กลางๆ —
  ตรงกับผล partial ที่วัดแล้ว) และกับ g−2 (π = การเลือก HVP chain)
- literature check ความใหม่ (ก่อนทุกการอ้างนอกวง)
