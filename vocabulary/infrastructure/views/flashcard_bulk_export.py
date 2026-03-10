from datetime import datetime

from django.views import View

from common.utils.export_to_csv import CSVResponseRenderer
from vocabulary.infrastructure.factories.container import container


class FlashcardBulkExportView(View):
    def post(self, request):
        card_ids = request.POST.getlist("card_ids")

        now = datetime.now()

        lines = container.use_case_get_flashcard_data_to_export.execute(
            card_ids=card_ids, time=now
        )

        filename = f"polyglossia_anki_export_{now.strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        return CSVResponseRenderer.render(filename=filename, rows=lines)
