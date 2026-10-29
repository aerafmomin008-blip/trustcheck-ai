# TrustCheckAI

TrustCheckAI is a machine learning based web application that helps assess website trustworthiness using a trained model and website data.

## Features

- Web interface for checking website trust
- Machine learning model for prediction
- Model training script
- Website datasets used for the project
- Result page for displaying predictions

## Tech Stack

- Python
- Machine Learning
- Pandas
- NumPy
- HTML and CSS

## Project Structure

    trustcheck-ai/
    |-- app.py
    |-- train_model.py
    |-- requirements.txt
    |-- model/
    |   `-- model.pkl
    |-- data/
    |   `-- websites.csv
    |-- static/
    |-- templates/
    |-- website_trust_dataset.csv
    `-- websites.csv

## Getting Started

1. Clone the repository:

    git clone https://github.com/aerafmomin008-blip/trustcheck-ai.git
    cd trustcheck-ai

2. Install the required libraries:

    pip install -r requirements.txt

3. Train the model if required:

    python train_model.py

4. Run the application:

    python app.py

## Author

Aeraf Naeem Momin  
BSc Artificial Intelligence and Machine Learning Student  
Pune, India
