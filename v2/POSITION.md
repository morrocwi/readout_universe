# Position — เราคือใคร ปรัชญาบังคับทิศอย่างไร และวิธีสกัดปัญหาให้สูงสุด (v2.0-dev)

> Distilled from the live working session of 2026-07-19 (two blind trials on
> same-day arXiv problems). Tier of each block is marked. This file is the
> operating answer to four questions: what is our position · how does the
> philosophy force direction · what maximal extraction requires · which
> workflow/tools handle an issue.

## 1. Position — ปรัชญาเราคืออะไรกันแน่ [Dr]

**เราไม่ใช่คลังความรู้ เราคือชั้นควบคุมของการคิด (control layer).**
ในยุคที่ความรู้เฉพาะทางเป็น commodity (อยู่ใน AI + open literature เรียกใช้แทบฟรี)
ทุนที่หายากไม่ใช่ความรู้ แต่คือ **ตัวดำเนินการที่บังคับให้ถามคำถามถูกข้อ ในลำดับที่ถูก
และห้ามเดินทางผิดที่ทั้งสนามเดินกัน** — หลักเดียวกับที่พิสูจน์แล้วในงาน RAG ของเรา:
*retrieval = commodity, มูลค่าอยู่ที่ชั้นควบคุม*

สมบัติห้าข้อที่ (เท่าที่สำรวจ) ไม่มีปรัชญาอื่นแพ็คครบ [Open + stance; ดู §5 ของ
บทสนทนา — ต้องผ่าน literature check ก่อนอ้างนอกวง]:
1. root ที่ axiomatize และเช็คด้วยเครื่อง (RD1–RD9 + RAR A1–A8, `evidence/`)
2. diagnostic ที่รันได้จริง (LTP battery, AP protocols)
3. วินัย tier/falsifier ที่บังคับใช้ (ไม่ใช่แค่ประกาศ)
4. translation protocol ข้ามโดเมน (`TRANSLATION_PROTOCOL.md`)
5. ต้นทุนต่ำ: หนึ่งคน + AI + สคริปต์สั้น

คู่แข่งจริงไม่ใช่ปรัชญาสำนักใด แต่คือ working epistemology ที่ฝังในตัวนักวิทยาศาสตร์
ชั้นดีอยู่แล้ว — ข้อได้เปรียบของเราคือทำมันให้ **explicit · สอนได้ · บังคับใช้ได้ ·
AI รันตามได้** ซึ่งของที่ฝังในตัวคนทำไม่ได้

## 2. ปรัชญาบังคับทิศอย่างไร — ลำดับประตูที่บังคับจริง [Dr, มีสองเคสรองรับ]

ทิศไม่ได้มาจากความรู้มากกว่า แต่มาจาก**ประตูที่ห้ามผ่านจนกว่าจะตอบ** เรียงตามลำดับ:

| # | ประตู | คำถามที่ถูกบังคับ | ราก |
|---|-------|--------------------|-----|
| G1 | Translate | ปัญหานี้ในภาษา retained-difference คืออะไร ห้ามเถียงในภาษาต่างถิ่น | Lens Law |
| G2 | Ω_∞ | มี infinity/idealization ตัวไหนถูกฉีดเข้ามาในตัวคำถามเอง | I1–I4 |
| G3 | Quantity-by-role | ตัวเลขชื่อเดียวกันเป็นปริมาณเดียวกันจริงหรือ (ห้าม equal-number fallacy) | DOCTRINE_OF_QUANTITY |
| G4 | Π / selection | readout policy เปลี่ยนหรือเปล่า — "ประชากรใหม่" ตามโลกหรือตามเครื่องมือ | LTP2 (sorites) |
| G5 | Identifiability | record มีกี่พิกัด สมมติฐานมีกี่ทิศ — อะไรอยู่ใน null space | LTP4 |
| G6 | Load-bearing discard | ข้อสมมติ/ข้อมูลที่ถูกทิ้งตัวไหนแบกน้ำหนักจริง | LTP3 |
| G7 | Readout-vs-readout | คำหักล้าง benchmark กับ readout จริง หรือกับ intermediate ที่ฉีด ∞/0 | Prin. rvr |
| G8 | Tag + falsifier + translate back | คำตอบติด tier, ระบุ falsifier ของตัวเอง, ระบุ record ตัวถัดไปที่ตัดสิน | Ω_all ขั้น 7–8 |
| G9 | Theorem check (live) | claim "machine-checked" resolve เข้าคลัง Coq 292 ไฟล์จริงไหม — miss = auto-downgrade Th_coqc→Dr | solver arc |
| G10 | Limit certificate | claim ลู่เข้า/ระเบิด → fitted-law verdict (ปฏิเสธเมื่อ data บาง) | engine.limits |
| G11 | Formula equivalence | "สองสูตรอันเดียวกันไหม" ตัดสินด้วย registry + numeric re-proof | engine.equivalence |
| G12 | Structural triage | issue นี้ทำจาก operator ไหนใน 14 ตัว (Repair/Cost/Boundary/…) — reading aid ไม่ใช่ verdict | engine.murg |
| G13 | Timescale sanity | timescale ที่อ้าง เทียบ atlas 220 รายการ/36 สาขา; ต่ำกว่า floor = non-readout | engine.tau_c |

