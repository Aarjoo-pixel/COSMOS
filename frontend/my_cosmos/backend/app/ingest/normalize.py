import re


def clean_text(value):
    """Remove extra spaces and handle missing values."""
    if value is None:
        return ""

    value = str(value).strip()

    if value.lower() in {"", "nan", "none", "null"}:
        return ""

    return re.sub(r"\s+", " ", value)


def normalize_country(country):
    """Normalize common country name variations."""
    country = clean_text(country)

    country_aliases = {
        "usa": "United States",
        "u.s.": "United States",
        "u.s.a.": "United States",
        "us": "United States",
        "united states of america": "United States",
        "uk": "United Kingdom",
        "u.k.": "United Kingdom",
    }

    return country_aliases.get(country.lower(), country)


def normalize_title(title):
    """Normalize title for duplicate detection."""
    title = clean_text(title).lower()

    # Remove punctuation and special characters
    title = re.sub(r"[^\w\s]", "", title)

    # Remove extra spaces
    title = re.sub(r"\s+", " ", title)

    return title.strip()


def normalize_doi(doi):
    """Normalize DOI for duplicate detection."""
    doi = clean_text(doi).lower()

    doi = doi.replace("https://doi.org/", "")
    doi = doi.replace("http://doi.org/", "")
    doi = doi.replace("https://dx.doi.org/", "")
    doi = doi.replace("http://dx.doi.org/", "")

    return doi.strip()