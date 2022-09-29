import re

from bs4 import BeautifulSoup
from src.section import Sections


class Question:
    def __init__(self, data: str, sections: Sections, preClose: str, postClose: str, commentSelector: str) -> None:
        self.data = data
        self.sections = sections
        self.preClose = preClose
        self.postClose = postClose
        self.commentSelector = commentSelector

    def toText(self) -> str:
        soup = BeautifulSoup(self.data, "html.parser")
        comment = ""
        for e in soup.select(self.commentSelector):
            comment += str(e.extract())
        text = str(soup)

        answers = self.__findAnswers(text)
        if not answers:
            return ""
        else:
            text = self.__addSectionsToText(text)
            text = self.__addNumberToAnswers(text, answers)
            return text + "\t" + comment + "\t"

    def __findAnswers(self, text: str) -> list[str]:
        matches = list(re.finditer(self.preClose + "(.*?)" + self.postClose, text))
        answers = [match.group(1) for match in matches]
        answers = sorted(set(answers), key=answers.index)
        return answers


    def __addSectionsToText(self, text: str) -> str:
        for section in reversed(self.sections.list):
            if section and not section in text:
                text = section + text
        return text

    def __addNumberToAnswers(
        self, text: str, answers: list
    ):
        answers = [answer for answer in answers]
        for answer in answers:
            i = answers.index(answer)
            text = re.sub(
                self.preClose + answer + self.postClose,
                "{{c" + str(i + 1) + "::" + answer + "}}",
                text,
            )
        return text
