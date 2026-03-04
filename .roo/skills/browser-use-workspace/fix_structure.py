"""
Fix directory structure and grading.json format to match aggregate_benchmark.py expectations.

Expected structure:
  iteration-1/eval-N-name/with_skill/run-1/grading.json
  iteration-1/eval-N-name/without_skill/run-1/grading.json

grading.json must include a 'summary' field with pass_rate, passed, failed, total.
"""
import json
from pathlib import Path

ITER_DIR = Path(__file__).parent / "iteration-1"

def compute_summary(expectations: list) -> dict:
    passed = sum(1 for e in expectations if e.get("passed", False))
    total = len(expectations)
    failed = total - passed
    return {
        "pass_rate": round(passed / total, 4) if total else 0.0,
        "passed": passed,
        "failed": failed,
        "total": total
    }

fixed = 0
for eval_dir in sorted(ITER_DIR.glob("eval-*")):
    if not eval_dir.is_dir():
        continue
    for config_dir in [eval_dir / "with_skill", eval_dir / "without_skill"]:
        if not config_dir.is_dir():
            continue
        grading_path = config_dir / "grading.json"
        if not grading_path.exists():
            print(f"  SKIP (no grading.json): {config_dir}")
            continue

        # Read existing grading data
        with open(grading_path) as f:
            grading = json.load(f)

        expectations = grading.get("expectations", [])
        summary = compute_summary(expectations)

        # Build updated grading with summary field
        updated_grading = {
            "summary": summary,
            "expectations": expectations
        }

        # Create run-1 subdirectory and write grading.json there
        run_dir = config_dir / "run-1"
        run_dir.mkdir(exist_ok=True)
        run_grading_path = run_dir / "grading.json"
        with open(run_grading_path, "w") as f:
            json.dump(updated_grading, f, indent=2)

        print(f"  Fixed: {run_grading_path} — pass_rate={summary['pass_rate']} ({summary['passed']}/{summary['total']})")
        fixed += 1

print(f"\nDone. Fixed {fixed} grading files.")
