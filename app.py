from flask import Flask, render_template, request
import random

app = Flask(__name__)

# 템플릿 기반 운세 문장들
intro_list = [
    "오늘은 마음이 평온하고 안정된 하루가 예상됩니다.",
    "예상치 못한 기쁨이 찾아올 수 있는 하루입니다.",
    "자신의 직감을 믿고 행동하기에 좋은 날입니다.",
    "작은 선택이 큰 결과로 이어질 수 있는 날이에요."
]

tip_list = [
    "긍정적인 마인드가 행운을 부를 것입니다.",
    "지나친 걱정보다는 현재에 집중해보세요.",
    "사람들과의 대화에서 힌트를 얻을 수 있어요.",
    "자기 자신을 믿는다면 원하는 방향으로 흘러갈 거예요."
]

warning_list = [
    "다만, 충동적인 행동은 삼가는 것이 좋습니다.",
    "감정에 휘둘리지 않도록 주의하세요.",
    "작은 실수가 큰 영향을 미칠 수 있습니다.",
    "건강 관리를 소홀히 하지 마세요."
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        hanja_name = request.form["hanja_name"]
        birth_date = request.form["birth_date"]
        birth_time = request.form["birth_time"]

        # 랜덤 운세 생성
        fortune = f"""
        {birth_date} {birth_time}에 태어난 {name}({hanja_name})님의 오늘의 운세는 다음과 같습니다:<br><br>
        {random.choice(intro_list)}<br>
        {random.choice(tip_list)}<br>
        {random.choice(warning_list)}<br><br>
        좋은 하루 보내세요! 🌟
        """
        return render_template("result.html", fortune=fortune)

    return render_template("index.html")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
