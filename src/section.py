import re
from typing import Literal


class Sections:
    def __init__(self, patternSection: list, ls: list = None):
        self.pattern: list[Literal] = patternSection
        self.list: list[str] = ls if ls is not None else [None] * len(patternSection)

    @classmethod
    def update(cls, data: str, previousSections):
        pattern = previousSections.pattern
        ls = previousSections.list
        for p in pattern:
            match = re.findall(p, data)
            if match:
                i = pattern.index(p)
                ls[i] = match[-1]

        return cls(pattern, ls)
