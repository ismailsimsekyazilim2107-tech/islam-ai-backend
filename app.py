from flask import Flask, request, render_template_string
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

SYSTEM_PROMPT = """
Sen İslamiyet konusunda uzman, güvenilir ve saygılı bir yapay zekasın.
Kur'an ve sahih hadisler doğrultusunda cevap ver.
Kesin olmayan konularda 'Allah en doğrusunu bilir' de.
"""

HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<title>İslam Yapay Zeka</title>
<style>
body{font-family:Arial;background:#f4f6f8;padding:40px}
.box{max-width:700px;margin:auto;background:white;padding:25px;border-radius:8px}
textarea{width:100%;height:100px}
button{padding:10px 20px;margin-top:10px}
.answer{background:#eef;padding:15px;margin-top:20px}
</style>
</head>
<body>
<div class="box">
<h2>🕌 İslam Yapay Zeka</h2>
<form method="POST">
<textarea name="prompt" required></textarea><br>
<button type="submit">Sor</button>
</form>
{% if result %}
<div class="answer"><b>Cevap:</b><br>{{ result }}</div>
{% endif %}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        prompt = request.form.get("prompt")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )
        result = response.choices[0].message.content

    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run()
