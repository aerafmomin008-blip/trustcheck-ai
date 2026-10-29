from flask import Flask, render_template, request, jsonify
import re
import os
import google.generativeai as genai

app = Flask(__name__)

# -----------------------------------
# Gemini Configuration
# -----------------------------------
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model_llm = genai.GenerativeModel("gemini-1.5-flash")

# -----------------------------------
# Popular & Trusted websites
# -----------------------------------
POPULAR_SITES = [
    "google.com", "gmail.com", "github.com",
    "youtube.com", "yahoo.com",
    "facebook.com", "flipkart.com",
    "instagram.com", "amazon.com", "amazon.in",
    "netflix.com", "linkedin.com",
    "microsoft.com", "apple.com",
    "openai.com", "wikipedia.org",
    "whatsapp.com", "twitter.com"
]

# -----------------------------------
# Scam-style domain patterns (DEMO)
# -----------------------------------
SCAM_PATTERNS = [
    "{brand}-login-secure.site",
    "{brand}-verify-account.xyz",
    "{brand}-support-help.top",
    "{brand}-reward-claim.online",
    "{brand}-free-offer.site"
]

# -----------------------------------
# Clean domain
# -----------------------------------
def clean_domain(url):
    url = url.lower().strip()
    url = re.sub(r"https?://", "", url)
    url = re.sub(r"www\.", "", url)
    return url.split("/")[0]

# -----------------------------------
# Trust Score Logic
# -----------------------------------
def calculate_trust_score(domain):
    if domain in POPULAR_SITES:
        return 90

    score = sum(ord(c) for c in domain) % 100
    return max(30, min(85, score))

# -----------------------------------
# 🤖 Gemini AI Suggestions
# -----------------------------------
def get_ai_analysis(domain, verdict, risk):
    try:
        prompt = f"""
        Analyze the website: {domain}
        Trust verdict: {verdict}
        Risk level: {risk}

        Provide:
        - Simple explanation of what this means
        - 3 safety tips
        - 2 warning signs to check
        Keep response beginner friendly.
        """

        response = model_llm.generate_content(prompt)
        return response.text

    except Exception as e:
        return "AI analysis temporarily unavailable."

# -----------------------------------
# 🔥 SMART AUTOCOMPLETE API
# -----------------------------------
@app.route("/suggest")
def suggest():
    query = request.args.get("q", "").lower().strip()

    if not query:
        return jsonify([])

    suggestions = set()

    for site in POPULAR_SITES:
        if site.startswith(query):
            suggestions.add(site)

    brand = query.split(".")[0]
    if len(brand) >= 1:
        for pattern in SCAM_PATTERNS:
            suggestions.add(pattern.format(brand=brand))

    return jsonify(list(suggestions)[:8])

# -----------------------------------
# Main Route
# -----------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        raw_input = request.form.get("website", "")
        website = clean_domain(raw_input)

        if not re.match(r"^[a-z0-9.-]+\.[a-z]{2,}$", website):
            return render_template(
                "index.html",
                error="Please enter a valid website (example: google.com)"
            )

        trust_score = calculate_trust_score(website)

        if trust_score >= 75:
            verdict, risk = "Safe", "Low Risk"
        elif trust_score >= 45:
            verdict, risk = "Suspicious", "Medium Risk"
        else:
            verdict, risk = "Malicious", "High Risk"

        signals = {
            "Domain Age": max(30, trust_score - 10),
            "SSL Certificate": min(100, trust_score + 10),
            "Traffic Reputation": max(25, trust_score - 15),
            "Overall Reputation": trust_score
        }

        positives, negatives = [], []

        if trust_score >= 75:
            positives += [
                "Well-established and trusted domain",
                "Low likelihood of phishing activity",
                "Strong security and reputation signals"
            ]
        elif trust_score >= 45:
            positives.append("Some legitimate trust indicators detected")
            negatives.append("Reputation indicators are inconsistent")
        else:
            negatives += [
                "Low trust score",
                "High probability of scam or phishing",
                "Weak or unknown domain reputation"
            ]

        suggestions = []

        if trust_score < 75:
            suggestions.append("Avoid sharing sensitive personal information.")
        if trust_score < 50:
            suggestions.append("Do not proceed with payments or downloads.")

        if not suggestions:
            suggestions += [
                "No major risks detected.",
                "Safe to browse with normal precautions."
            ]

        # 🤖 Get AI analysis
        ai_analysis = get_ai_analysis(website, verdict, risk)

        return render_template(
            "result.html",
            website=website,
            trust_score=trust_score,
            verdict=verdict,
            risk=risk,
            signals=signals,
            positives=positives,
            negatives=negatives,
            suggestions=suggestions,
            ai_analysis=ai_analysis
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
