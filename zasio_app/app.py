from flask import Flask, render_template, request
import os
import csv

# Support both package and script execution
try:
    # When imported as a package module (e.g., `python -m zasio_app.app`)
    from .retention_validator import validate_csv
except (ImportError, ValueError):
    # When run directly as a script (e.g., `python app.py`)
    from retention_validator import validate_csv

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        if file is None or file.filename == '':
            return "No file selected", 400
        upload_dir = os.path.join('zasio_app', 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        filepath = os.path.join(upload_dir, file.filename)
        file.save(filepath)
        # Build a raw preview (before validation): headers, limited rows, total count
        preview_limit = 50
        raw_headers: list[str] | list = []
        raw_rows: list[dict] | list = []
        total_rows = 0
        try:
            with open(filepath, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                raw_headers = reader.fieldnames or []
                for i, row in enumerate(reader):
                    total_rows += 1
                    if i < preview_limit:
                        raw_rows.append(row)
        except Exception:
            # If preview fails (encoding, etc.), keep processing validation
            raw_headers, raw_rows, total_rows = [], [], 0

        valid_records, errors = validate_csv(filepath)
        return render_template(
            'results.html',
            file_name=file.filename,
            raw_headers=raw_headers,
            raw_rows=raw_rows,
            total_rows=total_rows,
            preview_limit=preview_limit,
            valid_records=valid_records,
            errors=errors,
        )
    return render_template('upload.html')

# Keep old path working; support POST too and reuse same logic
@app.route('/upload', methods=['GET', 'POST'])
def upload_alias():
    return upload()

if __name__ == '__main__':
    app.run(debug=True)
