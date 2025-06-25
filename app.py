from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Hugging Face Inference API 설정
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
headers = {
    "Authorization": f"Bearer {os.getenv('HF_API_KEY')}"
}

# 운세 분석 함수
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

        if isinstance(result, dict) and "error" in result:
            return f"⚠️ 모델 오류: {result['error']}"

        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]

        return result[0].get("generated_text", "⚠️ 결과 형식이 예상과 다릅니다.")
    except Exception as e:
        return f"운세 분석 중 오류 발생: {e}"

# 웹 라우팅
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        hanja_name = request.form["hanja_name"]
        birth_date = request.form["birth_date"]
        birth_time = request.form["birth_time"]

        # AI에게 전달할 프롬프트
        prompt = (
            f"다음 정보로 오늘의 운세를 한국어로 예측해줘.\n\n"
            f"이름: {name} ({hanja_name})\n"
            f"생년월일: {birth_date}\n"
            f"태어난 시간: {birth_time}\n"
            f"결과는 진지하고 구체적인 어조로 써줘."
        )

        fortune = query_fortune(prompt)
        return render_template("result.html", fortune=fortune)

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
