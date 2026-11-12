"""Read a CSV email list without changing employee or user records."""
import csv
import io
from pathlib import Path

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

SESSION_KEY = 'employee_email_csv_filter'
MAX_BYTES = 1024 * 1024
MAX_ROWS = 5000


class EmailCSVForm(forms.Form):
    email_csv = forms.FileField()

    def clean_email_csv(self):
        upload = self.cleaned_data['email_csv']
        if Path(upload.name).suffix.lower() != '.csv':
            raise ValidationError('Choose a CSV file.')
        if upload.size > MAX_BYTES:
            raise ValidationError('The CSV must be 1 MB or smaller.')
        try:
            content = upload.read(MAX_BYTES + 1).decode('utf-8-sig')
        except UnicodeDecodeError:
            raise ValidationError('Save the CSV as UTF-8 and try again.')
        if '\x00' in content:
            raise ValidationError('The file is not a valid text CSV.')
        if len(content.encode('utf-8')) > MAX_BYTES:
            raise ValidationError('The CSV must be 1 MB or smaller.')
        try:
            sample = content[:8192]
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=',;\t')
            except csv.Error:
                dialect = csv.excel
            rows = csv.reader(io.StringIO(content, newline=''), dialect, strict=True)
            emails, seen = [], set()
            invalid = duplicates = 0
            column = None
            first = True
            data_rows = 0
            for row_number, row in enumerate(rows, 1):
                if row_number > MAX_ROWS + 1:
                    raise ValidationError('Use no more than 5,000 email rows per CSV.')
                if not row or not any(cell.strip() for cell in row):
                    continue
                if first:
                    first = False
                    headers = [cell.strip().lower().replace('_', ' ') for cell in row]
                    header_columns = [i for i, cell in enumerate(headers)
                                      if cell in ('email', 'email address', 'emailaddress', 'e-mail')]
                    if header_columns:
                        column = header_columns[0]
                        continue
                    if len(row) != 1:
                        raise ValidationError('For multiple columns, include an email column header.')
                    column = 0
                data_rows += 1
                if data_rows > MAX_ROWS:
                    raise ValidationError('Use no more than 5,000 email rows per CSV.')
                if column >= len(row):
                    invalid += 1
                    continue
                email = row[column].strip().lower()
                if not email:
                    invalid += 1
                    continue
                try:
                    validate_email(email)
                except ValidationError:
                    invalid += 1
                    continue
                if email in seen:
                    duplicates += 1
                    continue
                seen.add(email)
                emails.append(email)
            if not emails:
                raise ValidationError('No valid email addresses were found in the CSV.')
        except csv.Error:
            raise ValidationError('The CSV could not be read. Check its formatting.')
        return {'emails': emails, 'filename': Path(upload.name).name,
                'invalid_count': invalid, 'duplicate_count': duplicates}