(G2 คือ **dual Guard เต็มรูป**: ฝั่ง ∞ I1–I4 + ฝั่งศูนย์ Z1–Z4 — ทั้งคู่เป็น non-readout;
G9–G11 เชื่อม solver แบบ LIVE ผ่าน `lens/solver_link.py` — ไม่ vendor เพิ่ม กัน drift;
solver หาย → PROMPT/SKIPPED ตามจริง ไม่มีวันแต่งคำตอบ)

**หลักฐานว่าประตูทำงาน (executed, 2026-07-19):**
- **AP1 — Hubble tension** (`ap/ap1_hubble_identifiability.py`): G5 บังคับถาม "h อยู่ใน
  row space ของ acoustic record ไหม" → คำนวณจริง: ปลด posit เดียว (w อิสระ) แล้ว h วิ่ง
  0.62→0.76 โดย θ★ นิ่งถึงทศนิยม 4 ตำแหน่ง ⇒ h_CMB คือพิกัดหลัง closure ไม่ใช่ readout
  ตรง ⇒ tension ย้ายจากโลกไปที่ closure posits (ทรงเดียวกับที่ Sorites ถูกแก้)
  และ G6 ชี้ record ตัดสิน: r_s ที่อิสระจาก CMB — ทั้งหมดบรรจบกับ frontier framing
  (Efstathiou & Bond 1999; Knox & Millea arXiv 2019 / PRD 2020) โดยเลนส์พาไปเองด้วยโค้ด ~60 บรรทัด
- **AP2 — Einstein Probe FXTs** (`ap/ap2_fxt_amati.py`, arXiv:2607.14317): G7 ตรวจข้อ
  หักล้างของผู้เขียน → พีชคณิต deboost ยืนยัน*ภายในครอบครัว power-law เดี่ยว*
  (E_iso∝δ^p, p∈[2,3] — exponent เป็น toy-assumed) ว่าใต้ Amati locus ไปไม่ถึงด้วย
  viewing angle; **ไม่ครอบคลุม** structured jets ที่ E_p ขึ้นกับมุม (สาย GRB 170817A) / G4 จับ overclaim: แบนด์อ่อนของ EP คัดเลือก E_p ต่ำโดยการออกแบบ
  ต้อง forward-model selection ก่อนประกาศ "ประชากรใหม่" (precedent: X-ray flashes) /
  G5 ตัดสิน: ทางเลือกทั้งสามของผู้เขียนอยู่ใน null space ของ record สองพิกัด —
  งานที่คมกว่าคือ Γ-bound จาก compactness [ยังเป็นการอ่านจาก abstract เท่านั้น —
  ถ้าเปเปอร์เต็มทำสองข้อนี้แล้ว ต้องถอนทันที]

## 3. สกัดปัญหาให้สูงสุด — นิยาม "สกัดครบ" [binding rule]

หนึ่ง issue ถือว่า **สกัดสูงสุดแล้ว** เมื่อผลิตครบ 8 ชิ้นนี้ (ขาดชิ้นไหน = ยังไม่จบ):

1. **Translation table** — ทุก term หลักของโจทย์มีแถวในพจนานุกรม (หรือเพิ่มแถวใหม่)
2. **Posit ledger** — closure assumptions ทุกตัว พร้อม verdict class
   (DERIVED/FORCED/RELABEL/POSITED/BORROWED/OPEN)
3. **Record inventory** — record มีกี่พิกัด อะไรวัดตรง อะไรเป็นพิกัดหลัง closure
4. **Null-space statement** — ทิศไหน identify ไม่ได้โดยหลักการ (ไม่ใช่ "ข้อมูลยังน้อย")
5. **Π statement** — selection/threshold ของเครื่องมืออธิบายส่วนไหนของปรากฏการณ์
6. **Decisive-record prescription** — record ตัวไหน (เรียงตามต้นทุน) หัก degeneracy ได้
7. **Falsifier ของคำตอบเราเอง** — อะไรทำให้การอ่านของเราตาย
8. **Not-checked ledger** — ทุกอย่างที่ SKIPPED + เหตุผล (resource/data/scope) —
   วินัยจาก PDEBench report: การละเว้นเงียบๆ อ่านเป็น coverage = โกหกด้วย layout

