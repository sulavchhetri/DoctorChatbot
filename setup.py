from setuptools import setup, find_packages

setup(
    name="doctorchatbot",
    version="0.1",
    description="This is a chatbot that predicts the disease based on the symptoms",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "joblib"
    ],
)