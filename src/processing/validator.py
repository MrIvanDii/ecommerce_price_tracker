from typing import Dict, List


REQUIRED_FIELDS = [
    "dealer",
    "product_name",
    "product_url",
    "price",
    "currency",
]


def validate_record(record: Dict) -> Dict:
    missing_fields = []

    for field in REQUIRED_FIELDS:
        value = record.get(field)

        if value is None or value == "":
            missing_fields.append(field)

    if missing_fields:
        record["scrape_status"] = "partial"
        record["error_message"] = (
            "Missing required fields: " + ", ".join(missing_fields)
        )

    return record


def validate_records(records: List[Dict]) -> List[Dict]:
    return [validate_record(record) for record in records]