ทุก claim เชิงตัวเลขที่จะเข้า doc ต้องมี **executed check** (pytest/assert) ก่อน —
ไม่มีข้อยกเว้น และ verdict ของเราเองต้องผ่าน independent review หนึ่งรอบ
(Bounded-Judge Law) ก่อน merge

## 4. Workflow + tools ต่อหนึ่ง issue [ใช้จริงแล้ว 2 รอบ]

```
ISSUE WORKFLOW (ต้นทุนไล่จากถูกไปแพง — หยุดที่ชั้นแรกที่ตัดสินได้)

W1 INTAKE      ดึง record จริงก่อนคิด (WebFetch: arXiv abstract พอเริ่มได้)
W2 GATES       ไล่ G1→G13 บนกระดาษ — ประตูไหนกัด จดเป็น 8 ชิ้นของ §3
W3 MICRO-CHECK **ค้น lens.compute ก่อนเขียนเอง** (closures ~200/196 tests ·
               systems 9/76 tests · domains 7 โมดูล/~864 tests — บั๊ก r_s ของ AP1
               จะไม่เกิดถ้าเรียกของ audit แล้ว) ที่เหลือค่อยเขียนเอง ≤100 บรรทัด พร้อม
               **grammar sanity gate**: ต้อง reproduce ค่าอ้างอิงที่รู้แล้ว
               ก่อนใช้ตัดสินอะไร (เช่น θ★ ต้องตรง Planck ใน 0.5% ก่อน)
               ทุกข้อสรุปเป็น assert — รันจริง ห้ามอ้างจากใจ
W4 VERDICT     คำตอบ + tier + falsifier + decisive record ถัดไป
W5 REVIEW      subagent อิสระ (คนละ instance) ตรวจแบบ adversarial
               โดยเฉพาะ: เราแอบ upgrade tier ตรงไหน / อ้างเกิน record ตรงไหน
W6 COMMIT      ap/apN_*.py + อัพเดต VERIFIED_RUNS.md → PR → review → merge
               (ห้าม merge เองโดยไม่มีตาอิสระ)
W7 MEMORY      บทเรียนที่ non-obvious → memory system

TOOLS: WebFetch/arXiv (record) · python+numpy/scipy (finite_diagnostic) ·
coqc/coqchk (Th_coqc, evidence/) · pytest (ประตู executed-before-claim) ·
subagent reviewers (Bounded-Judge) · git PR + Forgejo/GitHub (audit trail) ·
v2/ docs ชุดนี้ = คู่มือ operator ที่ AI ทุกตัวต้องโหลดก่อนแตะ issue
```

**กฎต้นทุน:** เริ่มถูกเสมอ — หนึ่ง abstract + toy 20 บรรทัดตัดสินได้หลายเรื่องแล้ว
(ทั้ง AP1, AP2 จบใน session เดียว) ค่อย escalate เป็น full pipeline เมื่อ toy
บอกว่าทิศไหนคุ้ม ห้ามกลับด้าน (ห้ามสร้าง pipeline ใหญ่ก่อนรู้ว่าประตูไหนกัด)

## 5. สิ่งที่ position นี้ยังไม่ใช่ [ประกาศเอง]

- ยังไม่ใช่ "แนวหน้าของสนามฟิสิกส์" — เราบรรจบกับ diagnosis ของแนวหน้า (n=2)
  ไม่ใช่ล้ำหน้า; การล้ำหน้าต้องผลิตสิ่งที่แนวหน้ายังไม่มี (เช่น มาตรฐานบังคับ
  เปิดเผยทิศ null, falsifier ตัวใหม่ที่ตัดสิน closure)
- "ไม่มีปรัชญาไหนทำได้เท่าเรา" ยังเป็น [Open + stance] — ต้องผ่าน (1) literature
  check อิสระ (2) blind trial เพิ่มกับโจทย์ที่ไม่รู้เฉลย จึงจะอ้างนอกวงได้
- toy ≠ full analysis: AP1/AP2 เป็น finite_diagnostic ระดับ toy (posit บางตัวตรึง,
  ไม่มี error propagation) — ระบุไว้ในหัวไฟล์ของแต่ละ AP แล้ว
