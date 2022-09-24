import re


def sanitize(text: str) -> str:
    # https://qiita.com/YuukiMiyoshi/items/6ce77bf402a29a99f1bf
    # 全角文字はすべて半角に（数字が1桁なら全角にして2桁以上なら半角で表示することへの対応）
    text = text.translate(
        str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)})
    )

    # 改行とタブ文字を除去
    text = text.replace("\n", "").replace("\r", "").replace("\t", "")

    # 丸文字を画像から文字へ変換（監督指針用）
    numbers = [
        "①",
        "②",
        "③",
        "④",
        "⑤",
        "⑥",
        "⑦",
        "⑧",
        "⑨",
        "⑩",
        "⑪",
        "⑫",
        "⑬",
        "⑭",
        "⑮",
        "⑯",
        "⑰",
        "⑱",
        "⑲",
        "⑳",
    ]
    for i in range(20):
        k = i + 1
        text = re.sub(
            '<img[^>]*?src="/images/common/maru' + str(k) + '\\.gif".*?>',
            numbers[i],
            text,
        )
    return text
