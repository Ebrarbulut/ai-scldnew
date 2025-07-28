import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, confusion_matrix
from preprocess import preprocess
import seaborn as sns

def train_best_model(csv_path='dataset.csv'):
    print("🔍 Veri ön işleniyor...")
    X, y = preprocess(csv_path)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {
        "LogisticRegression": LogisticRegression(max_iter=500, class_weight='balanced'),
        "RandomForest": RandomForestClassifier(class_weight='balanced'),
        "GradientBoosting": GradientBoostingClassifier(),
        "NaiveBayes": MultinomialNB(),
        "LinearSVC": LinearSVC(class_weight='balanced')
    }

    best_model = None
    best_score = 0
    print("📊 Modeller eğitiliyor ve doğrulukları test ediliyor...")

    for name, model in models.items():
        if name == "LinearSVC":
            scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
            mean_score = scores.mean()
        else:
            scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
            mean_score = scores.mean()
        print(f" - {name}: Ortalama CV doğruluk: {mean_score:.4f}")

        if mean_score > best_score:
            best_score = mean_score
            best_model = (name, model)

    print(f"\n✅ En iyi model: {best_model[0]} (CV doğruluk: {best_score:.4f})")

    # En iyi modeli tüm eğitim verisinde eğit
    final_model = best_model[1]
    final_model.fit(X_train, y_train)

    y_pred = final_model.predict(X_test)

    print("\n--- Test Sonuçları ---")
    print(classification_report(y_test, y_pred))

    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=['Benign', 'Malicious'], yticklabels=['Benign', 'Malicious'])
    plt.title(f"Confusion Matrix - {best_model[0]}")
    plt.xlabel("Tahmin")
    plt.ylabel("Gerçek")
    plt.show()

    joblib.dump(final_model, 'model.pkl')
    print(f"💾 Model kaydedildi: model.pkl")

    return final_model

if __name__ == '__main__':
    train_best_model()
