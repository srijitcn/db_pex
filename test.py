from db_pex.model import PexModel
from sklearn import datasets
import numpy as np


def test():
    # Load the diabetes dataset
    diabetes_X, diabetes_y = datasets.load_diabetes(return_X_y=True)

    # Use only one feature
    diabetes_X = diabetes_X[:, np.newaxis, 2]
    diabetes_X_test = diabetes_X[-20:]

    PexModel().predict(diabetes_X_test)

if __name__ == "__main__":
    test()