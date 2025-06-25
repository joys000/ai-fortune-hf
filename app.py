
from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
    "Content-Type": "application/json"
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        hanja_name = request.form.get("hanja_name")
        birth_date = request.form.get("birth_date")
        birth_time = request.form.get("birth_time")

        prompt = f"""
        이름: {name}
        한자 이름: {hanja_name}
        생년월일: {birth_date}
        태어난 시간: {birth_time}

        위 정보를 바탕으로 오늘의 운세를 사주 풀이처럼 자세하게 알려줘.
        """.strip()

        try:
            response = requests.post(API_URL, headers=headers, json={
                "inputs": prompt,
                "parameters": {"max_new_tokens": 200}
            })
            result = response.json()
            fortune = result[0]["generated_text"] if isinstance(result, list) else str(result)
        except Exception as e:
            fortune = f"운세 분석 중 오류 발생: {e}"

        return render_template("result.html", fortune=fortune)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
