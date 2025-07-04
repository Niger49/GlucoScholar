# -*- coding: utf-8 -*-
"""GlucoScholar.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1DgxoD4lvvY6HlIE_fFs8rwIKdoNU2506

## **📦 Installs**
"""

# pip install pandas scikit-learn datasets pytesseract opencv-python-headless wikipedia-api wikipedia

"""## **⚙️ Random Forest Interface Function**"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import matplotlib.pyplot as plt
import time
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
import random
import re

class randomForest:
    """ Columns
      gender (categorical encoded)
      age
      hypertension
      heart_disease
      smoking_history (categorical encoded)
      bmi
      HbA1c_level
      blood_glucose_level
      diabetes
    """
    def __init__(self, test_size=0.2, random_state=42):
        self.csv_link = "https://gist.githubusercontent.com/sharna33/218183b8151378720081809c92b92235/raw/f949bf5752e27a99a44f34b685568801e57dbfe0/diabetes_prediction_dataset.csv"
        self.result_column_name = "diabetes"
        self.random_state = random_state
        self.model = RandomForestClassifier(random_state=self.random_state)
        self.X = None
        self.y = None
        self.test_size = test_size
        self.gender_encoder = LabelEncoder()
        self.smoking_history_encoder = LabelEncoder()

        # Use self.csv_link to access the instance variable
        df = pd.read_csv(self.csv_link)

        df['gender'] = self.gender_encoder.fit_transform(df['gender'])
        df['smoking_history'] = self.smoking_history_encoder.fit_transform(df['smoking_history'])

        self.X = df.drop(self.result_column_name, axis=1)
        self.y = df[self.result_column_name]

        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=self.test_size, random_state=self.random_state)
        self.model.fit(X_train, y_train)

    def predict(self, new_patient):
        prediction = self.model.predict(new_patient)
        return prediction

    def bulkPrediction(self, csv_link, limit=0):
        df = pd.read_csv(csv_link)

        # Apply Label Encoding to 'gender' and 'smoking_history' columns
        df['gender'] = self.gender_encoder.transform(df['gender'])
        df['smoking_history'] = self.smoking_history_encoder.transform(df['smoking_history'])

        if limit != 0:
            df = df.head(limit)

        # Drop the 'diabetes' column before prediction
        df = df.drop(self.result_column_name, axis=1)

        predictions = []
        for index in df.index:
            row_data = df.loc[[index]].values.tolist()
            prediction = self.predict(row_data)
            predictions.extend(prediction)

        return predictions

    def getEncoding(self):
        # Get mappings for gender
        gender_mapping = {index: label for index, label in enumerate(self.gender_encoder.classes_)}
        print("Gender Mapping:", gender_mapping)

        # Get mappings for smoking history
        smoking_history_mapping = {index: label for index, label in enumerate(self.smoking_history_encoder.classes_)}
        print("Smoking History Mapping:", smoking_history_mapping)
        return

"""## **🤖Plot Class For Bot**"""

class ploting_charts:
    def __init__(self):
        return

    def pieChart(self, data, labels, title="Pie Chart"):
        """
        Generates a pie chart with labels and percentages in the legend.

        Args:
            data (list): A list of numerical values representing the data.
            labels (list): A list of labels for the data slices.
            title (str, optional): The title of the chart. Defaults to "Pie Chart".
        """
        plt.figure(figsize=(6, 6))

        # Explode the pie chart slices
        #explode = (0.1, 0)  # Removed to avoid issues with label placement

        # Calculate percentages
        total = sum(data)
        percentages = [(x / total) * 100 for x in data]

        # Create the pie chart with percentage labels and start angle
        wedges, texts, autotexts = plt.pie(data, labels=labels, autopct='%1.1f%%', startangle=90,  shadow=True)
        # Create custom legend labels with percentages
        legend_labels = ['{0} - {1:1.1f} %'.format(i,j) for i,j in zip(labels, percentages)]

        # Add the legend
        plt.legend(wedges, legend_labels, loc="best", bbox_to_anchor=(1, 0, 0.5, 1))


        plt.title(title)
        plt.axis('equal')
        plt.show()

    def barChart(self, data, labels, title="Bar Chart", xlabel="X-axis", ylabel="Y-axis"):
        """
        Generates a bar chart.

        Args:
            data (list): A list of numerical values representing the data.
            labels (list): A list of labels for the bars.
            title (str, optional): The title of the chart. Defaults to "Bar Chart".
            xlabel (str, optional): The label for the x-axis. Defaults to "X-axis".
            ylabel (str, optional): The label for the y-axis. Defaults to "Y-axis".
        """
        plt.figure(figsize=(8, 6))  # Adjust figure size as needed
        plt.bar(labels, data)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()
## **🔍 Image & Info Modules**"""

import cv2
import pytesseract
from googlesearch import search

class ImageProcessor:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        # return

    def extract_text(self, image_path):
        """
        Extracts text from an image using Tesseract OCR.

        Args:
            image_path (str): Path to the image file.

        Returns:
            str: Extracted text from the image.
        """
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        return text.strip()

class InformationFetcher:
    def __init__(self):
        pass

    def clean_query(self, text):
        # Enhanced keyword extraction for better DuckDuckGo results
        keywords = []
        medical_terms = ['diabetes', 'glucose', 'hba1c', 'blood sugar',
                       'insulin', 'hyperglycemia', 'diabetic', 'blood test']

        text_lower = text.lower()
        for term in medical_terms:
            if term in text_lower:
                keywords.append(term)

        # If no medical terms found, use first few words
        if not keywords:
            words = text.split()[:3]
            keywords = [word for word in words if len(word) > 2]

        # Create search query optimized for medical content
        search_query = " ".join(keywords)
        print(f"Search Query: {search_query}")
        return search_query.strip()


    def google_search(self, text):
        """
        Search using DuckDuckGo (more reliable than Google for programmatic access)
        """
        try:
            # Clean and prepare search query
            query = self.clean_query(text)

            # Perform search using DuckDuckGo
            results = []
            try:
                with DDGS() as ddgs:
                    # Search for medical/health related content
                    search_results = ddgs.text(
                        query + " diabetes health medical",
                        max_results=10,
                        safesearch='moderate'
                    )

                    for result in search_results:
                        url = result.get('href', '')
                        if self.is_valid_url(url):
                            results.append(url)
                        if len(results) >= 5:
                            break

            except Exception as e:
                print(f"DuckDuckGo search failed: {e}")
                return self.get_default_urls()

            return results if results else self.get_default_urls()

        except Exception as e:
            print(f"Search error: {e}")
            return self.get_default_urls()

    def is_valid_url(self, url):
        # Filter out Google search URLs and verify it's a proper medical resource
        if any(x in url.lower() for x in [
            'google.com/search',
            'google.com/url',
            'google.com/webhp'
        ]):
            return False

        # Check for medical/diabetes related domains
        valid_domains = [
            'diabetes.org',
            'nih.gov',
            'who.int',
            'mayoclinic.org',
            'medlineplus.gov',
            'webmd.com',
            'healthline.com',
            'medicalnewstoday.com',
            'cdc.gov',
            'diabetesjournals.org',
            'pubmed.ncbi.nlm.nih.gov'
        ]
        return any(domain in url.lower() for domain in valid_domains)

    def get_default_urls(self):
        return [
            "https://www.diabetes.org/diabetes",
            "https://www.niddk.nih.gov/health-information/diabetes",
            "https://www.who.int/health-topics/diabetes"
        ]