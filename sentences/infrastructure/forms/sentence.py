from django import forms

from sentences.application.dtos.sentence import SentenceDTO


class SentenceForm(forms.Form):
    original_text = forms.CharField(
        label="Zdanie", max_length=500, widget=forms.Textarea(attrs={"rows": 3})
    )

    translated_text = forms.CharField(
        label="Tłumaczenie", max_length=500, widget=forms.Textarea(attrs={"rows": 3})
    )

    def to_dto(self) -> SentenceDTO:
        return SentenceDTO(
            original_text=self.cleaned_data["original_text"],
            translated_text=self.cleaned_data["translated_text"],
        )
