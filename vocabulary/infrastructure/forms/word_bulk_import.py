from django import forms


class BulkImportForm(forms.Form):
    data = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 10}),
        required=True,
    )

    def get_parsed_data(self):
        data_str = self.cleaned_data.get("data", "")
        lines = data_str.splitlines()
        parsed = []
        for line in lines:
            line = line.strip()
            if ";" in line:
                parts = line.split(";", 1)
                parsed.append({"text": parts[0].strip(), "context": parts[1].strip()})
        return parsed
