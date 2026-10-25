import streamlit as st
import joblib

st.set_page_config(
    page_title="أمان AI",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ أمان AI")
st.subheader("مساعد توعوي للأمن الرقمي")
st.write("حلّلي الرسالة لمعرفة تصنيف النموذج ومؤشرات الحذر.")

@st.cache_resource
def load_model():
    return joblib.load("aman_ai_model.joblib")

try:
    package = load_model()
    model = package["model"]
    vectorizer = package["vectorizer"]

    message = st.text_area(
        "الصقي نص الرسالة هنا",
        height=150,
        placeholder="اكتبي الرسالة المراد تحليلها..."
    )

    if st.button("تحليل الرسالة"):
        if not message.strip():
            st.warning("اكتبي رسالة أولًا.")
        else:
            vector = vectorizer.transform([message])
            prediction = model.predict(vector)[0]

            st.write("### نتيجة التحليل")

            if prediction == "احتيالية":
                st.error("النموذج صنّف الرسالة على أنها احتيالية.")
            else:
                st.success("النموذج صنّف الرسالة على أنها آمنة.")

            st.info(
                "هذا توقع آلي تقديري، وقد يخطئ. "
                "تحققي من مصدر الرسالة ولا تشاركي رموز التحقق."
            )

except Exception as error:
    st.error(
        "تعذّر تحميل النموذج. تأكدي من وجود ملف "
        "aman_ai_model.joblib بجانب app.py."
    )
