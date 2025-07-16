# 🚦 SecureCheck: Traffic Stop Data Analysis & Arrest Prediction Dashboard

**SecureCheck** is a data-driven dashboard built with **Streamlit**, connected to a **MySQL** database, offering insightful visualizations and an AI-powered **arrest prediction model**. It helps analyze traffic stop data based on location, time, driver demographics, and violations.

## 📊 Features

- **Interactive Dashboard**: Visualize stop trends, demographics, violations, and arrest patterns.
- **Time Series Analysis**: View stops by year, month, and hour using SQL time functions.
- **Driver Violation Patterns**: Filter by country, gender, age, and race.
- **ML Prediction Model**: Predict likelihood of arrest based on driver age, gender, and violation type.
- **Clean UI**: Built using Streamlit components and responsive design.

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io)
- **Backend**: Python + MySQL (via PyMySQL)
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Data Handling**: Pandas
- **Machine Learning**: Scikit-learn (Logistic Regression, Label Encoding)
- **SQL**: Joins, Subqueries, Group By, Window Functions

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/securecheck-dashboard.git
   cd securecheck-dashboard
   
2. Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt

3. Set up your .env file with database credentials:

ini
Copy
Edit
DB_HOST=localhost
DB_USER=youruser
DB_PASSWORD=yourpassword
DB_NAME=yourdatabase
DB_PORT=3306

4.Run the app:

bash
Copy
Edit
streamlit run app.py

📁 Folder Structure

bash
Copy
Edit
securecheck-dashboard/
├── app.py                # Main Streamlit app
├── db.py                 # MySQL database connection
├── utils.py              # Utility functions
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (DB creds)
└── README.md             # Project documentation

📌 Sample Use Cases

Law enforcement agencies analyzing arrest trends

Policy researchers studying racial or age-based violations

ML model deployment for real-time arrest prediction

📬 Contact
 
Built by Nijas
For questions or collaboration, feel free to reach out!
nijikhan123@gmail.com
