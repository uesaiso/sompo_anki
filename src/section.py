from bs4 import BeautifulSoup


class Sections:
    def __init__(self, patternSection: list[str], ls: list[str] = None):
        self.pattern: list[str] = patternSection
        self.list: list[str] = ls if ls is not None else [None] * len(patternSection)

    @classmethod
    def update(cls, data: str, previousSections):
        pattern: list[str] = previousSections.pattern
        _list: list[str] = previousSections.list
        soup = BeautifulSoup(data, "html.parser")
        for p in pattern:
            match = soup.select(p)
            if match:
                i = pattern.index(p)
                _list[i] = str(match[-1])

        return cls(pattern, _list)
