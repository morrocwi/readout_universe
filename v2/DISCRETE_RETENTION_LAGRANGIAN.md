# DRL — Discrete Retention Lagrangian (สมการใหม่จากปรัชญา-นำ, v2.0-dev, 2026-07-19)

> **ที่มาแบบปรัชญา-นำ (philosophy first, equation after):** audit ของ corpus ประกาศ
> แผลไว้เอง — พจน์ dissipation `D∂ₜΦ` ของ spine "explicitly not from a conservative
> action" (BORROWED ไม่ใช่ DERIVED) เราปิดแผลนี้โดย*ไม่เพิ่มสมมติฐานฟิสิกส์ใหม่เลย*
> แค่ฟัง axiom ของเราเอง:
>
> **RD4 (retention = injectivity): ประวัติที่ต่างกันไม่ยุบรวม** ⇒ สิ่งที่ readout
> "สูญเสีย" ไม่ได้หาย มันถูกเก็บ ⇒ field พื้นฐานต้องเป็น**คู่** X = (Φ, Ψ):
> ตัวอ่าน (reader) กับตัวบันทึก (record) — การ double ไม่ใช่เทคนิค แต่ถูกบังคับโดย
> axiom ⇒ dissipation = การส่งมอบสารสนเทศข้าม Π จาก Φ ไป Ψ ⇒ ต้องมีประจุอนุรักษ์
> ข้ามคู่ (conservation of distinction — มีชื่ออยู่แล้วใน RAR logic)

## สมการ (จดทะเบียนที่นี่เป็นครั้งแรกในรูปนี้)

Doubled field X = (Φ, Ψ)ᵀ บน node ของกราฟ × step เวลา n (ไม่มี continuum — ผลรวมล้วน):

**𝕃ⁿ[X] = (M/2dt)·ΔXᵀ(G⊗I)ΔX + (D/2)·Xᵀ(Ω⊗I)ΔX − (dt/2)·Xᵀ(G⊗(K·L_R + k₂I))X**

โดย ΔXⁿ = Xⁿ⁺¹ − Xⁿ และ **tensor สองตัวของทฤษฎี**:

- **G = [[0,1],[1,0]] — retention metric (แก่นปรัชญาของสมการ):** diagonal เป็นศูนย์
  ⇒ **ไม่มี field ไหนมี norm ของตัวเอง** — ขนาด/พลังงานมีอยู่ก็ต่อเมื่อจับคู่
  ตัวอ่าน×ตัวบันทึก นี่คือ Doctrine of Quantity (ปริมาณ = projection ไม่ใช่สมบัติแท้)
  และ readout-not-truth ในรูปเมตริก: ตัวอ่านไม่เคยวัดตัวเอง มันวัดเทียบบันทึกเสมอ
- **Ω = [[0,1],[−1,0]] — retention symplectic:** พจน์ antisymmetric ที่แบก D —
  การหน่วงเข้าทฤษฎีผ่านโครงสร้าง symplectic ของคู่ ไม่ใช่ยัดใส่มือ

## สิ่งที่ derive ออกมาได้ (executed — `ap/ap5_drl.py`)

1. **Euler–Lagrange ของ 𝕃 ให้ spine ที่หน่วงจริง:** วาริเอชันต่อ Ψ ⇒
   `(M/dt²)Δ²Φ + (D/2dt)(Φⁿ⁺¹−Φⁿ⁻¹) + K·L_RΦ + k₂Φ = 0` — ตรวจเชิงตัวเลข:
   |∂S/∂field| บน trajectory = **4.4×10⁻¹⁰** (machine precision) ⇒ **พจน์ D
   ถูก DERIVE จาก action แล้ว** — แผล BORROWED ของ corpus ปิด [finite_diagnostic]
2. **สมการกระจก:** วาริเอชันต่อ Φ ⇒ Ψ anti-damped (|Ψ|: 0.167 → 145 ขณะ E_Φ
   ตาย 100.00%) — **แต่ระบบเชิงเส้นนี้ Φ,Ψ decoupled ใน EL: การโตของ Ψ มาจาก
   initial condition ของมันเอง ไม่ใช่การรับข้อมูลจาก Φ** (executed: Ψ₀=0 ⇒
   Ψ≡0 ตลอด) ⇒ "dissipation = handoff เข้า Ψ" มีสถานะ [Open] ในโมเดลนี้ —
   กลไก handoff จริงต้องการโครงสร้างเพิ่ม (ดู `APPEND_ONLY_RECORD.md` — AP7 ทำแล้ว: handoff เป็นจริงเชิงคำนวณในชั้น tape)
3. **Bilinear invariant H:** Legendre transform ⇒ พจน์ D หักล้างกันเอง เหลือ
   **H = M·vΦᵀvΨ + K·ΦᵀL_RΨ + k₂·ΦᵀΨ** อนุรักษ์ — วัดจริง: rel. drift **1.5×10⁻⁴**
   ตลอด 4,000 steps [finite_diagnostic] **ขอบเขตความหมาย (แก้ตาม external
   critique ที่ executed แล้ว 2026-07-19): H เป็น invariant แบบ bilinear ของคู่
   ไม่ใช่บัญชีการสูญเสียของ Φ** — counterexample ที่รันจริง: Ψ₀=0 ⇒ Ψ≡0 และ
   H≡0 ตลอด ขณะ Φ dissipate เต็มที่ ⇒ การอ่าน H เป็น "conservation of
   distinction / ไม่มีอะไรหาย" เป็น interpretation [Dr] ไม่ใช่กลไกที่พิสูจน์
