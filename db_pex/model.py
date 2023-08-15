import numpy as np

from sklearn import datasets, linear_model

import mlflow
import mlflow.sklearn
from mlflow.tracking.client import MlflowClient

class PexModel:
    def train(self):
        print(f"Loading dataset")
        # Load the diabetes dataset
        diabetes_X, diabetes_y = datasets.load_diabetes(return_X_y=True)

        # Use only one feature
        diabetes_X = diabetes_X[:, np.newaxis, 2]

        # Split the data into training/testing sets
        diabetes_X_train = diabetes_X[:-20]
        diabetes_X_test = diabetes_X[-20:]

        # Split the targets into training/testing sets
        diabetes_y_train = diabetes_y[:-20]
        diabetes_y_test = diabetes_y[-20:]

        print(f"Initiating mlflow")

        mlflow_experiment_name = "/Users/srijit.nair@databricks.com/pex_poc"
        mlflow.set_tracking_uri("databricks")
        mlflow.set_experiment(experiment_name=mlflow_experiment_name)
        experiment = mlflow.get_experiment_by_name(mlflow_experiment_name)
        mlflow.sklearn.autolog()

        print(f"Starting training")
        with mlflow.start_run(experiment_id=experiment.experiment_id) as mlflow_run:

            # Create linear regression object
            regr = linear_model.LinearRegression()

            # Train the model using the training sets
            regr.fit(diabetes_X_train, diabetes_y_train)

            print(f"Logging model")
            mlflow.sklearn.log_model(regr, "pex_poc_model")

            print(f"Training done..registering model")
            artifact_path = "model"
            run_id = mlflow.active_run().info.run_id
            model_uri = f"runs:/{run_id}/{artifact_path}"
            model_details = mlflow.register_model(model_uri=model_uri, name="db_pex")


    def predict(self, data):
        
        print("Getting model")
        mlflow.set_tracking_uri("databricks")
        client = MlflowClient()
        model_name = "db_pex"
        latest_version_info = client.get_latest_versions(model_name, stages=["None"])
        latest_version = latest_version_info[0].version
        print(f"The latest production version {latest_version}")
        model_version_uri = f"models:/{model_name}/{latest_version}"
        model = mlflow.pyfunc.load_model(model_version_uri)
        result = model.predict(data)
        print(result)