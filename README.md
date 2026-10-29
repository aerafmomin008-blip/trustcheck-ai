# TrustCheckAI

TrustCheckAI is a machine learning based web application that helps assess website trustworthiness using a trained model and website data.

## Features

- Web interface for checking website trust
- Machine learning model for prediction
- Model training script
- Website datasets used for the project
- Simple result page for displaying predictions

## Tech Stack

- Python
- Machine Learning
- HTML and CSS
- Pandas
- NumPy

## Project Structure

```text
trustcheck-ai/
├── app.py                       # Main application
├── train_model.py               # Model training script
├── requirements.txt             # Project dependencies
├── model/
│   └── model.pkl                # Trained ML model
├── data/
│   └── websites.csv             # Dataset
├── static/                      # CSS and images

git clone https://github.com/aerafmomin008-blip/trustcheck-ai.git
cd trustcheck-ai

pip install -r requirements.txt

python train_model.py

python app.py
├── templates/                   # HTML pages
├── website_trust_dataset.csv
└── websites.csv
