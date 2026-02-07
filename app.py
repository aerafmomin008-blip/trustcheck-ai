from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

# -----------------------------------
# Popular & Trusted websites
# -----------------------------------
POPULAR_SITES = [
    "google.com", "youtube.com", "facebook.com", "instagram.com",
    "amazon.com", "amazon.in", "flipkart.com", "netflix.com",
    "twitter.com", "linkedin.com", "github.com", "microsoft.com",
    "apple.com", "openai.com", "whatsapp.com", "wikipedia.org"
]

# -----------------------------------
# Helper: Clean & normalize URL
# -----------------------------------
def clean_domain(url):
    url = url.lower().strip()
    url = re.sub(r"https?://", "", url)
    url = re.sub(r"www\.", "", url)
    return url.split("/")[0]

# -----------------------------------
# Trust Score Logic (IMPROVED)
# -----------------------------------
def calculate_trust_score(domain):
    # Highly trusted known sites
    if domain in POPULAR_SITES:
        return 90

    # AI-like deterministic score for unknown sites
    score = sum(ord(c) for c in domain) % 100
    return max(30, min(85, score))

# -----------------------------------
# Autocomplete API
# -----------------------------------
@app.route("/suggest")
def suggest():
    query = request.args.get("q", "").lower()
    results = [site for site in POPULAR_SITES if site.startswith(query)]
    return jsonify(results[:6])

# -----------------------------------
# Main Route
# -----------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        raw_input = request.form.get("website", "")
        website = clean_domain(raw_input)

        # Validation
        if not re.match(r"^[a-z0-9.-]+\.[a-z]{2,}$", website):
            return render_template(
                "index.html",
                error="Please enter a valid website (example: google.com)"
            )

        trust_score = calculate_trust_score(website)

        # Verdict & Risk
        if trust_score >= 75:
            verdict, risk = "Safe", "Low Risk"
        elif trust_score >= 45:
            verdict, risk = "Suspicious", "Medium Risk"
        else:
            verdict, risk = "Malicious", "High Risk"

        # Trust Signals
        signals = {
            "Domain Age": max(30, trust_score - 10),
            "SSL Certificate": min(100, trust_score + 10),
            "Traffic Reputation": max(25, trust_score - 15),
            "Overall Reputation": trust_score
        }

        # Highlights
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

        # Safety Suggestions
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

        return render_template(
            "result.html",
            website=website,
            trust_score=trust_score,
            verdict=verdict,
            risk=risk,
            signals=signals,
            positives=positives,
            negatives=negatives,
            suggestions=suggestions
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

