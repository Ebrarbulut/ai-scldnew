import joblib
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, accuracy_score
from preprocess import preprocess
import numpy as np

def train_models():
    print("=== LOLBAS-Aware Model Eğitim Başladı ===")

    # Veri setini yükle
    X, y = preprocess('dataset.csv')

    # Eğitim ve test seti ayır
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Modeller
    models = {
        "LogisticRegression": LogisticRegression(max_iter=200, n_jobs=-1),
        "RandomForest": RandomForestClassifier(n_estimators=200, n_jobs=-1),
        "SVM": LinearSVC(),
        "GradientBoosting": GradientBoostingClassifier(n_estimators=150),
        "NaiveBayes": MultinomialNB()
    }

    best_model = None
    best_score = 0.0
    scores_summary = {}

    for name, model in models.items():
        print(f"\n--- {name} eğitiliyor ---")
        model.fit(X_train, y_train)

        # Test seti doğruluk
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        scores_summary[name] = acc

        print(f"{name} doğruluk: {acc:.4f}")
        print(classification_report(y_test, y_pred))

        # En iyi modeli seç
        if acc > best_score:
            best_model = model
            best_score = acc

    print("\n=== MODELLERİN DOĞRULUK SONUÇLARI ===")
    for m, score in scores_summary.items():
        print(f"{m}: {score:.4f}")

    print(f"\nEn iyi model: {best_model.__class__.__name__} (Acc: {best_score:.4f})")

    # En iyi modeli kaydet
    joblib.dump(best_model, 'model.pkl')
    print("En iyi model 'model.pkl' olarak kaydedildi.")

if __name__ == "__main__":
    train_models()
