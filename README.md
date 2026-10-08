# App Review Platform

An interactive Streamlit dashboard for exploring and analyzing mobile app reviews.

This project was developed during my work with FocusKPI and demonstrates an end-to-end workflow for collecting, processing, tagging, and visualizing app-review data.

## Overview

The App Review Platform transforms raw mobile app reviews into an interactive dashboard that makes customer feedback easier to explore and understand.

The project includes:

- App review data collection and cleaning
- Review tagging and categorization
- Interactive review analysis
- Sentiment and rating exploration
- Dynamic filtering and visualizations
- CSV upload support
- Built-in demo data for exploring the dashboard without uploading a dataset

## Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- OpenAI API
- Google Play and Apple App Store review data

## Project Workflow

### 1. Data Collection & Cleaning

Reviews are collected from mobile app stores and prepared for downstream analysis.

The workflow includes data cleaning, normalization, and preprocessing to create a structured review dataset.

### 2. App Review Tagging

Reviews are categorized to help identify common themes and patterns within customer feedback.

This stage explores automated tagging and structured classification of review text.

### 3. Streamlit Dashboard

The processed data is presented through an interactive Streamlit application.

Users can upload a CSV dataset or load the built-in demo dataset to explore the dashboard.

## Run Locally

Install the required packages:

```bash
pip install -r requirements.txt
```

Then launch the application:

```bash
streamlit run app_v2.py
```

## Requirements

The deployed dashboard requires:

```text
streamlit
pandas
plotly
numpy
```

## Author

**Aurora Olaya**

Data Scientist / Analytics Engineer

M.S. Information and Data Science — UC Berkeley  
B.A. Mathematics — UC Santa Barbara
