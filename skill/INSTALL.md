# Installing the readout-lens skill

## Requirements
- Python 3.10+ with numpy, scipy (pytest to verify)
- A clone of this repo (private): `git clone <origin> readout_universe`

## Install (Claude Code)

**Per-project** (recommended — skill + code travel together):
```bash
cd <your-project>
mkdir -p .claude/skills
ln -s /path/to/readout_universe/skill/readout-lens .claude/skills/readout-lens
```

**Global** (all projects on this machine):
```bash
ln -s /path/to/readout_universe/skill/readout-lens ~/.claude/skills/readout-lens
```

Or run the helper: `bash skill/install.sh [--global]` (from the repo root).

## Verify

```bash
cd /path/to/readout_universe && python3 -m pytest -q   # expect: all passed
```
Then in a Claude Code session: type `/readout-lens` (or mention "วิเคราะห์ด้วยปรัชญาเรา")
— the skill loads and drives the W1–W7 workflow against `lens/gates.py`.

## Update

`git pull` in the repo — the symlink picks up changes; re-run pytest after.

## Layout

```
skill/readout-lens/SKILL.md   the skill (thin operator manual; calls the API)
lens/gates.py                 G1–G8 gates + 7-piece Extraction (the new layer)
lens/vendor/                  snapshot of the verified engine (provenance-tagged)
ap/                           executed case studies (pytest)
v2/POSITION.md                doctrine the skill enforces
```