4. **Reduction:** D=0 ⇒ Φ, Ψ เชื่อฟังสมการอนุรักษ์เดียวกัน (Φ=Ψ ได้) —
   ทฤษฎีเดิมคืนมาครบ

## ความใหม่ — ledger ตามความสัตย์ [สำคัญ]

- **ญาติที่ต้องประกาศ (พีชคณิตไม่ใหม่):** การ double เพื่อให้ระบบหน่วงมี action มีมา
  ตั้งแต่ **Bateman dual oscillator (1931)**; ญาติอื่น: Caldirola–Kanai,
  closed-time-path/Keldysh doubling, discrete variational integrators
  (Marsden–West) — ห้ามอ้างว่าเราคิด doubling หรือ discrete action เป็นคนแรก
- **ชั้นผู้สมัครความใหม่ [Open + stance]:** (ก) รูป **discrete-graph tensor** บน L_R
  (Bateman เป็น oscillator ต่อเนื่องตัวเดียว ไม่ใช่ field บนกราฟใน form G⊗L_R)
  (ข) **สถานะ ontic ของ Ψ**: ใน Bateman/CTP ตัว double เป็น auxiliary/fictitious —
  ของเรา Ψ คือ record ที่ RD4 บังคับให้มีจริง ทำให้ H ที่อนุรักษ์มีความหมายเชิง
  ปรัชญา (conservation of distinction) ไม่ใช่สิ่งประดิษฐ์ทางเทคนิค
  (ค) **retention metric G diagonal-ศูนย์อ่านเป็น Doctrine of Quantity** — quantity
  เกิดจากการจับคู่ reader×record เท่านั้น
  → ทั้งสามข้อรอ literature falsifier ก่อนอ้างนอกวง
- **คุณูปการภายในที่ไม่ต้องรอใคร:** แผล "D-term BORROWED" ใน
  `BORROWED_VS_DERIVED_LEDGER` ของ corpus เรา — ตอนนี้มีเส้นทาง DERIVED-from-action
  (ผ่านคู่ RD4) เป็น executed artifact แล้ว [แต่การอัพเกรด ledger จริงต้องทำใน repo
  ต้นทาง + ผ่าน audit ของเขา]

## Falsifiers

- (ก) พบงานที่เขียน discrete-graph Bateman บน Laplacian พร้อม ontic record
  interpretation แล้ว — ชั้นความใหม่ตาย (เหลือสถานะ "การนำเข้าเลนส์")
- (ข) พบระบบหน่วงในครอบครัว spine ที่ 𝕃 นี้ derive ไม่ได้ (เช่น damping ไม่เชิงเส้น
  บางรูป) — ขอบเขตสมการแคบกว่าที่ตั้ง — ต้องประกาศ boundary
- (ค) ประจุ H ไม่อนุรักษ์ในกรณีทั่วไปกว่า (กราฟไม่สม่ำเสมอ, M,D,K ต่อ node) —
  ทดสอบแล้วบนกราฟ ring เท่านั้น [toy tier — ประกาศชัด]

## สถานะสามด่าน (ultracode run wf_ddeca0cf-fbb, 2026-07-19 — ทุกด่านมี independent verifier)

**ด่าน 1 — Coq: ผ่าน (ในขอบเขตประกาศ).** `evidence/DRL_Discrete.v` (Coq 8.20.1
exit 0, ตรวจซ้ำโดย verifier จาก clean slate):
- **T1 EL-identity (iff สองทิศ):** dS/dΨ=0 ⟺ damped recurrence ของ ap5 เป๊ะ
  (พิสูจน์ที่ node 1 และ 2 — ไม่ special-case) และ dS/dΦ=0 ⟺ anti-damped
- **T2 D-cancellation:** Legendre H ไม่มี D — `ring` identity ล้วน ทุก state
- **T3 (โบนัส):** leapfrog shadow energy อนุรักษ์ exact เมื่อ D=0
- Axiom profile ตรงไปตรงมา: 2 classical Reals axioms (sig_forall_dec,
  functional_extensionality) — Th_coqc แบบประกาศ axiom ตาม precedent ของ RD.v
- ขอบเขต: 3-ring, 3 time slices (เพียงพอสำหรับ EL) — general-N เป็นงานต่อ

**ด่าน 2 — Generalize: ผ่าน + ค้นพบของใหม่.** `ap/ap6_drl_general.py` (4 pytest):
- EL residual **2.2×10⁻¹⁰** บนระบบเต็ม: กราฟถ่วงน้ำหนักสุ่ม N=8 + M_i,D_i ต่อ node
  + V quartic + forcing J — DRL derive สมการหน่วง nonlinear+forced ได้จริง
