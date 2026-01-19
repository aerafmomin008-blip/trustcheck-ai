from flask import Flask, render_template, request
from urllib.parse import urlparse
import csv

app = Flask(__name__)

SUSPICIOUS_KEYWORDS = [
    "free", "bonus", "win", "prize",
    "crypto", "giveaway", "login",
    "secure", "verify"
]

def load_database():
    db = {}
    with open("data/websites.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            db[row["domain"]] = row
    return db

DATABASE = load_database()

def calculate_dynamic_score(url):
    parsed = urlparse(url if "://" in url else "http://" + url)
    domain = parsed.netloc.lower()

    security = 100 if url.startswith("https://") else 60
    reputation = 50
    risk = 100

    for word in SUSPICIOUS_KEYWORDS:
        if word in url.lower():
            risk -= 15

    final_score = int((security + reputation + risk) / 3)

    if final_score >= 80:
        status = "Legitimate"
        color = "green"
    elif final_score >= 50:
        status = "Suspicious"
        color = "orange"
    else:
        status = "High Risk"
        color = "red"

    return {
        "domain": domain,
        "score": final_score,
        "status": status,
        "color": color,
        "security": security,
        "reputation": reputation,
        "risk": risk,
        "source": "Real-time analysis"
    }

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        parsed = urlparse(url if "://" in url else "http://" + url)
        domain = parsed.netloc.lower()

        if domain in DATABASE:
            data = DATABASE[domain]
            result = {
                "domain": domain,
                "score": int(data["trust_score"]),
                "status": data["category"].capitalize(),
                "color": "green" if int(data["trust_score"]) > 80 else "orange" if int(data["trust_score"]) > 50 else "red",
                "security": int(data["trust_score"]),
                "reputation": int(data["trust_score"]),
                "risk": int(data["trust_score"]),
                "source": "Known website database"
            }
        else:
            result = calculate_dynamic_score(url)

        return render_template("result.html", result=result, url=url)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
