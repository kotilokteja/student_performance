# EdTech Academic Risk Early-Warning System

An academic risk prediction system that uses student performance and academic information to identify students who may be at risk and provide an early warning through a web application.

## About the Project

The project was developed to explore how machine learning can be used to identify students who may need additional academic support.

The system analyzes student-related information such as:

* Study time
* Absences
* Previous failures
* First-period grade (G1)
* Second-period grade (G2)
* Other academic and personal factors

Based on these inputs, the system predicts whether a student is **At Risk** or **Not At Risk**.

## Dataset

The project uses the Student Performance dataset containing **649 student records**.

The academic risk dataset contains:

* **348 — Not At Risk**
* **301 — At Risk**

## Machine Learning

The project includes:

* Data preparation
* Academic risk target creation
* Feature analysis
* Model training
* Model evaluation
* Student risk prediction

The model was evaluated using accuracy, precision, recall, F1-score, and a confusion matrix.

### Model Results

| Metric                | Result |
| --------------------- | -----: |
| Accuracy              |    93% |
| Not At Risk Precision |    98% |
| Not At Risk Recall    |    89% |
| Not At Risk F1-score  |    93% |
| At Risk Precision     |    88% |
| At Risk Recall        |    98% |
| At Risk F1-score      |    93% |

## Web Application

The project includes a web interface with the following sections:

* **Dashboard** — Overview of student and risk data
* **Risk Assessment** — Enter student information and generate a prediction
* **Model Performance** — View model evaluation results
* **Dataset Insights** — Explore patterns and statistics in the dataset
* **About** — Information about the project

## Project Structure

```text
AcademicRiskProject/
│
├── app.py
├── src/
│   ├── create_target.py
│   ├── feature_analysis.py
│   └── evaluate_model.py
│
├── dataset/
│   └── student-por.csv
│
├── model/
│
├── requirements.txt
└── README.md
```

The exact structure may vary depending on the final version of the project.

## Running the Project

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

The application will open in your browser.

## Purpose

This project is intended as an early-warning and academic-support tool. The prediction should be treated as an indicator that can help identify students who may require additional attention, rather than as a definitive judgment about a student's academic ability.

## Future Improvements

Possible future improvements include:

* Using a larger and more diverse dataset
* Adding more academic indicators
* Improving model performance
* Adding historical performance tracking
* Providing personalized recommendations
* Adding teacher or administrator dashboards

## Project Status

Completed as an academic machine-learning and web application project.
