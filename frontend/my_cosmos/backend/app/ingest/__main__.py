import argparse
import json
from pathlib import Path

from app.ingest.importer import import_papers, save_papers
from app.ingest.report import save_report


def main():
    parser = argparse.ArgumentParser(description="COSMOS CSV Importer")

    parser.add_argument("csv_file", help="Path to input CSV file")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--out", default="data_imported")

    args = parser.parse_args()

    csv_path = Path(args.csv_file)

    if not csv_path.exists():
        print(f"Error: CSV file not found: {csv_path}")
        return

    papers, report = import_papers(csv_path)

    print("\nImport completed.")

    if args.dry_run:
        print("\nDry run: nothing written.")
        print("\nReport:")
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return

    output_path = Path(args.out)

    save_papers(papers, output_path)
    save_report(report, output_path)

    print("\nImport successful!")


if __name__ == "__main__":
    main()