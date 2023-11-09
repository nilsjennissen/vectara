# LLM Power Hybrid Search by Vectara 

## Introduction

Welcome to the LLM Power Hybrid Search project! This project is dedicated to building a powerful and efficient text corpus and retriever for legal documents using Vectara. Our goal is to explore the possibilities in new ways of legal professionals search for information, making it faster, easier, and more accurate.

## What you need 

To use LLM Power Hybrid Search, you need the following:
- OpenAI API Key


## Features

- **Text Corpus**: A large and structured set of texts that serve as the foundation for our search engine.
- **Retriever**: An advanced algorithm that scans the text corpus to find the most relevant legal documents based on the user's query.
- **Vectara Integration**: Utilizes the powerful capabilities of Vectara to enhance the efficiency and accuracy of the search process.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

To install LLM Power Hybrid Search, follow these steps:

1. Clone the repo: `git clone https://github.com/nilsjennissen/vectara.git`
2. Add a .streamlit folder to the root directory: `mkdir ~/.streamlit` and `touch ~/.streamlit/secrets.toml`
3. Setup Vectara Account and enter your own corpus details in the secrets.toml file 
4. Upload documents to Vectara 
5. Install the required packages from requirements.txt: `pip install -r requirements.txt`
6. Run the app: `streamlit run streamlit_app.py`
7. Set your OpenAI API Key and start searching!
