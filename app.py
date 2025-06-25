import requests
from flask import Flask, render_template, request

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
API_KEY = "hf_당신의_키"  # Hugging Face API 키

headers = {"Authorization": f"Bearer {API_KEY}"}

def generate_fortune(user_input):
    payload = {
        "inputs": f"다음 사람의 운세를 예측해 주세요:\n{user_input}",
        "options": {"wait_for_model": True}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return f"운세 분석 중 오류 발생: {response.status_code} - {response.text}"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        hanja_name = request.form.get("hanja_name")
        birth_date = request.form.get("birth_date")
        birth_time = request.form.get("birth_time")

        user_input = f"이름: {name} ({hanja_name})\n생년월일: {birth_date}\n출생시간: {birth_time}"

        fortune = generate_fortune(user_input)
        return render_template("result.html", fortune=fortune)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
