from django import forms

from vocabulary.infrastructure.models.word import Word


class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ["text", "context"]
        widgets = {
            "text": forms.TextInput(
                attrs={"class": "form-control-custom shadow-sm", "id": "id_text"}
            ),
            "context": forms.TextInput(
                attrs={
                    "class": "form-control-custom translated-field shadow-sm",
                    "id": "id_context",
                }
            ),
        }
