from flask import Flask, request, render_template
import pickle
from news_verifier import verify_news
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

model = pickle.load(open("models/fake_news_model.pkl", "rb"))
vectorizer = pickle.load(open("models/vectorizer.pkl", "rb"))


def predict_news(text):
    text = text.lower().strip()
    text_vec = vectorizer.transform([text])

    prediction = model.predict(text_vec)[0]
    probs = model.predict_proba(text_vec)[0]

    real_prob = probs[0] * 100
    fake_prob = probs[1] * 100

    if prediction == 0:
        label = "REAL NEWS"
    else:
        label = "FAKE NEWS"

    return label, round(real_prob, 2), round(fake_prob, 2)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/predict', methods=['POST'])
def predict():
    news = request.form['news']

    label, real_prob, fake_prob = predict_news(news)
    verified, articles = verify_news(news)

    return render_template(
        "index.html",
        prediction=label,
        real_prob=real_prob,
        fake_prob=fake_prob,
        verified=verified,
        articles=articles
    )


@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():

    news = request.form.get('Body')

    label, real_prob, fake_prob = predict_news(news)
    verified, articles = verify_news(news)

    resp = MessagingResponse()

    message = f"📰 Fake News Result:\n\n"
    message += f"Prediction: {label}\n"
    message += f"Real: {real_prob}%\n"
    message += f"Fake: {fake_prob}%\n"

    if verified:
        message += "\n✅ Verified Sources:\n"
        for article in articles[:3]:
            message += f"- {article['title']}\n"
    else:
        message += "\n⚠️ No trusted sources found"

    resp.message(message)

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)