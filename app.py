from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)

# Hugging Face API 설정
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
headers = {
    "Authorization": f"Bearer {os.getenv('HF_API_TOKEN')}"
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

def generate_fortune(name, birth, time, category, period):
    prompt = (
        f"이름: {name}\n생년월일: {birth}\n출생시간: {time}\n"
        f"운세 분야: {category}\n기간: {period}\n"
        "위 정보를 바탕으로 해당 운세를 자세히 분석해 주세요."
    )
    try:
        output = query({"inputs": prompt})
        result = output[0].get("generated_text", "운세 정보를 불러오지 못했습니다.")
        return result
    except Exception as e:
        return f"운세 분석 중 오류 발생: {e}"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/select_period/<category>")
def select_period(category):
    return render_template("select_period.html", category=category)

@app.route("/form/<category>/<period>", methods=["GET", "POST"])
def form(category, period):
    if request.method == "POST":
        name = request.form['name']
        birth = request.form['birth']
        time = request.form['time']
        fortune = generate_fortune(name, birth, time, category, period)
        return render_template("result.html", name=name, fortune=fortune, category=category, period=period)
    return render_template("form.html", category=category, period=period)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
