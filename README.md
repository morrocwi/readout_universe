# Readout Universe — Philosophy and Logic (v1.0 → v2.0-dev "of Everything")

Open-science, reproducible textbook (83 pp.). Author: Yaoharee Lahtee
(ORCID 0009-0005-3861-0626), Open Civil Science Initiative. License: CC BY 4.0.

**v2.0-dev:** this repo is being elevated toward *The Philosophy and Logic of
Everything* — a tier-honest candidacy, never a declared ToE. The governing law of
v2 is the **Lens Law**: every problem, from any domain, is first TRANSLATED into
this book's information-philosophy language and solved inside its logic
(`v2/TRANSLATION_PROTOCOL.md` — Ω_all), with bridges to the machine-checked
physics/biology/AI corpus recorded per-domain in `v2/DOMAIN_LEDGER.md` and release
gates in `v2/ROADMAP_V2.md`. The v1.0 text in `main.tex` is frozen; v2 adds, it
never silently edits.

This repository is the canonical git home of the book so that **any AI or human
can read the full philosophy and logic system directly from source** — no PDF
extraction needed: the complete text lives in [`main.tex`](main.tex) (single file),
with the compiled book in `main.pdf`.

## หลักการและเหตุผล — Principles & Rationale

1. **Position — control layer, not a knowledge store.** ความรู้เฉพาะทางเป็น
   commodity แล้ว ทุนที่แท้คือ*ตัวดำเนินการบังคับทิศ*: ประตู G1–G13 บังคับให้ถาม
   คำถามถูกข้อ ในลำดับที่ถูก และห้ามหลงทางที่ทั้งสนามหลงกัน (`v2/POSITION.md`)
2. **Lens Law.** ทุกปัญหาถูกแปลเข้าภาษาปรัชญาสารสนเทศ (Information DNA: RD1–9 +
   RAR A1–8) ก่อนแก้ — ห้ามเถียงในภาษาต่างถิ่นเกินขั้น 1 (`v2/TRANSLATION_PROTOCOL.md`)
3. **Readout-not-truth + tier discipline.** ทุก claim ติดป้าย
   `Th_coqc / finite_diagnostic / Dr / Open` และไม่มีตัวเลขใดเข้าเอกสารโดยไม่มี
   executed run ประกบ (`docs/VERIFIED_RUNS.md`); ทุก PR ผ่าน adversarial review
4. **ปรัชญา-นำ แล้วสมการตามหลัง — และตรวจแล้วว่าปิดแผลได้จริง (narrow):** สมการที่เกิดจากเลนส์ในบ้านนี้
   - **Φ_FI** = 1 − V*(C∖π)/V*(C) — attribution fraction ของ inter-chain tension
     ต่อ posit ที่มีชื่อ (`v2/EQUATION_FI.md`, AP4)
   - **DRL** — Discrete Retention Lagrangian: RD4 บังคับคู่ reader–record →
     derive พจน์หน่วงจาก action ได้ (Coq: EL-iff ที่ 3-ring — ℝ-version 2 classical
     axioms declared; ℚ-version ใน solver axiom-free) และ**โครงประจุ/D-cancellation
     ปิด axiom-free ที่ general-N** (`DRL_General_Legendre.v` — คนละทฤษฎีบทกัน,
     แยกให้ชัด) + conservation of pairing ทั้งครอบครัว nonlinear
     (`v2/DISCRETE_RETENTION_LAGRANGIAN.md`, AP5/6/8) — และถูกนำเข้า `research_universal_solver` ผ่าน
     audit จน **ledger row 8 (D-term) เปลี่ยน BORROWED → DERIVED-narrow**
     (solver PR #185+#186, audit record: cpg DEC-drl-d-term-ratification-2026-0719)
   - **Tape layer** — append-only record ที่ realize RD4 ใน dynamics + สะพาน
     γ↔D/M เข้า DRL (`v2/APPEND_ONLY_RECORD.md`, AP7)
   - **Forced Identification thesis** — โครงสร้างร่วมของวิกฤตฟิสิกส์ยุคนี้
     (`v2/FORCED_IDENTIFICATION.md`, n=4)
5. **ความใหม่ทุกชิ้น = [Open] จนกว่าผ่าน peer ภายนอก** — kinship ประกาศเสมอ
   (Bateman/CTP/collision models/…) และ falsifier ของทุก claim แขวนไว้ในไฟล์

## For AI readers — start here

1. Read [`docs/AI_READING_GUIDE.md`](docs/AI_READING_GUIDE.md) — entry order, tier
   discipline, and what the book does NOT claim.
2. Read [`main.tex`](main.tex) — the full textbook (plain LaTeX, one file).
3. Read [`CLAIMS.md`](CLAIMS.md) — one falsifiable claim per row, each with its
   check command.

**Tier legend (never collapse):**
`Th_coqc` (machine-checked, axiom-free) ≠ `finite_diagnostic` (verified numeric run)
≠ `Dr` (declared-bridge reading) ≠ `Open` (always carries a stance, never bare).

## Reproduce every claim (~5 minutes)

```
make verify        # LTP1 (expect PASS 3/3), LTP2-4 (expect PASS 8/8),
                   # coqc UPL_Sorites.v (expect exit 0 + 3x "Closed under the global context")
make pdf           # builds main.pdf from main.tex (pdflatex x2)
make all           # verify + pdf
```

Requirements: `make verify` needs Python 3 + numpy, and Coq (8.18+; 8.20.1
verified — see [`docs/VERIFIED_RUNS.md`](docs/VERIFIED_RUNS.md)); `make pdf`
needs TeX Live (pdflatex). The pytest suite (`ap/`, exercised via `lens/`)
additionally needs scipy and sympy — see [`requirements.txt`](requirements.txt)
for the exact floor pins and `python3 -m pytest -q` to run it.

Found a genuine falsification? That is the book working as designed — report it.


## Repository layout

```
main.tex                              full textbook source (single file, canonical)
main.pdf                              compiled book (83 pp.)
CLAIMS.md                             falsifiable-claims register (C1–C7)
Makefile                              verify / pdf / all
code/LTP1_logic_as_residual_flow.py   finite_diagnostic protocol 1  (C1–C3)
code/LTP2_3_4_battery.py              finite_diagnostic protocols 2–4 (C4–C6)
code/UPL_Sorites.v                    Th_coqc formal floor, axiom-free (C7)
docs/AI_READING_GUIDE.md              how an AI should read this system
docs/VERIFIED_RUNS.md                 executed verification log (dated, per machine)
v2/                                   the lens doctrine + equations (DNA, Lens Law,
                                      Doctrine of Quantity, Position, Φ_FI, DRL,
                                      Append-Only Record, Forced-Identification)
ap/                                   executed case studies (pytest; ap0–ap9)
evidence/                             in-repo Coq evidence (RD.v, URCF_RD_All.v,
                                      DRL_Discrete.v, DRL_General_Legendre.v)
```
Note: `lens/`, `skill/`, `ap/` are proprietary (LICENSE EXCEPTIONS), not CC BY.

## We do NOT claim

`finite_diagnostic` = proof; Coq scope beyond monotone g; B1 uniqueness;
Gödel/liar/ethics solved; supersession of any tradition in Part IV;
machine-independent timings.
