from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Hugging Face Inference API
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
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

        # 출력 구조 확인 및 텍스트 추출
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]
        elif isinstance(result, dict) and "error" in result:
            return f"⚠️ 모델 오류: {result['error']}"
        else:
            return "⚠️ 예상치 못한 응답 형식입니다."

    except Exception as e:
        return f"운세 분석 중 오류 발생: {e}"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        hanja_name = request.form["hanja_name"]
        birth_date = request.form["birth_date"]
        birth_time = request.form["birth_time"]

        # 프롬프트 구성
        prompt = (
            f"이름: {name} ({hanja_name})\n"
            f"생년월일: {birth_date}\n"
            f"태어난 시간: {birth_time}\n\n"
            f"이 정보를 바탕으로 오늘의 운세를 자세히 분석해줘."
        )

        fortune = query_fortune(prompt)
        return render_template("result.html", fortune=fortune)

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
