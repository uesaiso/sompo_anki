import sys
from src.sanitize import sanitize
from src.section import Sections
from src.question import Question


def convert(input: str, output: str, patternSection: list) -> None:

    inputFile = open(input, "r", encoding="utf-8")
    inputData = inputFile.read()
    inputFile.close()
    inputData = sanitize(inputData)

    # 問題の区切りは<hr>で行う
    ls = inputData.split("<hr>")

    latestSections = Sections(patternSection)
    questionList: list[Question] = []

    for item in ls:
        latestSections = Sections.update(item, latestSections)
        questionList.append(Question(item, latestSections))

    outputData = ""

    patternClosePre = '{{'
    patternClosePost = "}}"
    for question in questionList:
        outputData = (
            outputData + question.toText(patternClosePre, patternClosePost) + "\n"
        )

    print(outputData)
    outputFile = open(output, "w", encoding="utf-8")
    outputFile.write(outputData)
    outputFile.close()


if __name__ == "__main__":
    # セクション文字列を適切に切り出し、問題文の手前に置くための正規表現パターン
    # petternRoman = "(IX|IV|V?I{0,3})"
    # これは監督指針用
    # patternSections = ["<h1>\\s*?"+petternRoman+"\\s*?\\..*?</h1>",
    #                   "<h2>\\s*?"+petternRoman+"\\s*?-\\d*?[^-]*?</h2>",
    #                   "<h3>\\s*?"+petternRoman+"\\s*?-\\d*?-\\d*?[^-]*?</h3>",
    #                   "<h4>\\s*?"+petternRoman+"\\s*?-\\d*?-\\d*?-\\d*?[^-]*?</h4>",
    #                   "<h4>\\s*?"+petternRoman+"\\s*?-\\d*?-\\d*?-\\d*?-\\d*?[^-]*?</h4>"]
    patternSections = ["<h1>.*?</h1>", "<h2>.*?</h2>", "<h3>.*?</h3>", "<h4>.*?</h4>"]
    args = sys.argv
    convert(args[1], args[2], patternSections)
