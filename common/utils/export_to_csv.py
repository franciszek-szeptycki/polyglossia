import csv
from typing import List

from django.http import HttpResponse


class CSVResponseRenderer:
    @staticmethod
    def render(*, filename: str, rows: List[List[str]]) -> HttpResponse:
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{filename}.csv"'

        writer = csv.writer(response)
        writer.writerows(rows)

        return response
