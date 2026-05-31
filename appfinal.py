import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
# ---------- USER LOGIN STATE ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "user_history" not in st.session_state:
    st.session_state.user_history = {}



# -------- CHATBOT SESSION STATE --------
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

if "chat_step" not in st.session_state:
    st.session_state.chat_step = 0




# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Diabetes Prediction App",
    page_icon="🩺",
    layout="wide"
)
# ---------- LOGIN PAGE ----------
if not st.session_state.logged_in:
    st.title("🔐 Login")

    username = st.text_input("Enter your name")

    if st.button("Login"):
        if username != "":
            st.session_state.logged_in = True
            st.session_state.username = username

            if username not in st.session_state.user_history:
                st.session_state.user_history[username] = []

            st.success("Login successful")
            st.rerun()
        else:
            st.error("Please enter a name")

    st.stop()

# ---------------- PREDICTION HISTORY STORAGE ----------------
if "history" not in st.session_state:
    st.session_state.history = []


# ---------------- PWA SUPPORT ----------------
st.markdown(
    """
    <link rel="manifest" href="/manifest.json">
    <script>
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/service-worker.js');
        }
    </script>
    """,
    unsafe_allow_html=True
)
# ---------------- PWA CONFIG ----------------
st.markdown("""
<link rel="manifest" href="/manifest.json">
<script>
if ('serviceWorker' in navigator) {
  window.addEventListener('load', function() {
    navigator.serviceWorker.register('/service-worker.js')
      .then(reg => console.log('Service Worker registered'))
      .catch(err => console.log('Service Worker failed', err));
  });
}
</script>
""", unsafe_allow_html=True)

# ---------------- LOGIN SECTION ----------------
if not st.session_state.logged_in:
    username = st.sidebar.text_input("Enter Username")
    if st.sidebar.button("Login"):
        if username.strip() != "":
            st.session_state.logged_in = True
            st.session_state.username = username
            if username not in st.session_state.user_history:
                st.session_state.user_history[username] = []
            st.sidebar.success(f"Logged in as {username}")
            st.rerun()
        else:
            st.sidebar.error("Please enter a username")
