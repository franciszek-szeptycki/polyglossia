from enum import Enum

class Language(Enum):
    GERMAN = "german"
    SPANISH = "spanish"
    ENGLISH = "english"

    @property
    def pretty_name(self):
        labels = {
            Language.GERMAN: "🇩🇪 DEUTSCH",
            Language.SPANISH: "🇪🇸 ESPAÑOL",
            Language.ENGLISH: "🇬🇧 ENGLISH",
        }
        return labels.get(self, self.value.upper())
