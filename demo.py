import streamlit as st
import pandas as pd
import pymysql
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

# Sidebar navigation
page = st.sidebar.radio("Go to", ["Project Introduction", "Dashboard", "Data Visualization", "SQL Queries", "Prediction Model", "Creator Info"])

# Local MySQL connection using PyMySQL
@st.cache_resource
def get_connection():
    try:
        return pymysql.connect(
            host="localhost",
            user="root",
            password="1234",
            database="police_ledger"
        )
    except Exception as e:
        st.error(f"❌ Database connection failed: {e}")
        return None

# Reusable function to fetch query results
def get_data(query, params=None):
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cur.execute(query, params or ())
        return pd.DataFrame(cur.fetchall())
    except Exception as e:
        st.error(f"❌ Query failed: {e}")
        return pd.DataFrame()
    finally:
        cur.close()

# --- Page 1: Project Introduction ---
if page == "Project Introduction":
    st.title("🚨 SecureCheck: Police Stop Log Analyzer")
    st.subheader("📊 A Streamlit App for Real-Time Vehicle Stop Monitoring")
    st.write("""
    This project improves police check post operations using Python, SQL, and Streamlit.
    - Real-time logging of stops
    - Violation and arrest analytics
    - Interactive visualizations and prediction
    """)

# --- Page 2: Dashboard ---
elif page == "Dashboard":
    st.title("🚨 SecureCheck Dashboard")
    st.subheader("Live Insights from Police Check Posts")
    try:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Stops", get_data("SELECT COUNT(*) AS count FROM traffic_stops")["count"][0])
        col2.metric("Total Arrests", get_data("SELECT COUNT(*) AS count FROM traffic_stops WHERE is_arrested = TRUE")["count"][0])
        col3.metric("Drug-Related Stops", get_data("SELECT COUNT(*) AS count FROM traffic_stops WHERE drugs_related_stop = TRUE")["count"][0])

        countries = get_data("SELECT DISTINCT country_name FROM traffic_stops")["country_name"].tolist()
        selected_country = st.selectbox("Filter by Country", countries)
        df = get_data("SELECT * FROM traffic_stops WHERE country_name = %s", (selected_country,))

        if not df.empty:
            df["stop_hour"] = pd.to_datetime(df["stop_time"], errors="coerce").dt.hour
            fig, ax = plt.subplots()
            sns.barplot(x=df["stop_hour"].value_counts().sort_index().index,
                        y=df["stop_hour"].value_counts().sort_index().values,
                        palette="Blues_r", ax=ax)
            st.pyplot(fig)

            if "violation" in df.columns:
                fig2, ax2 = plt.subplots()
                ax2.pie(df["violation"].value_counts(), labels=df["violation"].value_counts().index,
                        autopct="%1.1f%%", startangle=90)
                ax2.axis("equal")
                st.pyplot(fig2)

            selected_date = st.date_input("Filter by Date")
            filtered = get_data("SELECT * FROM traffic_stops WHERE country_name = %s AND stop_date = %s",
                                (selected_country, selected_date.strftime("%Y-%m-%d")))
            st.dataframe(filtered)
        else:
            st.warning("No data found for this country.")
    except Exception as e:
        st.error(f"⚠️ Unexpected error: {e}")

# --- Page 3: Data Visualization ---
elif page == "Data Visualization":
    st.title("📊 Interactive Data Visualization")
    countries = get_data("SELECT DISTINCT country_name FROM traffic_stops")["country_name"].tolist()
    selected_country = st.selectbox("Select Country", countries)
    chart_type = st.radio("Chart Type", ["Stops by Hour", "Arrest by Age", "Gender Breakdown"])
    df = get_data("SELECT * FROM traffic_stops WHERE country_name = %s", (selected_country,))

    if not df.empty:
        if chart_type == "Stops by Hour":
            df["hour"] = pd.to_datetime(df["stop_time"], errors="coerce").dt.hour
            st.plotly_chart(px.histogram(df, x="hour", nbins=24, title="Stops by Hour"))
        elif chart_type == "Arrest by Age":
            st.plotly_chart(px.histogram(df[df["is_arrested"] == True], x="driver_age", nbins=10, title="Arrests by Age"))
        elif chart_type == "Gender Breakdown":
            st.plotly_chart(px.pie(df, names="driver_gender", title="Gender Breakdown"))

# --- Page 4: SQL Queries ---
elif page == "SQL Queries":
    st.title("📋 SQL Query Viewer")
    queries = {
        "Top 10 Vehicles in Drug-Related Stops":
            "SELECT vehicle_number, COUNT(*) AS Stop_Count FROM traffic_stops WHERE drugs_related_stop = TRUE GROUP BY vehicle_number ORDER BY Stop_Count DESC LIMIT 10",
        "Driver Age Group with Highest Arrests":
            "SELECT driver_age, COUNT(*) AS Arrest_Count FROM traffic_stops WHERE is_arrested = TRUE GROUP BY driver_age ORDER BY Arrest_Count DESC LIMIT 5",
        "Gender Distribution of Stops":
            "SELECT driver_gender, COUNT(*) AS Total_Stops FROM traffic_stops GROUP BY driver_gender",
        "Common Violations by Drivers < 25":
            "SELECT violation, COUNT(*) AS Count FROM traffic_stops WHERE driver_age < 25 GROUP BY violation ORDER BY Count DESC",
        "Country with Most Drug-Related Stops":
            "SELECT country_name, COUNT(*) AS Drug_Stops FROM traffic_stops WHERE drugs_related_stop = TRUE GROUP BY country_name ORDER BY Drug_Stops DESC LIMIT 1"
    }
    selected_query = st.selectbox("Choose a Query", list(queries.keys()))
    st.dataframe(get_data(queries[selected_query]))

# --- Page 5: Prediction Model ---
elif page == "Prediction Model":
    st.title("🔮 Arrest Prediction Model")

    # ✅ Define df before using it
    df = get_data("SELECT driver_age, driver_gender, violation, is_arrested FROM traffic_stops WHERE driver_age IS NOT NULL")

    if not df.empty:
        df.dropna(inplace=True)

        le_gender = LabelEncoder()
        le_violation = LabelEncoder()

        df["driver_gender"] = le_gender.fit_transform(df["driver_gender"])
        df["violation"] = le_violation.fit_transform(df["violation"])

        X = df[["driver_age", "driver_gender", "violation"]]
        y = df["is_arrested"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        model = LogisticRegression()
        model.fit(X_train, y_train)

        age = st.slider("Driver Age", 16, 80, 25)
        gender = st.selectbox("Gender", le_gender.classes_)
        violation = st.selectbox("Violation", le_violation.classes_)

        input_df = pd.DataFrame([[age,
                                  le_gender.transform([gender])[0],
                                  le_violation.transform([violation])[0]]],
                                columns=["driver_age", "driver_gender", "violation"])

        pred = model.predict(input_df)[0]
        st.write(f"**Prediction:** {'🚨 Arrest Likely' if pred else '✅ No Arrest Likely'}")
    else:
        st.warning("No data available to train the model.")
# --- Page 6: Creator Info ---
elif page == "Creator Info":
    st.title("👩‍💻 Project Created By")
    st.markdown("""
    **Name**: Nijas  
    **Project**: SecureCheck – A Police Stop Monitoring System  
    **Tools**: Python, Streamlit, MySQL (Local), pandas, matplotlib, scikit-learn  
    """)
