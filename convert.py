import os
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

    patternClosePre = "{{"
    patternClosePost = "}}"
    for question in questionList:
        outputData = (
            outputData + question.toText(patternClosePre, patternClosePost) + "\n"
        )

    print(outputData)
    outputFile = open(output, "w", encoding="utf-8")
    outputFile.write(outputData)
    outputFile.close()


def to_output(input: str) -> str:
    input_path = os.path.dirname(input)
    output_path = input_path.replace("input", "output")
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    return os.path.splitext(input)[0].replace("input", "output") + ".txt"


if __name__ == "__main__":
    patternSections = ["<h1>.*?</h1>", "<h2>.*?</h2>", "<h3>.*?</h3>", "<h4>.*?</h4>"]
    args = sys.argv
    input = args[1]
    if os.path.isdir(input):
        for root, dirs, files in os.walk(top=input):
            for file in files:
                if not file.lower().endswith((".html")):
                    continue
                filePath = os.path.join(root, file)
                print(f"input file = {filePath}")
                output = to_output(filePath)
                convert(filePath, output, patternSections)
    if os.path.isfile(input):
        output = to_output(input)
        convert(input, output, patternSections)
