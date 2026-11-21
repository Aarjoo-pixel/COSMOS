import json
from pathlib import Path


def save_report(report, output_path):
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    report_file = output_path / "report.json"

    with report_file.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)

    print("\n========== IMPORT REPORT ==========")
    print(f"Rows received       : {report.get('rows_in', 0)}")
    print(f"Papers imported     : {report.get('papers_out', 0)}")
    print(f"Duplicates removed  : {report.get('duplicates_removed', 0)}")
    print(f"Missing abstracts   : {report.get('skipped_no_abstract', 0)}")

    print("\nUnknown countries:")
    print(report.get("countries_without_iso_code", {}))

    print("\nUnknown topics:")
    print(report.get("topics_outside_taxonomy", {}))

    print("\nReport saved to:", report_file)