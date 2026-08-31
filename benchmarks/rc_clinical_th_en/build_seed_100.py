"""Build 100 bilingual *synthetic seed* items for RC Clinical Separation Eval.

These items are NOT a validated benchmark.  They exist to stress the schema,
annotation protocol, and USR/MSR evaluator before independent human annotation.
Every generated row is marked DRAFT_SYNTHETIC / NEEDS_HUMAN_ADJUDICATION.

Run:
    python3 benchmarks/rc_clinical_th_en/build_seed_100.py

Output:
    benchmarks/rc_clinical_th_en/seed_100.jsonl
"""

from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).with_name("seed_100.jsonl")


def row(idx, domain, source_en, source_th, claim_en, claim_th, rival_en, rival_th,
        gold, rival_type):
    return {
        "id": f"RC-CLIN-{idx:03d}",
        "domain": domain,
        "source_en": source_en,
        "source_th": source_th,
        "claim_en": claim_en,
        "claim_th": claim_th,
        "rival_en": rival_en,
        "rival_th": rival_th,
        "gold_provisional": gold,
        "rival_type": rival_type,
        "rival_origin": "author_seed",
        "construction_status": "DRAFT_SYNTHETIC",
        "annotation_status": "NEEDS_HUMAN_ADJUDICATION",
        "medical_use": "benchmark_only_not_clinical_advice",
    }


