from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/bigscience/bloomz-560m"
headers = {
    "Authorization": f"Bearer {os.getenv('HF_API_KEY')}"
}

def query_fortune(prompt):
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": prompt},
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        return result[0].get("generated_text", "⚠️ 운세 분석 결과 없음")
    except Exception as e:
        return f"운세 분석 중 오류 발생: {e}"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        hanja_name = request.form["hanja_name"]
        birth_date = request.form["birth_date"]
        birth_time = request.form["birth_time"]

        prompt = (
            f"다음 정보로 오늘의 운세를 진지하고 구체적으로 알려줘.\n"
            f"이름: {name} ({hanja_name})\n"
            f"생년월일: {birth_date}\n"
            f"태어난 시간: {birth_time}\n"
            f"한국어로 작성해줘."
        )

        fortune = query_fortune(prompt)
        return render_template("result.html", fortune=fortune)

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
