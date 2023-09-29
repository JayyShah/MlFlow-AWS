import os

import mlflow
from mlflow.tracking import MlflowClient

# Specify Public URL of EC2 instance where the MLflow tracking server is running
TRACKING_SERVER_HOST = "<Public IPv4 DNS>"

mlflow.set_tracking_uri(f"http://{TRACKING_SERVER_HOST}:5000") 
print(f"Tracking Server URI: '{mlflow.get_tracking_uri()}'")

#specify name of experiment (will be created if it does not exist)
mlflow.set_experiment("my-test-exp") 

import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

# Load the sample dataset
data = load_iris()
X, y = data.data, data.target

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Enable MLflow autologging
mlflow.sklearn.autolog()

# Define a dictionary of classification models
models = {
    "Logistic Regression": LogisticRegression(),
    "Decision Tree": DecisionTreeClassifier(),
    "Random Forest": RandomForestClassifier()
}

# Train and log each classification model
for model_name, model in models.items():

    with mlflow.start_run():

        # Set the tag for name of user who ran the experiment
        mlflow.set_tag("User", "Jay Shah")
        
        # Train the model
        model.fit(X_train, y_train)
        
        # Evaluate the model on the test set
        accuracy = model.score(X_test, y_test)
        
        # Log model metrics
        mlflow.log_metric("Accuracy", accuracy)

        print(f"Artifacts URI: '{mlflow.get_artifact_uri()}'")