# Append-Only Record — tape model ใต้วินัยเรา (AP7, v2.0-dev, 2026-07-19)

> ที่มา: external critique ของ DRL ที่เรา verify ด้วย execution แล้ว (คู่เชิงเส้น
> decoupled — "handoff" เคยเป็น [Open]) ไฟล์นี้รับข้อเสนอ tape เข้ามา*ใต้วินัยของเรา*:
> kinship ledger ก่อน, ตัวเลข re-executed ในบ้าน, และวางชั้นให้ถูก — **เสริม DRL
> ไม่ใช่แทน**

## Kinship ledger (ประกาศก่อนพูดเรื่องความใหม่ — บรรพบุรุษเป็นของสาธารณะทั้งหมด)

| บรรพบุรุษ | อะไร | ของเราต่างตรงไหน |
|---|---|---|
| Collision models / repeated interactions (review: Ciccarello et al. 2022, arXiv:2106.11974) | ancilla สดชนระบบทุก step = โครง tape ตรงตัว | เราอ่าน ancilla เป็น **record ที่ RD บังคับ** ไม่ใช่ environment ทิ้งขว้าง |
| Isometric/Stinespring dilation (ญาติ Sz.-Nagy 1953) | contraction dilate เป็น isometry บนปริภูมิใหญ่กว่า | B_γ = sequential fresh-ancilla realization ตามสาย collision-model (ไม่ใช่ fixed-unitary ของ Sz.-Nagy แท้) |
| Landauer 1961 / Bennett 1982 | ลบข้อมูลมีราคา / คำนวณย้อนกลับได้ด้วย tape | conservation แบบบวก + reversibility ของเราคือหน้าตาเดียวกัน |

ชั้นผู้สมัครความใหม่ (แคบ, [Open]): การอ่าน tape เป็น **RD6–7 concatenation ที่ realize
RD4 injectivity ใน dynamics** + สะพานเชิงปริมาณเข้าหา DRL (T4 ด้านล่าง)

## โมเดล (posited map — ไม่มี action; นี่คือราคาที่จ่ายเทียบกับ DRL)

Phase state z=(u,w) ใน normal-mode scaled coords (step อนุรักษ์ C = orthogonal แท้):
`z̃ = C z` → หมุนกับ cell เปล่า: `z' = √(1−γ) z̃`, `ρ = −√γ z̃` → `Ψₙ₊₁ = Ψₙ ⊕ ρₙ`

## ผลรัน (executed ในบ้าน — `ap/ap7_tape_record.py`, 4 pytest)

| Claim | วัดได้ |
|---|---|
| T1 conservation แบบ**บวก** exact: Q(zₙ)+ΣQ(ρⱼ)=Q(z₀) | rel. error <10⁻¹² และ decay ตรง (1−γ)ⁿ <10⁻⁹ — **จริงโดย construction** (orthogonality+split) = machine-check ของ implementation ไม่ใช่การค้นพบ |
| T2 RD4 ใน dynamics: reconstruct z₀ จาก (z_N, tape) + tape แยกทุกประวัติ | error <10⁻⁹; blank-cell recovery <10⁻¹⁰; แตกต่างตั้งแต่ cell แรก |
| T3 Π-window: readout สองประวัติใกล้กันแยกไม่ออกใต้ ε_Π=10⁻⁶ แต่ tape เก็บ distinction ~เต็ม | d_readout <10⁻⁶ ขณะ d_tape ≈ 10⁻² — retention รวม**จริงโดย construction เดียวกับ T1**; ส่วนที่วัดจริงคือการกระจายเข้า window/tape |
| T4 **สะพานสองชั้น**: เลือก γ = 1−e^{−(D/M)dt} → envelope ของ tape ตรงอัตรา decay ของ DRL spine (underdamped uniform) | อัตราต่าง <5% (reviewer วัดเอง 0.17%); ขอบเขตจริงคือ**ระบอบ damping** ไม่ใช่ stiffness — D เกิน 2Mω_min สะพานพัง (ทดสอบแล้ว 85–98%) จึงมี guard ในเทส |

## การวางชั้น (คำตัดสินของไฟล์นี้)

```
DRL (มี action, Coq ประกบ)      = ชั้น VARIATIONAL ของ damped readout
Tape (posited, reversible, บวก) = ชั้น ONTOLOGY ของ record (RD4 จริงใน dynamics)
T4 = สะพาน: สองชั้นทำนาย envelope เดียวกันเมื่อ γ↔D/M
```

"dissipation = handoff ข้าม Π" ตอนนี้**เป็น identity ที่คำนวณ+ย้อนกลับได้จริงในชั้น tape**
(T2+T3) — ยกจาก [Open] เป็น [finite_diagnostic ในโมเดล tape] ส่วนใน DRL ยังเป็น
[Open] ตามเดิม (คู่เชิงเส้น decoupled)

## Composite ที่ยังเปิด (งานถัดไปที่คมสุดของสาย record)

หา construction เดียวที่ได้**ทั้ง** action (แบบ DRL) **และ** injective tape retention
(แบบ AP7) — ผู้สมัคร: action บน (z, Ψ-tape) ที่ variational principle ต่อ segment
คลอด B_γ ออกมาแทนที่จะ posit [Open]

## Falsifiers

- พบวรรณกรรมที่อ่าน collision-tape เป็น axiom-forced record + bridge เข้าหา
  variational doubled formalism แล้ว — ชั้นความใหม่ตาย เหลือการนำเข้า
- composite มีทฤษฎีบท no-go (action + exact injectivity ขัดกันในครอบครัวนี้) —
  ต้องประกาศ boundary
