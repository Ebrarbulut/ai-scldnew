import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import re

def clean_command(command):
    
  
    command = re.sub(r'[^\w\s\-\./:]', ' ', command)
    
    command = re.sub(r'\s+', ' ', command.lower().strip())
    return command

def preprocess(csv_path, max_features=2000):
    
    df = pd.read_csv(csv_path)
    
   
    df['command'] = df['command'].apply(clean_command)
    
  
    df = df.dropna()
    df = df[df['command'].str.len() > 2]
    
    print(f"Temizlenen veri boyutu: {len(df)}")
    
    
    tfidf = TfidfVectorizer(
        stop_words='english',
        max_features=max_features,
        ngram_range=(1, 2),  
        min_df=2,  
        max_df=0.95  
    )
    
    X = tfidf.fit_transform(df['command'])
    y = df['label']
    
    joblib.dump(tfidf, 'vectorizer.pkl')
    
    return X, y

if __name__ == '__main__':
    X, y = preprocess('dataset.csv')
    print(f"Veri şekli: {X.shape}, Etiket dağılımı: {pd.Series(y).value_counts().to_dict()}")

