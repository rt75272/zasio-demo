import csv

def validate_record(row):
    required = ["Record_ID", "Category", "Retention_Years", "Owner"]
    for field in required:
        if not row.get(field):
            return False, f"Missing {field}"
    try:
        int(row["Retention_Years"])
    except ValueError:
        return False, "Retention_Years must be numeric"
    return True, "OK"

def validate_csv(csv_file):
    valid_records = []
    errors = []

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            valid, message = validate_record(row)
            if valid:
                valid_records.append(row)
            else:
                errors.append({"Record": row, "Error": message})
    return valid_records, errors
