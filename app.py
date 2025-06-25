from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# [1] 간단한 한자 추천 매핑
hanja_map = {
    "재우": ["在雨", "宰祐", "才祐", "載雨"],
    "민주": ["敏珠", "玟柱", "旼周"],
    "지민": ["智珉", "志旼", "知敏"],
    "희진": ["喜珍", "希眞", "熙珍"],
    "유진": ["柔珍", "有珍", "裕珍"]
}

# [2] 별자리 매핑 (생일 기준)
zodiac_signs = [
    ("염소자리", (1, 1), (1, 19)),
    ("물병자리", (1, 20), (2, 18)),
    ("물고기자리", (2, 19), (3, 20)),
    ("양자리", (3, 21), (4, 19)),
    ("황소자리", (4, 20), (5, 20)),
    ("쌍둥이자리", (5, 21), (6, 21)),
    ("게자리", (6, 22), (7, 22)),
    ("사자자리", (7, 23), (8, 22)),
    ("처녀자리", (8, 23), (9, 23)),
    ("천칭자리", (9, 24), (10, 22)),
    ("전갈자리", (10, 23), (11, 22)),
    ("사수자리", (11, 23), (12, 24)),
    ("염소자리", (12, 25), (12, 31)),
]

# [3] 별자리별 운세 메시지 예시 (30개 중 일부)
zodiac_fortunes = {
    "물병자리": [
        "오늘은 새로운 만남이 기다리고 있습니다.",
        "계획보다 감정이 먼저일 수 있어요.",
        "작은 선택이 큰 변화를 불러올 수 있어요."
    ],
    "염소자리": [
        "자기 자신을 믿는 하루가 되세요.",
        "기대하지 않았던 도움을 받을 수 있어요.",
        "노력의 결실이 서서히 나타날 거예요."
    ],
    # ... (다른 별자리도 30개씩 확장 가능)
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search_hanja")
def search_hanja():
    name = request.args.get("name", "")
    options = hanja_map.get(name, [])
    return jsonify({"options": options})

@app.route("/result", methods=["POST"])
def result():
    name = request.form.get("name", "")
    hanja_name = request.form.get("hanja_name", "")
    year = int(request.form.get("year", "2000"))
    month = int(request.form.get("month", "1"))
    day = int(request.form.get("day", "1"))

    # 별자리 계산
    sign = "알 수 없음"
    for zodiac, start, end in zodiac_signs:
        if (month == start[0] and day >= start[1]) or (month == end[0] and day <= end[1]):
            sign = zodiac
            break

    # 운세 선택
    fortune = random.choice(zodiac_fortunes.get(sign, ["오늘은 평범한 하루입니다."]))

    return render_template("result.html", name=name, hanja=hanja_name, sign=sign, fortune=fortune)