else:
    st.sidebar.success(f"👤 {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
if not st.session_state.logged_in:
    st.info("🔐 Please login from the sidebar to use the application.")
    st.stop()


# ---------------- SIDEBAR SETTINGS ----------------
st.sidebar.header("⚙️ Settings")
dark_mode = st.sidebar.toggle("🌙 Dark Mode")

if st.sidebar.button("🔄 Reset Inputs"):
    st.rerun()   # ✅ updated here
st.sidebar.title("⚙️ Bot Assistant")


# ---------------- SIDEBAR CHATBOT ----------------
with st.sidebar.expander("🤖 Bot Assistant", expanded=False):

    # Show chat history
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    def bot_say(text):
        st.session_state.chat_messages.append(
            {"role": "assistant", "content": text}
        )

    def user_say(text):
        st.session_state.chat_messages.append(
            {"role": "user", "content": text}
        )

    # ---- STEP 0: GREETING ----
    if st.session_state.chat_step == 0:
        bot_say(
            "👋 Hi! I’m your Health Bot Assistant.\n\n"
            "How can I help you today?"
        )
        st.session_state.chat_step = 1
        st.rerun()

    # ---- STEP 1: TOP 3 QUESTIONS ----
    if st.session_state.chat_step == 1:
        st.markdown("### ⭐ Frequently Asked")

        if st.button("🩺 Which doctor should I consult?"):
            user_say("Which doctor should I consult?")
            bot_say(
                "👨‍⚕️ You should consult a **Diabetologist or General Physician**.\n\n"
                "👉 https://www.google.com/maps/search/diabetologist+near+me"
            )
            st.session_state.chat_step = 2
            st.rerun()

        if st.button("🏥 Nearest hospitals"):
            user_say("Nearest hospitals")
            bot_say(
                "🏥 Find nearby hospitals here:\n\n"
                "👉 https://www.google.com/maps/search/diabetes+hospital+near+me"
            )
            st.session_state.chat_step = 2
            st.rerun()

        if st.button("🥗 How to prevent diabetes?"):
            user_say("How to prevent diabetes?")
            bot_say(
                "🛡️ Maintain healthy diet, exercise daily, and avoid excess sugar."
            )
            st.session_state.chat_step = 2
            st.rerun()

    # ---- STEP 2: NEXT 3 QUESTIONS ----
    if st.session_state.chat_step == 2:
        st.markdown("### 🔁 More Assistance")

        if st.button("🍎 Diet tips"):
            user_say("Diet tips")
            bot_say(
                "🥗 Eat vegetables, fruits, whole grains.\nAvoid junk food and sweets."
            )
            st.session_state.chat_step = 3
            st.rerun()

        if st.button("🏃 Exercise tips"):
            user_say("Exercise tips")
            bot_say(
                "🏃 30 minutes walking, yoga, or cycling daily is recommended."
            )
            st.session_state.chat_step = 3
            st.rerun()

        if st.button("🩸 Sugar control tips"):
            user_say("Sugar control tips")
            bot_say(
                "🩸 Regular checkups, balanced meals, and doctor consultation help."
            )
            st.session_state.chat_step = 3
            st.rerun()

    # ---- STEP 3: FINAL ----
    if st.session_state.chat_step == 3:
        st.markdown("### ✅ Anything else?")

        if st.button("📍 Find best doctors nearby"):
            user_say("Find best doctors nearby")
            bot_say(
                "👨‍⚕️ Top-rated doctors near you:\n\n"
                "👉 https://www.google.com/maps/search/best+diabetologist+near+me"
            )
            st.session_state.chat_step = 4
            st.rerun()

        if st.button("🙏 Thank you"):
            user_say("Thank you")
            bot_say(
                "🙏 You're welcome!\n\nTake care and stay healthy 😊"
            )
            st.session_state.chat_step = 4
            st.rerun()

    # ---- END ----
    if st.session_state.chat_step == 4:
        st.caption("Chat ended. Refresh page to restart.")



# ---------------- THEME ----------------
if dark_mode:
    bg_color = "#0E1117"
    text_color = "white"
    card_color = "#1C1E26"
else:
    bg_color = "white"
    text_color = "black"
    card_color = "#F4F6F6"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    .card {{
        background-color: {card_color};
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- LOAD DATA ----------------
df = pd.read_csv(
    r'C:\Users\PRERANA\Downloads\diabetes_prediction-master\diabetes_prediction-master\diabetes.csv'
)

# ---------------- HEADER ----------------
st.markdown(
    "<h1 style='text-align:center;'>🩺 Diabetes Prediction System</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center;'>AI-based Health Risk Assessment using Machine Learning</p>",
    unsafe_allow_html=True
)
st.divider()


# ---------------- SIDEBAR INPUT ----------------
st.sidebar.header("🧍 Patient Details")

def user_report():
    return pd.DataFrame({
        'Pregnancies': [st.sidebar.slider('🤰 Pregnancies', 0, 17, 3)],
        'Glucose': [st.sidebar.slider('🩸 Glucose', 0, 200, 120)],
        'BloodPressure': [st.sidebar.slider('💓 Blood Pressure', 0, 122, 70)],
        'SkinThickness': [st.sidebar.slider('📏 Skin Thickness', 0, 100, 20)],
        'Insulin': [st.sidebar.slider('💉 Insulin', 0, 846, 79)],
        'BMI': [st.sidebar.slider('⚖️ BMI', 0, 67, 20)],
        'DiabetesPedigreeFunction': [st.sidebar.slider('🧬 DPF', 0.0, 2.4, 0.47)],
        'Age': [st.sidebar.slider('🎂 Age', 21, 88, 33)]
    })

user_data = user_report()

# ---------------- INPUT VALIDATION ----------------
if user_data['Glucose'][0] == 0 or user_data['BMI'][0] == 0:
    st.warning("⚠️ Some input values look unrealistic. Please verify patient data.")

# ---------------- LAYOUT ----------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='card'><h3>📋 Patient Data</h3></div>", unsafe_allow_html=True)
    st.dataframe(user_data, use_container_width=True)

with col2:
    st.markdown("<div class='card'><h3>📊 Dataset Summary</h3></div>", unsafe_allow_html=True)
    st.write(df.describe())

st.divider()

# ---------------- MODEL ----------------
X = df.drop('Outcome', axis=1)
y = df['Outcome']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0
)

rf = RandomForestClassifier(random_state=0)
rf.fit(X_train, y_train)

user_data = user_data[X_train.columns]

prediction = rf.predict(user_data)
probability = rf.predict_proba(user_data)[0][1] * 100
accuracy = accuracy_score(y_test, rf.predict(X_test)) * 100

# ---------------- RESULT ----------------
st.markdown("<div class='card'><h3>🧪 Prediction Result</h3></div>", unsafe_allow_html=True)

if prediction[0] == 0:
    st.success("✅ You are NOT Diabetic")
else:
    st.error("⚠️ You are Diabetic")

st.metric("🎯 Model Accuracy", f"{accuracy:.2f} %")

from datetime import datetime

history_data = {
    "Date & Time": datetime.now().strftime("%d-%m-%Y %H:%M"),
    "Age": user_data['Age'].values[0],
    "BMI": user_data['BMI'].values[0],
    "Glucose": user_data['Glucose'].values[0],
    "Result": "Diabetic" if prediction[0] == 1 else "Not Diabetic",
    "Risk %": round(probability, 2)
}

st.session_state.user_history[st.session_state.username].append(history_data)


# ---------------- PROBABILITY BAR ----------------
st.subheader("📊 Diabetes Risk Probability")
st.progress(int(probability))
st.write(f"**Risk Probability:** {probability:.2f} %")

if probability < 30:
    st.success("🟢 Risk Level: LOW")
elif probability < 70:
    st.warning("🟠 Risk Level: MEDIUM")
else:
    st.error("🔴 Risk Level: HIGH")
# ---------------- DOCTOR CONSULTATION RECOMMENDATION ----------------
st.divider()
st.subheader("👨‍⚕️ Doctor Consultation Recommendation")

if probability >= 70:
    st.error("⚠️ High risk detected")
    if st.button("🩺 Consult a Doctor"):
        st.warning(
            "Please consult an endocrinologist or general physician for medical advice."
        )

elif probability >= 30:
    st.warning("⚠️ Medium risk detected")
    if st.button("🩺 Consult a Doctor"):
        st.info(
            "A preventive consultation with a doctor is recommended."
        )

else:
    st.success("✅ Low risk detected")
    st.info("Doctor consultation not required at this stage.")
# ---------------- BEST DOCTOR RECOMMENDATION ----------------
st.divider()
st.subheader("⭐ Best Doctor Recommendation (Based on Reviews)")

st.info(
    "Doctors are recommended based on Google Maps ratings and reviews."
)

if st.button("🔍 Find Best Nearby Doctors"):
    doctor_maps_link = (
        "https://www.google.com/maps/search/"
        "best+diabetes+doctor+near+me"
    )

    st.markdown(
        f"[👉 Click here to view top-rated doctors on Google Maps]({doctor_maps_link})"
    )


# ---------------- HEALTH TIPS & SUGGESTIONS ----------------
st.divider()
st.subheader("💡 Health Tips & Suggestions")

if probability < 30:
    st.success("🟢 You are at LOW risk. Maintain a healthy lifestyle.")
    st.markdown("""
    **🥗 Diet Tips**
    - Eat balanced meals with fruits and vegetables
    - Limit sugar and processed foods

    **🏃 Exercise**
    - 30 minutes of walking or light exercise daily

    **❤️ Lifestyle Advice**
    - Get enough sleep
    - Stay hydrated
    - Manage stress
    """)

elif probability < 70:
    st.warning("🟠 You are at MEDIUM risk. Lifestyle improvement is recommended.")
    st.markdown("""
    **🥗 Diet Tips**
    - Reduce sugar and refined carbohydrates
    - Increase fiber-rich foods
    - Avoid junk and fast food

    **🏃 Exercise**
    - Brisk walking, cycling, or yoga (30–45 minutes/day)

    **❤️ Lifestyle Advice**
    - Monitor weight regularly
    - Reduce stress
    - Avoid smoking and alcohol
    """)

else:
    st.error("🔴 You are at HIGH risk. Medical consultation is strongly advised.")
    st.markdown("""
    **🥗 Diet Tips**
    - Follow a low-sugar, low-carb diet
    - Avoid sugary drinks and sweets
    - Eat whole grains and green vegetables

    **🏃 Exercise**
    - Light to moderate exercise as advised by a doctor
    - Avoid overexertion

    **❤️ Lifestyle Advice**
    - Consult a doctor immediately
    - Monitor blood sugar regularly
    - Follow medical advice strictly
    """)


st.divider()


# ---------------- VISUAL COMPARISON ----------------
st.subheader("📈 Visual Comparison (Others vs You)")

color = "green" if prediction[0] == 0 else "red"

def plot_graph(y_col, title):
    fig = plt.figure()
    sns.scatterplot(x='Age', y=y_col, data=df, hue='Outcome', palette='coolwarm')
    sns.scatterplot(
        x=user_data['Age'],
        y=user_data[y_col],
        s=200,
        color=color,
        label="You"
    )
    plt.title(title)
    plt.legend()
    st.pyplot(fig)

colA, colB = st.columns(2)
with colA:
    plot_graph('Glucose', 'Age vs Glucose')
    plot_graph('BMI', 'Age vs BMI')

with colB:
    plot_graph('BloodPressure', 'Age vs Blood Pressure')
    plot_graph('Insulin', 'Age vs Insulin')
    st.subheader("🏥 Nearest Hospital (Live Location)")

st.info("📍 Hospitals are shown based on your current location using Google Maps")

if st.button("📍 Find Nearest Hospitals"):
    maps_link = "https://www.google.com/maps/search/diabetes+hospital+near+me"
    st.markdown(
        f"[👉 Click here to view nearby hospitals on Google Maps]({maps_link})"
    )




# ---------------- DOWNLOAD REPORT ----------------
st.subheader("📄 Download Health Report")

report_text = f"""
DIABETES PREDICTION REPORT
-------------------------
Age: {user_data['Age'].values[0]}
BMI: {user_data['BMI'].values[0]}
Glucose: {user_data['Glucose'].values[0]}
Blood Pressure: {user_data['BloodPressure'].values[0]}

Prediction: {"Diabetic" if prediction[0]==1 else "Not Diabetic"}
Risk Probability: {probability:.2f} %
Model Accuracy: {accuracy:.2f} %
"""

st.download_button(
    "⬇️ Download Report",
    report_text,
    file_name="diabetes_report.txt",
    mime="text/plain"
)

st.subheader("📜 Your Prediction History")

history_df = pd.DataFrame(
    st.session_state.user_history[st.session_state.username]
)

if not history_df.empty:
    st.dataframe(history_df, use_container_width=True)
else:
    st.info("No history available yet.")

# ---------------- FOOTER ----------------
st.markdown(
    """
    <hr>
    <p style='text-align:center; color:grey;'>
    Developed by abc |Project | Streamlit + Machine Learning
    </p>
    """,
    unsafe_allow_html=True
)
