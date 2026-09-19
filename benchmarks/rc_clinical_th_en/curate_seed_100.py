"""Curate the raw 100-item RC clinical seed into an annotation candidate.

The raw builder deliberately stress-tests counts/schema and historically used
literal ``synthetic variant`` suffixes for some families.  That is not good
enough for human annotation: disguised duplicates can inflate apparent sample
size without adding a new readout context.

This module performs a conservative curation pass:

* remove the literal variant markers;
* add one materially interpretable, label-preserving context clause per raw
  variant instead of a cosmetic number;
* add empty human-annotation/adjudication fields;
* reject duplicate (source, claim, rival) triples;
* preserve the provisional 40/40/20 label balance.

It does NOT validate rival quality.  ``gold_provisional`` remains author-seeded
until independent human annotation and adjudication.

Run:
    python3 benchmarks/rc_clinical_th_en/curate_seed_100.py

Output:
    benchmarks/rc_clinical_th_en/candidate_100.jsonl
"""

from __future__ import annotations

import importlib.util
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

HERE = Path(__file__).resolve().parent
RAW_BUILDER = HERE / "build_seed_100.py"
OUT = HERE / "candidate_100.jsonl"


def _load_raw_builder():
    spec = importlib.util.spec_from_file_location("rc_raw_seed_builder", RAW_BUILDER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


_CONTEXTS = {
    ("NOT_IDENTIFIED", "laboratory_measurement"): [
        ("No correction model beyond the stated uncertainty is supplied.",
         "ไม่มี correction model นอกเหนือจากความไม่แน่นอนที่ระบุ"),
        ("No independent repeat measurement is included in the excerpt.",
         "ข้อความที่ให้มาไม่มีการวัดซ้ำแบบอิสระ"),
        ("The excerpt gives no evidence that uncertainty is one-sided.",
         "ข้อความที่ให้มาไม่มีหลักฐานว่าความไม่แน่นอนอยู่ด้านเดียว"),
        ("No calibration update resolving the threshold crossing is supplied.",
         "ไม่มี calibration update ที่แก้ความกำกวมบริเวณ threshold"),
        ("The report supplies no additional measurement capable of separating the two sides of the threshold.",
         "รายงานไม่มีการวัดเพิ่มเติมที่สามารถแยกสองด้านของ threshold"),
    ],
    ("NOT_IDENTIFIED", "diagnostic_testing"): [
        ("No prior odds are supplied elsewhere in the excerpt.",
         "ไม่มี prior odds ให้ไว้ในส่วนอื่นของข้อความ"),
        ("No prevalence estimate for the tested population is provided.",
         "ไม่มี prevalence estimate สำหรับประชากรที่ตรวจ"),
        ("The excerpt contains no patient-specific baseline risk estimate.",
         "ข้อความไม่มี baseline risk estimate เฉพาะผู้ป่วย"),
        ("No independent confirmatory result is included.",
         "ไม่มีผลยืนยันแบบอิสระรวมอยู่"),
        ("The report gives no decision rule converting the test readout into a categorical diagnosis.",
         "รายงานไม่มี decision rule ที่แปลงผลตรวจเป็น diagnosis แบบ categorical"),
    ],
    ("NOT_IDENTIFIED", "imaging"): [
        ("No higher-quality repeat study is included.", "ไม่มีการตรวจซ้ำคุณภาพสูงกว่ารวมอยู่"),
        ("No alternative imaging sequence is supplied.", "ไม่มี imaging sequence ทางเลือกให้ไว้"),
        ("The technical limitation remains unresolved in the supplied record.", "ข้อจำกัดทางเทคนิคยังไม่ถูกแก้ใน record ที่ให้มา"),
        ("No independent modality confirms absence.", "ไม่มี modality อิสระที่ยืนยันการไม่มีอยู่"),
        ("The excerpt contains no follow-up image resolving the non-visualization.", "ข้อความไม่มีภาพติดตามที่แก้ปัญหาการมองไม่เห็น"),
    ],
    ("NOT_IDENTIFIED", "medication_safety"): [
        ("No larger safety registry is cited.", "ไม่มีการอ้าง registry ความปลอดภัยขนาดใหญ่กว่า"),
        ("No longer-term follow-up is supplied.", "ไม่มีข้อมูลติดตามระยะยาวกว่า"),
        ("The excerpt contains no evidence about rare-event detection power.", "ข้อความไม่มีหลักฐานเรื่อง power สำหรับตรวจเหตุการณ์ที่พบได้น้อย"),
        ("No external population bridge is provided.", "ไม่มี population bridge ภายนอกให้ไว้"),
        ("No independent post-marketing safety source is included.", "ไม่มีแหล่งความปลอดภัยหลังวางตลาดแบบอิสระรวมอยู่"),
    ],
    ("NOT_IDENTIFIED", "screening"): [
        ("No confirmatory result is included.", "ไม่มีผลตรวจยืนยันรวมอยู่"),
        ("The excerpt contains no diagnostic gold-standard result.", "ข้อความไม่มีผล diagnostic gold standard"),
        ("No follow-up assessment resolving false-positive status is supplied.", "ไม่มีการประเมินติดตามที่แก้สถานะ false positive"),
        ("The screening result is the only stated access route.", "ผลคัดกรองเป็น access route เดียวที่ระบุ"),
        ("No second-stage diagnostic record is available in the excerpt.", "ไม่มี record การวินิจฉัยขั้นที่สองในข้อความ"),
    ],
    ("NOT_IDENTIFIED", "epidemiology"): [
        ("No negative-control exposure analysis is supplied.", "ไม่มี negative-control exposure analysis ให้ไว้"),
        ("No sensitivity analysis for unmeasured confounding is reported.", "ไม่มี sensitivity analysis สำหรับ unmeasured confounding"),
        ("No randomized assignment is present in the described design.", "design ที่อธิบายไม่มี randomized assignment"),
        ("The excerpt gives no independent intervention evidence.", "ข้อความไม่มีหลักฐาน intervention แบบอิสระ"),
        ("No additional record closes the stated confounding route.", "ไม่มี record เพิ่มเติมที่ปิดเส้นทาง confounding ที่ระบุ"),
    ],
    ("NOT_IDENTIFIED", "prognosis"): [
        ("No calibration table for this target population is included.", "ไม่มี calibration table สำหรับประชากรเป้าหมายนี้"),
        ("No external-validation result is supplied.", "ไม่มีผล external validation ให้ไว้"),
        ("The excerpt gives no calibration intercept or slope for the deployment population.", "ข้อความไม่มี calibration intercept หรือ slope สำหรับประชากรใช้งาน"),
        ("No local recalibration result is available.", "ไม่มีผล local recalibration"),
        ("No independent outcome follow-up is included in the supplied record.", "ไม่มี outcome follow-up แบบอิสระใน record ที่ให้มา"),
    ],
    ("NOT_IDENTIFIED", "statistics_uncertainty"): [
        ("No equivalence margin is specified.", "ไม่มีการระบุ equivalence margin"),
        ("No non-inferiority margin is supplied.", "ไม่มี non-inferiority margin ให้ไว้"),
        ("The excerpt contains no precision target that would license a no-effect conclusion.", "ข้อความไม่มี precision target ที่จะรองรับข้อสรุป no-effect"),
        ("No additional study narrows the uncertainty interval.", "ไม่มีการศึกษาเพิ่มเติมที่ทำให้ uncertainty interval แคบลง"),
        ("The record contains no power analysis showing the relevant alternative was detectably separated.", "record ไม่มี power analysis ที่แสดงว่าแยกทางเลือกที่เกี่ยวข้องได้"),
    ],
    ("UNSUPPORTED", "clinical_document_ai"): [
        ("The quoted assessment is the only supplied note fragment.", "assessment ที่ยกมาเป็นส่วนบันทึกเดียวที่ให้ไว้"),
        ("No later note reverses the quoted assessment.", "ไม่มีบันทึกภายหลังที่กลับ assessment ที่ยกมา"),
        ("The excerpt contains no rule-out statement elsewhere.", "ข้อความไม่มีคำตัดโรคออกในส่วนอื่น"),
        ("No supplementary document changes the stated differential.", "ไม่มีเอกสารเสริมที่เปลี่ยน differential ที่ระบุ"),
        ("The supplied record preserves the quoted alternative without contradiction.", "record ที่ให้มายังคงทางเลือกที่ยกมาโดยไม่มีข้อความขัดแย้ง"),
    ],
    ("UNSUPPORTED", "guideline_policy"): [
        ("No extension clause is provided.", "ไม่มี extension clause ให้ไว้"),
        ("No cross-setting validation is cited.", "ไม่มีการอ้าง cross-setting validation"),
        ("The excerpt contains no exception expanding the declared scope.", "ข้อความไม่มีข้อยกเว้นที่ขยายขอบเขตที่ประกาศ"),
        ("No institutional rule supplies the missing bridge.", "ไม่มีกฎสถาบันที่ให้ bridge ที่ขาด"),
        ("The stated scope restriction remains operative in the supplied text.", "ข้อจำกัดขอบเขตที่ระบุยังมีผลในข้อความที่ให้มา"),
    ],
    ("UNSUPPORTED", "medication_safety"): [
        ("No bridging study for the excluded population is cited.", "ไม่มีการอ้าง bridging study สำหรับประชากรที่ถูกตัดออก"),
        ("No external source fills the population gap.", "ไม่มีแหล่งภายนอกเติมช่องว่างของประชากร"),
        ("The exclusion criterion is explicit in the supplied study description.", "exclusion criterion ระบุชัดในคำอธิบายการศึกษา"),
        ("No subgroup evidence overturns the exclusion-based limitation.", "ไม่มี subgroup evidence ที่ลบข้อจำกัดจาก exclusion"),
        ("The supplied record contains no access route to the excluded population.", "record ที่ให้มาไม่มี access route ไปยังประชากรที่ถูกตัดออก"),
    ],
    ("UNSUPPORTED", "statistics_uncertainty"): [
        ("No later confirmatory statement is included.", "ไม่มีข้อความยืนยันภายหลังรวมอยู่"),
        ("The quoted qualification remains unmodified in the supplied record.", "qualification ที่ยกมายังไม่ถูกแก้ใน record"),
        ("No supplementary analysis upgrades the stated evidential status.", "ไม่มี analysis เสริมที่ยกระดับสถานะหลักฐานที่ระบุ"),
        ("The excerpt supplies no stronger conclusion elsewhere.", "ข้อความไม่มีข้อสรุปที่แรงกว่านี้ในส่วนอื่น"),
        ("No additional source reverses the explicit limitation.", "ไม่มีแหล่งเพิ่มเติมที่กลับข้อจำกัดที่ระบุชัด"),
    ],
}

_VARIANT_RE_EN = re.compile(r"\s*\(synthetic variant \d+\)\s*$")
_VARIANT_RE_TH = re.compile(r"\s*\(ตัวอย่างสังเคราะห์ \d+\)\s*$")


def curate() -> List[Dict]:
    raw = _load_raw_builder().build()
    counters = defaultdict(int)
    out: List[Dict] = []

    for original in raw:
        item = dict(original)
        key = (item["gold_provisional"], item["domain"])
        if key in _CONTEXTS:
            i = counters[key]
            if i >= len(_CONTEXTS[key]):
                raise AssertionError(f"not enough contexts for {key}")
            add_en, add_th = _CONTEXTS[key][i]
            counters[key] += 1
            base_en = _VARIANT_RE_EN.sub("", item["source_en"]).strip()
            base_th = _VARIANT_RE_TH.sub("", item["source_th"]).strip()
            item["source_en"] = f"{base_en} {add_en}"
            item["source_th"] = f"{base_th} {add_th}"

        item.update(
            {
                "rival_quality_r1": None,
                "rival_quality_r2": None,
                "rival_quality_r3": None,
                "rival_quality_r4": None,
                "claim_compatible_annotator_1": None,
                "rival_compatible_annotator_1": None,
                "claim_compatible_annotator_2": None,
                "rival_compatible_annotator_2": None,
                "rival_quality": None,
                "translation_equivalence": None,
                "adjudicated_label": None,
                "adjudication_rationale": None,
                "annotator_1_id": None,
                "annotator_2_id": None,
                "adjudicator_id": None,
            }
        )
        out.append(item)

    _validate_candidate(out)
    return out


def _validate_candidate(items: List[Dict]) -> None:
    assert len(items) == 100
    counts = {label: sum(x["gold_provisional"] == label for x in items)
              for label in ("LICENSED", "NOT_IDENTIFIED", "UNSUPPORTED")}
    assert counts == {"LICENSED": 40, "NOT_IDENTIFIED": 40, "UNSUPPORTED": 20}

    ids = [x["id"] for x in items]
    assert len(ids) == len(set(ids))

    triples_en = [(x["source_en"], x["claim_en"], x["rival_en"]) for x in items]
    triples_th = [(x["source_th"], x["claim_th"], x["rival_th"]) for x in items]
    assert len(triples_en) == len(set(triples_en))
    assert len(triples_th) == len(set(triples_th))

    for item in items:
        assert "synthetic variant" not in item["source_en"].lower()
        assert "ตัวอย่างสังเคราะห์" not in item["source_th"]
        assert item["claim_en"] != item["rival_en"]
        assert item["claim_th"] != item["rival_th"]
        assert item["annotation_status"] == "NEEDS_HUMAN_ADJUDICATION"


def main() -> None:
    items = curate()
    OUT.write_text(
        "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in items),
        encoding="utf-8",
    )
    print(f"wrote {len(items)} curated draft items to {OUT}")


if __name__ == "__main__":
    main()
