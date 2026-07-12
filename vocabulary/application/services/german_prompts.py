from typing import List


class GermanPrompts:
    @staticmethod
    def sentences(*, word: str) -> str:
        return (
            f"""
        Generate 7 sentences in German using the word "{word}".
        Each sentence should be simple and easy to understand for a beginner learner of German.
        Each sentence should be no longer than 7 words and should include the word "{word}" in a natural way.
        Each sentence should be common used in everyday conversation.
        Word "{word}" can take different forms depending on the person, number, and inflection.
        """
            + """
        return the sentences as a list of strings in format:
        {
            "sentences": [
                "sentence 1",
                "sentence 2",
                "sentence 3"
            ]
        }"""
        )

    @staticmethod
    def word_forms(*, sentences: List[str], word: str) -> str:
        return (
            f"""
        Given the following sentences in German:
        {sentences}
        Each sentence contains a word "{word}" in German.
        Identify that word in each sentence and return a list of the forms of the word "{
                word
            }" used in each sentence.
        For example, if the word is "sprechen" and the sentences are:
        "Ich spreche Deutsch."
        "Du sprichst Englisch."
        "Er spricht Franzosisch."
        The output should be: """
            + """
        {
            "forms": [
                "spreche",
                "sprichst",
                "spricht"
            ]
        }
        """
        )

    @staticmethod
    def translate(*, data: List[tuple[str, str]]) -> str:
        return (
            f"""
        Given the following sentences in German and the word used in each sentence:
        {data}
        Translate each sentence into Polish, and also word assigned to that sentence.
        Return the translations as a list of objects in format:"""
            + """
        {
            "translations": [
                {
                    "sentence": "translation 1",
                    "word": "translation of the word in sentence 1"
                },
                {
                    "sentence": "translation 2",
                    "word": "translation of the word in sentence 2"
                }
            ]
        }
        example for:
            ['Ich spreche jeden Tag Deutsch.', 'spreche']
            ['Sprichst du Englisch?', 'sprichst']
        should return:
            {
                "translations": [
                    {
                        "sentence": "Mówię po niemiecku codziennie.",
                        "word": "spreche"
                    },
                    {
                        "sentence": "Czy mówisz po angielsku?",
                        "word": "sprichst"
                    }
                ]
            }
        """
        )
