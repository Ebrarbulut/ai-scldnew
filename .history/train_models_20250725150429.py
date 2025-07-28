import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split, cross_val_score
from preprocess import preprocess
import numpy as np

def train_and_evaluate():
    """Gelişmiş model eğitimi ve karşılaştırması"""
    X, y = preprocess('dataset.csv')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
   
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "Linear SVC": LinearSVC(random_state=42, dual=False),
        "Gradient Boosting": GradientBoostingClassifier(random_state=42),
        "Multinomial NB": MultinomialNB()
    }
    
    results = {}
    best_model = None
    best_score = 0
    
    print("=" * 80)
    print("MODEL PERFORMANS KARŞILAŞTIRMASI")
    print("=" * 80)
    
    for name, model in models.items():
        print(f"\n--- {name} ---")
        
        
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        
        acc = accuracy_score(y_test, y_pred)
        
        
        cv_scores = cross_val_score(model, X_train, y_train, cv=5)
        
        
        try:
            y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else model.decision_function(X_test)
            auc_score = roc_auc_score(y_test, y_prob)
        except:
            auc_score = 0
        
       
        results[name] = {
            'accuracy': acc,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'auc_score': auc_score
        }
        
        print(f"Accuracy: {acc:.4f}")
        print(f"Cross-Validation: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        print(f"AUC-ROC: {auc_score:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        
        if acc > best_score:
            best_score = acc
            best_model = model
    
    
    print("\n" + "=" * 80)
    print("ÖZET PERFORMANS TABLOSU")
    print("=" * 80)
    df_results = pd.DataFrame(results).T
    df_results = df_results.round(4)
    print(df_results.to_string())
    
   
    print(f"\n🏆 En iyi model: {best_model.__class__.__name__} (Accuracy: {best_score:.4f})")
    joblib.dump(best_model, 'model.pkl')
    
    
    y_pred_best = best_model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred_best)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f'Confusion Matrix - {best_model.__class__.__name__}')
    plt.ylabel('Gerçek')
    plt.xlabel('Tahmin')
    plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return results, best_model

if __name__ == '__main__':
    results, best_model = train_and_evaluate()