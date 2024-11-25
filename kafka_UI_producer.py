import streamlit as st
from confluent_kafka import Producer
import json

# Konfigurasi Kafka Producer dengan confluent_kafka
producer_config = {
    'bootstrap.servers': 'localhost:9092'  
}
producer = Producer(producer_config)

def send_message(topic, value):
    producer.produce(topic, value=json.dumps(value))
    producer.flush()

# Streamlit form
st.title("Credit Risk Prediction")

with st.form("credit_risk_form"):
    person_home_ownership = st.selectbox("Home Ownership", ["RENT", "OWN", "MORTGAGE"])
    loan_intent = st.selectbox("Loan Intent", ["PERSONAL", "EDUCATION", "DEBT CONSOLIDATION"])
    loan_grade = st.selectbox("Loan Grade", ["A", "B", "C", "D", "E", "F", "G"])
    person_age = st.number_input("Age", min_value=0, step=1)
    person_income = st.number_input("Income", min_value=0.0, step=0.1)
    person_emp_length = st.number_input("Employment Length (in years)", min_value=0, step=1)
    loan_amnt = st.number_input("Loan Amount", min_value=0.0, step=0.1)
    loan_int_rate = st.number_input("Interest Rate", min_value=0.0, step=0.1)
    cb_person_cred_hist_length = st.number_input("Credit History Length (in years)", min_value=0, step=1)

    submitted = st.form_submit_button("Submit")

if submitted:
    message = {
        "person_home_ownership": person_home_ownership,
        "loan_intent": loan_intent,
        "loan_grade": loan_grade,
        "person_age": person_age,
        "person_income": person_income,
        "person_emp_length": person_emp_length,
        "loan_amnt": loan_amnt,
        "loan_int_rate": loan_int_rate,
        "cb_person_cred_hist_length": cb_person_cred_hist_length
    }
    try:
        send_message('loan_applications', message)
        st.success("Pesan berhasil dikirim ke Kafka!")
    except Exception as e:
        st.error(f"Error: {e}")
