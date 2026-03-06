class ReplaceWordInSentence:
    def execute(self, sentence: str, word: str) -> str:
        return sentence.replace(word, "[ ___ ]")
