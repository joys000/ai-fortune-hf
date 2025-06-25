
import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Hugging Face API 키 환경변수에서 불러오기
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# 사용할 모델 지정 (Hugging Face에서 무료 사용 가능)
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HEADERS = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
    "Content-Type": "application/json"
}

def generate_fortune(user_input):
    payload = {
        "inputs": f"다음은 운세 분석입니다:\n{user_input}\n운세 결과:",
        "options": {"wait_for_model": True}
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()

        # 모델 응답 형식 확인 후 텍스트 추출
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"].split("운세 결과:")[-1].strip()
        else:
            return "운세 응답 형식을 이해하지 못했습니다."
    except Exception as e:
        return f"운세 분석 중 오류 발생: {e}"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        hanja_name = request.form.get("hanja_name")
        birth_date = request.form.get("birth_date")
        birth_time = request.form.get("birth_time")

        user_input = f"이름: {name}, 한자 이름: {hanja_name}, 생년월일: {birth_date}, 태어난 시간: {birth_time}"
        fortune = generate_fortune(user_input)
        return render_template("result.html", fortune=fortune)

    return render_template("index.html")

# 🔧 Render에서 인식할 수 있게 PORT 바인딩 추가
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render는 PORT 환경변수로 포트를 지정함
    app.run(host="0.0.0.0", port=port)
