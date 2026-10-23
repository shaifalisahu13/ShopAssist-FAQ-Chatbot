# ShopAssist - FAQ Chatbot 🛍️

ShopAssist is a Python-based FAQ chatbot that answers common online shopping questions about orders, payments, delivery, returns, and refunds.

## Features

- Answers frequently asked shopping questions.
- Uses Natural Language Processing (NLP) for text preprocessing.
- Matches user questions with FAQs using TF-IDF and cosine similarity.
- Provides an interactive chat interface using Streamlit.
- Maintains conversation history during the session.
- Includes a clear conversation option.

## Technologies Used

- Python
- NLTK
- Scikit-learn
- Streamlit
- JSON

## Project Structure

```text
ShopAssist-FAQ-Chatbot/
├── app.py
├── chatbot.py
├── preprocessing.py
├── data/
│   └── faqs.json
├── tests/
│   └── test_chatbot.py
├── requirements.txt
└── .gitignore
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/shaifalisahu13/ShopAssist-FAQ-Chatbot.git
cd ShopAssist-FAQ-Chatbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
streamlit run app.py
```

The chatbot will open in your web browser.

## How It Works

1. Loads predefined FAQs from a JSON file.
2. Preprocesses questions using NLTK.
3. Converts FAQ questions into numerical vectors using TF-IDF.
4. Uses cosine similarity to find the most relevant question.
5. Returns the matching answer when the similarity score meets the configured threshold.

## Purpose

This project was developed as part of my AI internship task to practice NLP, text similarity, and chatbot development.

## Author

**Shaifali Sahu**

GitHub: [shaifalisahu13](https://github.com/shaifalisahu13)
