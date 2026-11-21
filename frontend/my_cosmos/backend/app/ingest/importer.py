import csv
import json
from pathlib import Path

from app.ingest.normalize import (
    clean_text,
    normalize_country,
    normalize_title,
    normalize_doi,
)


def import_papers(csv_path):
    csv_path = Path(csv_path)

    papers = []
    seen_dois = set()
    seen_titles = set()

    report = {
        "rows_in": 0,
        "papers_out": 0,
        "skipped_no_abstract": 0,
        "duplicates_removed": 0,
        "countries_without_iso_code": {},
        "topics_outside_taxonomy": {},
    }

    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            report["rows_in"] += 1

            title = clean_text(row.get("title"))
            abstract = clean_text(row.get("abstract"))
            doi = normalize_doi(row.get("doi"))
            country = normalize_country(row.get("affiliation_country"))

            if not abstract:
                report["skipped_no_abstract"] += 1
                continue

            normalized_title = normalize_title(title)

            if doi and doi in seen_dois:
                report["duplicates_removed"] += 1
                continue

            if normalized_title and normalized_title in seen_titles:
                report["duplicates_removed"] += 1
                continue

            if doi:
                seen_dois.add(doi)

            if normalized_title:
                seen_titles.add(normalized_title)

            institutions = clean_text(row.get("institutions"))
            topics = clean_text(row.get("topics"))
            methods = clean_text(row.get("methods"))

            paper = {
                "paper_id": clean_text(row.get("id")),
                "title": title,
                "abstract": abstract,
                "year": clean_text(row.get("year")) or clean_text(row.get("date"))[:4],
                "doi": doi,
                "country": country,
                "institutions": [
                    item.strip()
                    for item in institutions.split(";")
                    if item.strip()
                ],
                "topics": [
                item.strip()
                for item in topics.replace("|", ";").split(";")
                if item.strip()
                ],
                "methods": [
                    item.strip()
                    for item in methods.split(";")
                    if item.strip()
                ],
            }

            papers.append(paper)

    report["papers_out"] = len(papers)

    return papers, report


def save_papers(papers, output_path):
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    file_path = output_path / "papers.json"

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(papers, file, indent=2, ensure_ascii=False)

    return file_path