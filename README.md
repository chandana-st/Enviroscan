**Project Report** : **EnviroScan:AI-Powered Pollution Source Identifier using Geospatial Analytics**

**Project Overview**

EnviroScan is an air pollution monitoring and prediction system developed using machine learning. It integrates real-time data and historical datasets to analyze pollution levels and provide predictions through an interactive dashboard. The system helps users understand environmental conditions and take necessary precautions.

----------------------------------------------------------------------------------------------------------------------------------------------------------------

**Problem Statement**

Air pollution is one of the most critical environmental challenges affecting urban and rural areas worldwide. Traditional air quality monitoring systems focus on measuring pollutant concentrations such as PM2.5, PM10, NO₂, CO, and SO₂. 

However, these systems do not identify the specific source of pollution, making it difficult for authorities to implement targeted mitigation strategies.
Without accurate source identification, it becomes challenging to determine whether pollution originates from vehicular traffic, industrial emissions, agricultural activities, or natural causes.

---------------------------------------------------------------------------------------------------------------------------------------------------------------

**Objectives**

Collect real-time air pollution data from external APIs.

Train machine learning models to classify pollution sources.

Visualize pollution patterns using geospatial heatmaps.

Develop an interactive dashboard for monitoring pollution levels.

---------------------------------------------------------------------------------------------------------------------------------------------------------------

**Motivation**

The motivation behind this project is to create awareness about air pollution and its harmful effects. By providing predictions and insights, the system helps users take preventive actions and supports better environmental decision-making.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------

**Technologies** 

• Python

• Pandas, NumPy

• Scikit-learn

• Matplotlib, Seaborn

• Folium (maps)

• Streamlit

• Open AQ, OpenWeather, Groq API's

• GitHub

----------------------------------------------------------------------------------------------------------------------------------------------------------------

**System Architecture**

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/e694d9a2-68d0-49f1-9782-7b1463e21bb4" />


--------------------------------------------------------------------------------------------------------------------------------------------------------------

**Methodology**

The EnviroScan project follows a structured workflow to ensure accurate data processing, prediction, and visualization of air pollution levels. The methodology is divided into the following stages:

**1. Data Collection**

• Air pollution data is collected from reliable sources such as historical datasets and real-time APIs.

• The dataset includes major pollutants like PM2.5, PM10, NO₂, CO, and SO₂.

• Weather-related parameters such as temperature, humidity, and wind speed are also included.

**2. Data Preprocessing**

• Handling missing values using suitable techniques (mean/median filling).

• Removing duplicate and irrelevant data entries.

• Converting data into a consistent format for analysis.

• Normalizing or scaling data using min max.

**3. Exploratory Data Analysis (EDA)**

• Analyzing data distribution and identifying patterns.

• Visualizing pollutant trends over time.

<img width="2400" height="1200" alt="image" src="https://github.com/user-attachments/assets/e389897d-eb39-4d31-aa6e-2188296d3b02" />

• Generating correlation heatmaps to understand relationships between variables.

**4. Feature Engineering & Selection**

• Selecting important features that influence pollution levels.

• Creating new features if needed (e.g., combining weather factors).

• Removing less relevant features to improve model efficiency.

**5. Model Building**

Applying machine learning algorithms such as:

Decision Tree

Random Forest

XGBoost

Gradient Boosting

**6. Model Evaluation**

**SMOTE (Synthetic Minority Oversampling Technique)**

It is used to handle class imbalance in the dataset by generating synthetic samples for minority classes. This helps improve model performance and avoids biased predictions.

**Performance Evaluation Metrics**

The models are evaluated using standard classification metrics such as:

• Accuracy

• Precision

• Recall

• F1-Score

• Confusion Matrix

**Model Comparison**

Different machine learning models such as Decision Tree, Random Forest, and XGBoost are compared based on their performance metrics to identify the most accurate and reliable model.

**Cross-Validation**

Cross-validation techniques are used to ensure that the model performs well on unseen data and to reduce overfitting.

**Hyperparameter Tuning**

Model parameters are fine-tuned using techniques like Grid Search or Random Search to improve prediction accuracy and overall performance.

**7. Prediction**

The trained machine learning model is used to identify the probable source of pollution based on input features.

Generating outputs from real-time and user input data

The system takes real-time data (API) or user-provided inputs and predicts the likely source of pollution such as industrial, vehicular, or natural sources.

**8. Visualization**

**Graphical Visualization**

Pollution data is represented using graphs such as line charts, bar charts, and trend plots to understand variations over time.

<img width="2100" height="750" alt="image" src="https://github.com/user-attachments/assets/56c28923-2303-4611-a3b5-4ec1dc486e78" />


**Heatmaps**

Heatmaps are used to show the correlation between different pollutants and environmental factors. They help in identifying strong relationships and patterns in the dataset.

<img width="1800" height="1350" alt="image" src="https://github.com/user-attachments/assets/1cf34949-a0fb-4e04-bdf8-96964fe9eabd" />


**Geospatial Visualization (Folium)**

Interactive maps are created using Folium to display pollution levels across different locations. Marker maps and heatmaps are used to highlight highly polluted areas.

**SHAP (Explainable AI Visualization)**

SHAP (SHapley Additive exPlanations) is used to explain the impact of each feature on model predictions. It helps in understanding how different factors contribute to pollution levels.

**Waterfall Plot**

A Waterfall Plot explains how each feature contributes to a single prediction.

Each bar = one feature

Red → increases prediction

Blue → decreases prediction

<img width="800" height="650" alt="image" src="https://github.com/user-attachments/assets/a62daf00-4057-4bc7-b41f-c35536b6465b" />

**Beeswarm Plot (Summary Plot)**

A Beeswarm Plot shows feature importance for the entire dataset.

Each dot = one data point

Red → high feature value

Blue → low feature value

Shows overall model behavior

<img width="864" height="680" alt="image" src="https://github.com/user-attachments/assets/f95791da-85b7-4885-befa-2a78f048e39c" />

**Interactive Dashboard Visualization**

All visualizations are integrated into the Streamlit dashboard, allowing users to interact with the data and explore results easily..

**Deployment**

Developing an interactive dashboard using Streamlit.

Integrating real-time API data into the system.

Deploying the application on Streamlit Cloud.

Making the system accessible through a web link.

---------------------------------------------------------------------------------------------------------------------------------------------------------------

**Results**

The system successfully predicts pollution levels and displays them through interactive visualizations. It helps users understand pollution trends and make informed decisions.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Challenges**   

API integration issues

Handling missing and inconsistent data

Improving model accuracy

Class imbalance in dataset affects model performance (handled using SMOTE).

Interactive visualizations (Folium maps) can slow down with large datasets.

LLM APIs may cause response delays, higher cost, and dependency issues.

Ensuring accurate responses from LLMs (avoiding hallucinations) is challenging.

Managing API keys securely during deployment is difficult.

Managing large files and maintaining a structured GitHub repository is difficult.

----------------------------------------------------------------------------------------------------------------------------------------------------------------

**Future Scope**

Integration with IoT sensors

Mobile application development

Use of advanced AI models

Expansion to multiple cities

-----------------------------------------------------------------------------------------------------------------------------------------------------------------

**Conclusion**

Successfully developed an AI-powered pollution source identification system using machine learning and geospatial analytics.

Overcame limitations of traditional systems by identifying actual pollution sources, not just pollutant levels. 

The Gradient Boosting model provided high accuracy and reliable predictions. 


