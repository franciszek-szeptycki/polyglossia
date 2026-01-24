from django import forms

from sentences.application.dtos.sentece import SentenceDTO


class SentenceForm(forms.Form):
    text = forms.CharField(
        label="Zdanie", max_length=500, widget=forms.Textarea(attrs={"rows": 3})
    )

    def to_dto(self) -> SentenceDTO:
        return SentenceDTO(
            text=self.cleaned_data["text"],
        )
