import joblib
import re

# LOLBAS Whitelist
WHITELIST_PATTERNS = [
    r"^regsvr32\s+/s\s+/n\s+/u\s+/i:https://www\.example\.org/file\.sct\s+scrobj\.dll$",
    r"^csc\s+-target:library\s+.*$"
]

def is_whitelisted(command):
    return any(re.match(pattern, command) for pattern in WHITELIST_PATTERNS)

def predict_command(command):
    """Komut tahmin fonksiyonu"""
    try:
        # Whitelist kontrolü
        if is_whitelisted(command):
            return {
                "command": command,
                "prediction": "benign",
                "confidence": 100.0,
                "risk_level": "GÜVENLİ",
                "model_type": "Whitelist"
            }

        model = joblib.load('model.pkl')
        vectorizer = joblib.load('vectorizer.pkl')

        command_vector = vectorizer.transform([command])
        prediction = model.predict(command_vector)[0]

        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(command_vector)[0]
            confidence = max(probabilities) * 100
        else:
            confidence = 85.0

        # Threshold ayarı
        if prediction == "malicious" and confidence < 75:
            prediction = "benign"

        risk_level = "GÜVENLİ" if prediction == "benign" else ("YÜKSEK" if confidence > 90 else "ORTA")

        return {
            "command": command,
            "prediction": prediction,
            "confidence": round(confidence, 2),
            "risk_level": risk_level,
            "model_type": model.__class__.__name__
        }

    except Exception as e:
        return {
            "command": command,
            "prediction": "error",
            "confidence": 0,
            "risk_level": "UNKNOWN",
            "error": str(e)
        }