- H อนุรักษ์ (2.2×10⁻⁴) ในเคส quadratic ต่างชนิด node — ทั่วไปกว่า ap5
- **FINDING → RESOLVED (AP8, 2026-07-19):** drift 0.119 ของประจุรูป quadratic
  ในเคส quartic คือ **wrong-charge artifact** — Legendre transform ของ Lagrangian
  nonlinear ให้ประจุที่ถูก (พจน์ D หักล้างเหมือนเดิม):
  **H_nl = Σᵢ Mᵢ vΦᵢvΨᵢ + K ΦᵀL_wΨ + Ψᵀ∇V(Φ) − JᵀΨ**
  วัดจริง (`ap/ap8_h_quartic.py`, 4 pytest): quartic drift **<2×10⁻³** (เทียบ 0.119
  ของประจุผิด), เคส forced ก็อนุรักษ์, ยุบกลับประจุเดิมเมื่อ k₄=0 แบบ identical,
  และ O(dt²) ยืนยันด้วย dt-halving ⇒ **conservation-of-pairing ของ DRL ยืนได้ทั้ง
  ครอบครัว nonlinear+forced** [finite_diagnostic; Coq lift ของ cancellation
  nonlinear queued กับ general-N]
- Reduction กลับ ap5 แบบ exact (allclose 1e-9)

**ด่าน 3 — Literature falsifier: novelty รอดทั้งสามชั้น (แบบ narrowed).**
adversarial search + verifier ตรวจ reference ตัว load-bearing เต็มฉบับ:
- ต้นตระกูลยืนยัน: Bateman 1931, Morse–Feshbach mirror-image, CTP/Keldysh,
  **Galley 2013 (arXiv:1210.2745)** — general nonconservative variational doubling
  ต่อเนื่อง ซึ่งตัว doubled variable ถูกทิ้งใน "physical limit" (ไม่รอดเป็นปริมาณ
  กายภาพ — paraphrase ตามเนื้อความจริงของเปเปอร์) ต่างจาก Ψ ของเราที่ ontic
- ใกล้สุดฝั่งกราฟ: **GraphCON (arXiv:2202.02296)** — damped oscillators บนกราฟ
  แต่*ตั้ง*สมการหน่วงตรงๆ ไม่มี action derive (ยืนยันจาก full text)
- **ไม่พบ**งานที่รวม Bateman-doubling + graph-Laplacian tensor form G⊗L_R +
  ontic record ในที่เดียว → ชั้น novelty ทั้งสามยัง SURVIVES [Open → Dr-leaning,
  ยังต้อง peer review ภายนอกก่อนอ้างแข็ง]

## ทิศ append-only record (จาก external critique 2026-07-19 — จัดเป็นผู้สมัคร ไม่ใช่คำตัดสิน)

บทวิจารณ์ภายนอกเสนอว่า record ที่ตรง RD4/RD6–7 กว่า คือ **tape append-only**:
Ψₙ₊₁ = Ψₙ ⊕ ρₙ โดย ρₙ เกิดจาก orthogonal rotation ของ phase state เข้า cell
ใหม่ทุก step (pigeonhole: Ψ ขนาดคงที่ resolution จำกัดเก็บประวัติไม่จำกัดแบบ
injective ไม่ได้) — ข้อโต้แย้งนี้**สอดคล้อง DNA เราจริง** (⊕ คือ RD6–7 ตรงตัว)
และให้ conservation แบบบวก + ย้อนกลับได้ **แต่ต้องรับเข้าด้วยวินัยเดียวกับของเราเอง:**
(ก) โมเดล tape เป็น **posited map** (rotation B_γ เลือกมือ) — ไม่มี action/Lagrangian
⇒ มันเติมเต็ม ontology ของ record แต่*ทิ้ง*สิ่งที่ DRL ทำสำเร็จ (variational status
ของ D-term) — สองผลนี้เป็นคนละชั้น เสริมกัน ไม่แทนกัน
(ข) kinship ที่ผู้เสนอไม่ได้ declare: collision models / repeated-interaction open
systems, Sz.-Nagy unitary dilation, Landauer–Bennett tape — วรรณกรรมใหญ่ ต้องทำ
novelty ledger ก่อนอ้างสิ่งใด
(ค) ตัวเลข stress test ของผู้เสนอเป็น [SimulatedData] ภายนอก — ยังไม่ executed ใน
repo นี้ ⇒ ยังอ้างไม่ได้จนกว่าจะ re-implement เป็น AP7 พร้อม pytest

## งานต่อ (อัพเดต)

- ~~หา H_quartic~~ ✅ RESOLVED (AP8): H_nl = MΦ̇Ψ̇+KΦL_wΨ+Ψᵀ∇V(Φ)−JᵀΨ — เหลือ Coq lift ของ nonlinear cancellation (รวมกับ general-N)
- Coq general-N + per-node params (ตอนนี้ 3-ring)
- เสนอ DRL เข้า `research_universal_solver` ปิดแถว BORROWED ของ D-term ใน ledger
  ต้นทาง (ผ่าน PR + adversarial audit ของ repo นั้น)
