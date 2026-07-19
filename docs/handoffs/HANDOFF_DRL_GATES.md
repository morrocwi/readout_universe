# HANDOFF — ultracode: DRL three gates (2026-07-19, session e4ff62dd)

**User request (verbatim):** "ทำเลย แบ่งทีม sonnet ทำ ultracode" — สั่งหลังคุยกันว่า
DRL จะเลื่อนขั้นเป็น "สมการแม่" ได้ต้องผ่านสามด่าน: (1) ยกขึ้น Th_coqc,
(2) ขยาย general graph + nonlinear ∇V + forcing J−η, (3) literature falsifier.

**Context ที่ตัดสินแล้ว (อย่า re-litigate):**
- DRL = Discrete Retention Lagrangian, นิยาม+ผลรันใน `v2/DISCRETE_RETENTION_LAGRANGIAN.md`
  + `ap/ap5_drl.py` (merged PR #11, main = 52240d7, suite 39/39)
- โครงสร้าง: doubled X=(Φ,Ψ), G=[[0,1],[1,0]], Ω=[[0,1],[−1,0]];
  action ใน ap5_drl.py คือ ground truth ของ discretization
- Nonlinear design ที่เลือกแล้ว: U_cross = Ψᵀ∇V(Φ) − JᵀΨ (CTP-style) —
  EL_Ψ ให้สมการหน่วง + ∇V(Φ) − J; EL_Φ ให้ Ψ-eq กับ Hessian ∇²V(Φ)Ψ
- ประจุ H มี drift O(dt²) (ไม่ exact) — Coq จึงห้ามอ้าง exact conservation ของ
  discretization นี้; เป้า Coq ที่ทำได้จริง: EL-identity (พีชคณิต) + D-cancellation ใน H
- วินัย: tier-honest, toy scope ประกาศ, ห้าม overclaim, ทุกตัวเลข executed,
  workers = sonnet เท่านั้น (Fable = orchestrator อย่างเดียว)

**Run:** workflow "drl-three-gates" — **runId `wf_ddeca0cf-fbb`**, script persisted at
`~/.claude/projects/-home-yaoharee-lt-ANSE-ASIA-readout-universe/e4ff62dd-.../workflows/scripts/drl-three-gates-wf_ddeca0cf-fbb.js`
— resume: `Workflow({scriptPath: <ไฟล์ข้างบน>, resumeFromRunId: "wf_ddeca0cf-fbb"})`;
เช็คว่าจบแล้วหรือยัง: journal.jsonl ใน transcript dir `subagents/workflows/wf_ddeca0cf-fbb`

**Workers เขียนไฟล์บน branch `feat/drl-gates`** (สร้างก่อน launch):
- Gate1 Coq → `evidence/DRL_Discrete.v` (ห้ามแตะไฟล์อื่น)
- Gate2 General → `ap/ap6_drl_general.py` (ห้ามแตะ ap5)
- Gate3 Literature → รายงานกลับเป็น structured output เท่านั้น (ไม่เขียนไฟล์)

**ห้ามทำ:** push/merge (main loop ทำผ่าน PR+review เท่านั้น), แก้ v1.0 files,
แตะ repo อื่น, ประกาศ novelty โดยไม่มี citation

**Next step หลัง workflow คืนผล:** main loop integrate → update
DISCRETE_RETENTION_LAGRANGIAN.md + VERIFIED_RUNS + ROADMAP → PR → adversarial
review → merge → sync both remotes → memory update
