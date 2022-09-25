import re
from src.section import Sections


class Question:
    def __init__(self, data, sections: Sections) -> None:
        self.data = data
        self.sections = sections

    def toText(self, patternClosePre, patternClosePost) -> str:
        text = self.data
        matches = list(re.finditer(patternClosePre + "(.*?)" + patternClosePost, text))
        if not matches:
            return ""
        else:
            answers = [match.group(1) for match in matches]
            answers = sorted(set(answers), key=answers.index)
            text = self.__addSectionsToText(text, self.sections)
            text = (
                self.__replaceAnswer(text, answers, patternClosePre, patternClosePost)
                + "\t"
            )

            return text

    def __addSectionsToText(self, text: str, sections: Sections) -> str:
        for section in reversed(sections.list):
            if section and not section in text:
                text = section + text
        return text

    def __replaceAnswer(
        self, text: str, answers: list, patternClosePre, patternClosePost
    ):
        answers = [answer.replace("(", "\\(").replace(")", "\\)") for answer in answers]
        for answer in answers:
            i = answers.index(answer)
            escapedAnswer = answer.replace("(", "\\(")
            escapedAnswer = escapedAnswer.replace(")", "\\)")
            text = re.sub(
                patternClosePre + answer + patternClosePost,
                "{{c" + str(i + 1) + "::" + escapedAnswer + "}}",
                text,
            )
        return text
