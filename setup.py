from setuptools import setup, find_packages

setup(
    name="NLP_app",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "nltk",
        "spacy",
        "textblob",
        "pdfplumber", 
        "gtts",
    ],
)