def build():
    items = []
    idx = 1

    # 8 LICENSED families x 5 = 40 positive separation controls.
    licensed_families = [
        ("laboratory_measurement", "Lab value {v} is above the stated upper reference limit {t}.",
         "ค่าห้องปฏิบัติการ {v} สูงกว่าขีดบนช่วงอ้างอิงที่ระบุ {t}",
         "The reported value is above the stated reference limit.",
         "ค่าที่รายงานสูงกว่าขีดอ้างอิงที่ระบุ",
         "The reported value is not above the stated reference limit.",
         "ค่าที่รายงานไม่ได้สูงกว่าขีดอ้างอิงที่ระบุ", "direct_contrast"),
        ("diagnostic_testing", "The assay report says '{label}: detected'.",
         "รายงานการทดสอบระบุว่า '{label}: detected'",
         "The assay detected the stated target in this sample.",
         "การทดสอบตรวจพบเป้าหมายที่ระบุในตัวอย่างนี้",
         "The assay did not detect the stated target in this sample.",
         "การทดสอบไม่ได้ตรวจพบเป้าหมายที่ระบุในตัวอย่างนี้", "direct_contrast"),
        ("imaging", "The radiology report states: '{finding} identified'.",
         "รายงานรังสีระบุว่า 'พบ {finding}'",
         "The examination identified the stated imaging finding.",
         "การตรวจพบข้อค้นพบทางภาพที่ระบุ",
         "The examination did not identify the stated imaging finding.",
         "การตรวจไม่พบข้อค้นพบทางภาพที่ระบุ", "direct_contrast"),
        ("screening", "{n} of {N} participants screened positive.",
         "ผู้เข้าร่วม {n} จาก {N} คนมีผลคัดกรองบวก",
         "The reported screening-positive proportion is {pct}%.",
         "สัดส่วนผลคัดกรองบวกที่รายงานคือ {pct}%",
         "The reported screening-positive proportion is 0%.",
         "สัดส่วนผลคัดกรองบวกที่รายงานคือ 0%", "direct_contrast"),
        ("epidemiology", "The cohort reports RR {rr} for exposed versus unexposed participants.",
         "cohort รายงาน RR {rr} สำหรับกลุ่มสัมผัสเทียบไม่สัมผัส",
         "The reported relative risk is greater than 1.",
         "relative risk ที่รายงานมากกว่า 1",
         "The reported relative risk is less than 1.",
         "relative risk ที่รายงานน้อยกว่า 1", "direct_contrast"),
        ("prognosis", "A prognostic model outputs {risk}% five-year risk under the stated inputs.",
         "โมเดลพยากรณ์ให้ความเสี่ยง 5 ปี {risk}% ภายใต้ input ที่ระบุ",
         "The model output is {risk}% under those inputs.",
         "model output คือ {risk}% ภายใต้ input เหล่านั้น",
         "The model output is 0% under those inputs.",
         "model output คือ 0% ภายใต้ input เหล่านั้น", "direct_contrast"),
        ("guideline_policy", "A hospital policy sets an alert threshold at {t}; the recorded value is {v}.",
         "นโยบายโรงพยาบาลกำหนด alert threshold ที่ {t}; ค่าที่บันทึกคือ {v}",
         "The recorded value crosses the stated alert threshold.",
         "ค่าที่บันทึกข้าม alert threshold ที่ระบุ",
         "The recorded value is below the stated alert threshold.",
         "ค่าที่บันทึกต่ำกว่า alert threshold ที่ระบุ", "policy_vs_evidence"),
        ("clinical_document_ai", "The note says: '{a} remains possible; {b} is less likely but not excluded.'",
         "บันทึกระบุว่า '{a} ยังเป็นไปได้; {b} น่าจะน้อยกว่าแต่ยังไม่ตัดออก'",
         "The note preserves both alternatives while favoring {a}.",
         "บันทึกยังคงทั้งสองทางเลือกแต่ให้น้ำหนัก {a} มากกว่า",
         "The note definitively rules out {b}.",
         "บันทึกตัด {b} ออกอย่างเด็ดขาด", "explicit_alternative"),
    ]

    vals = [
        {"v": "5.2", "t": "5.1", "label": "target A", "finding": "a 4 mm nodule", "n": 50, "N": 1000, "pct": 5, "rr": "1.8", "risk": 10, "a": "viral infection", "b": "bacterial infection"},
        {"v": "12.1", "t": "12.0", "label": "marker B", "finding": "a small effusion", "n": 24, "N": 400, "pct": 6, "rr": "1.4", "risk": 15, "a": "diagnosis A", "b": "diagnosis B"},
        {"v": "38.2", "t": "38.0", "label": "organism C", "finding": "a focal opacity", "n": 30, "N": 500, "pct": 6, "rr": "2.1", "risk": 25, "a": "cause A", "b": "cause B"},
        {"v": "1.05", "t": "1.00", "label": "antigen D", "finding": "a 6 mm lesion", "n": 15, "N": 300, "pct": 5, "rr": "1.3", "risk": 35, "a": "syndrome A", "b": "syndrome B"},
        {"v": "7.1", "t": "7.0", "label": "signal E", "finding": "a small cyst", "n": 45, "N": 900, "pct": 5, "rr": "1.6", "risk": 40, "a": "process A", "b": "process B"},
    ]

    for family in licensed_families:
        domain, s_en, s_th, p_en, p_th, q_en, q_th, rtype = family
        for data in vals:
            items.append(row(idx, domain, s_en.format(**data), s_th.format(**data),
                             p_en.format(**data), p_th.format(**data),
                             q_en.format(**data), q_th.format(**data),
                             "LICENSED", rtype))
            idx += 1

    # 8 NOT_IDENTIFIED families x 5 = 40 underdetermination controls.
    unresolved_families = [
        ("laboratory_measurement",
         "A result is close to a decision threshold and the stated measurement uncertainty crosses that threshold.",
         "ผลตรวจอยู่ใกล้ decision threshold และความไม่แน่นอนที่ระบุคร่อม threshold",
         "The measurement definitively places the patient above the threshold.",
         "การวัดจัดผู้ป่วยไว้เหนือ threshold อย่างแน่นอน",
         "Given the stated uncertainty, the target value may lie on either side of the threshold.",
         "เมื่อคำนึงถึงความไม่แน่นอน ค่าของเป้าหมายอาจอยู่ได้ทั้งสองด้านของ threshold",
         "measurement_artifact"),
        ("diagnostic_testing",
         "A test is positive; sensitivity and specificity are supplied but no pre-test probability is given.",
         "ผลตรวจเป็นบวก มี sensitivity และ specificity แต่ไม่มี pre-test probability",
         "The positive test proves the patient has the disease.",
         "ผลบวกพิสูจน์ว่าผู้ป่วยมีโรค",
         "The posterior probability still depends on the missing pre-test probability.",
         "posterior probability ยังขึ้นกับ pre-test probability ที่ขาดอยู่",
         "missing_context"),
        ("imaging",
         "A technically limited study does not visualize the target structure.",
         "การตรวจที่มีข้อจำกัดทางเทคนิคมองไม่เห็นโครงสร้างเป้าหมาย",
         "The structure is absent.",
         "โครงสร้างนั้นไม่มีอยู่",
         "Non-visualization may reflect the technical limitation rather than true absence.",
         "การมองไม่เห็นอาจเกิดจากข้อจำกัดทางเทคนิค ไม่ใช่การไม่มีอยู่จริง",
         "proxy_vs_target"),
        ("medication_safety",
         "A short study reports no serious adverse events in a small sample.",
         "การศึกษาระยะสั้นรายงานว่าไม่พบเหตุการณ์ไม่พึงประสงค์รุนแรงในตัวอย่างขนาดเล็ก",
         "The treatment is safe for all patients.",
         "การรักษาปลอดภัยสำหรับผู้ป่วยทุกคน",
         "The study may be too small and short to establish safety for all patients.",
         "การศึกษาอาจเล็กและสั้นเกินไปที่จะยืนยันความปลอดภัยสำหรับผู้ป่วยทุกคน",
         "insufficient_evidence"),
        ("screening",
         "A screening test is positive but confirmatory diagnosis is not available.",
         "ผลคัดกรองเป็นบวก แต่ยังไม่มีการวินิจฉัยยืนยัน",
         "The person definitely has the disease.",
         "บุคคลนั้นมีโรคอย่างแน่นอน",
         "The positive screen may still be a false positive.",
         "ผลคัดกรองบวกยังอาจเป็น false positive",
         "screen_vs_diagnosis"),
        ("epidemiology",
         "An observational study reports RR 1.8 and states residual confounding is not excluded.",
         "การศึกษาเชิงสังเกตรายงาน RR 1.8 และระบุว่ายังไม่ตัด residual confounding",
         "The exposure caused the outcome.",
         "การสัมผัสเป็นสาเหตุของผลลัพธ์",
         "The observed association could be partly or wholly confounded.",
         "association ที่พบอาจถูก confound บางส่วนหรือทั้งหมด",
         "confounding"),
        ("prognosis",
         "A model outputs a risk estimate but calibration in the patient's population is not reported.",
         "โมเดลให้ risk estimate แต่ไม่ได้รายงาน calibration ในประชากรของผู้ป่วย",
         "The patient's true risk is exactly the model output.",
         "ความเสี่ยงจริงของผู้ป่วยเท่ากับ model output แบบ exact",
         "The model may be miscalibrated in this population.",
         "โมเดลอาจ miscalibrated ในประชากรนี้",
         "model_vs_target"),
        ("statistics_uncertainty",
         "A small study reports a non-significant result with a wide confidence interval.",
         "การศึกษาขนาดเล็กรายงานผลไม่ significant พร้อม confidence interval กว้าง",
         "The study proves there is no meaningful effect.",
         "การศึกษาพิสูจน์ว่าไม่มี effect ที่มีความหมาย",
         "The study may be too imprecise to distinguish no effect from a meaningful effect.",
         "การศึกษาอาจไม่แม่นยำพอที่จะแยก no effect จาก effect ที่มีความหมาย",
         "insufficient_evidence"),
    ]

    for family in unresolved_families:
        domain, s_en, s_th, p_en, p_th, q_en, q_th, rtype = family
        for k in range(5):
            suffix_en = f" (synthetic variant {k+1})"
            suffix_th = f" (ตัวอย่างสังเคราะห์ {k+1})"
            items.append(row(idx, domain, s_en + suffix_en, s_th + suffix_th,
                             p_en, p_th, q_en, q_th,
                             "NOT_IDENTIFIED", rtype))
            idx += 1

    # 4 UNSUPPORTED families x 5 = 20 contradiction/scope controls.
    unsupported_families = [
        ("clinical_document_ai",
         "The note states: 'bacterial infection is not excluded.'",
         "บันทึกระบุว่า 'ยังไม่ตัดการติดเชื้อแบคทีเรียออก'",
         "Bacterial infection is ruled out.",
         "ตัดการติดเชื้อแบคทีเรียออกแล้ว",
         "The note explicitly preserves bacterial infection as possible.",
         "บันทึกระบุให้การติดเชื้อแบคทีเรียยังเป็นไปได้",
         "explicit_alternative"),
        ("guideline_policy",
         "A guideline is explicitly limited to inpatient care.",
         "แนวทางระบุชัดว่าใช้เฉพาะการดูแลผู้ป่วยใน",
         "The guideline automatically governs outpatient care.",
         "แนวทางใช้กับผู้ป่วยนอกโดยอัตโนมัติ",
         "Outpatient application requires an additional scope bridge.",
         "การนำไปใช้กับผู้ป่วยนอกต้องมี scope bridge เพิ่ม",
         "scope_generalization"),
        ("medication_safety",
         "A study excluded pregnant participants.",
         "การศึกษาไม่รับผู้เข้าร่วมที่ตั้งครรภ์",
         "The study directly establishes safety in pregnancy.",
         "การศึกษายืนยันความปลอดภัยในครรภ์โดยตรง",
         "Pregnancy safety is not directly established because that population was excluded.",
         "ความปลอดภัยในครรภ์ไม่ได้รับการยืนยันโดยตรงเพราะประชากรนี้ถูกตัดออก",
         "domain_shift"),
        ("statistics_uncertainty",
         "A report says evidence is 'insufficient to establish causation.'",
         "รายงานระบุว่าหลักฐาน 'ไม่เพียงพอที่จะยืนยัน causation'",
         "The report establishes causation.",
         "รายงานยืนยัน causation",
         "The report explicitly stops short of establishing causation.",
         "รายงานระบุชัดว่ายังไม่ถึงการยืนยัน causation",
         "explicit_alternative"),
    ]

    for family in unsupported_families:
        domain, s_en, s_th, p_en, p_th, q_en, q_th, rtype = family
        for k in range(5):
            suffix_en = f" (synthetic variant {k+1})"
            suffix_th = f" (ตัวอย่างสังเคราะห์ {k+1})"
            items.append(row(idx, domain, s_en + suffix_en, s_th + suffix_th,
                             p_en, p_th, q_en, q_th,
                             "UNSUPPORTED", rtype))
            idx += 1

    assert len(items) == 100
    assert sum(x["gold_provisional"] == "LICENSED" for x in items) == 40
    assert sum(x["gold_provisional"] == "NOT_IDENTIFIED" for x in items) == 40
    assert sum(x["gold_provisional"] == "UNSUPPORTED" for x in items) == 20
    return items


def main():
    items = build()
    OUT.write_text(
        "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in items),
        encoding="utf-8",
    )
    print(f"wrote {len(items)} draft items to {OUT}")


if __name__ == "__main__":
    main()
