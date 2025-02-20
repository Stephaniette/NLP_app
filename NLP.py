import streamlit as st
import os
import sys

# Add this at the beginning of your script
if not os.path.exists(os.path.join(os.path.dirname(sys.executable), "en_core_web_sm")):
    st.info("Downloading language model for the first time... This may take a while.")
    os.system("python -m spacy download en_core_web_sm")
    st.experimental_rerun()
import streamlit as st  # Create the web-based interactive UI
import nltk  # Provides tokenization of words and sentences
# Downloading required nltk files
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import spacy  # Handles part-of-speech tagging
from textblob import TextBlob  # Perform sentiment analysis
import pdfplumber  # Extract text from PDF documents
from gtts import gTTS  # Convert text into audio/speech
import os


# python -m spacy download en_core_web_sm
import subprocess
import spacy

# Ensure the spaCy model is downloaded
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

def tokenize_text(text):
    words = word_tokenize(text)
    sentences = sent_tokenize(text)
    return words, sentences

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    filtered_text = [word for word in words if word.lower() not in stop_words]
    return " ".join(filtered_text)

def pos_tagging(text):
    doc = nlp(text)
    return [(token.text, token.pos_) for token in doc]

def name_entity_recognition(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

def sentiment_analysis(text):
    analysis = TextBlob(text)  # Perform sentiment analysis
    return analysis.sentiment.polarity  # Polarity ranges from (-1 to 1)

def pdf_to_audio(pdf_file):
    pdf_text = ""  # Initialize empty string for text storage
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pdf_text += text + " "  # Append text correctly
    if not pdf_text.strip():
        return None  # Handle empty PDF content
    
    tts = gTTS(text=pdf_text, lang='fr')
    audio_path = "audiobook.mp3"
    tts.save(audio_path)
    return audio_path

# Streamlit App
st.set_page_config(page_title="NLP Mini Project", layout="wide")  # Set the page title and layout
st.title("NLP Mini Project")  # Set the heading
st.write("Explore various NLP tasks with this interactive app")

option = st.sidebar.selectbox("Select an NLP task:", ['Tokenization', 'Stop Word Removal', 'POS Tagging', 'Name Entity Recognition', 'Sentiment Analysis', 'PDF to Audio'])

if option == "PDF to Audio":
    st.header("PDF to Audio Conversion")
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"], help="Only text-based PDFs are supported")
    if uploaded_file is not None:
        audio_file = pdf_to_audio(uploaded_file)
        if audio_file:
            st.audio(audio_file, format='audio/mp3')
            st.success("Audio Generated Successfully!")
        else:
            st.error("Could not extract text from the PDF. Ensure it is not a scanned document")
else:
    st.header(f'{option}')  # Display the selected NLP task
    text_input = st.text_area('Enter text here')  # User input
    
    if st.button('Run NLP task'):
        if not text_input.strip():
            st.warning('Please enter some text before running an NLP task')
        else:
            if option == 'Tokenization':
                words, sentences = tokenize_text(text_input)
                st.write('Words:', words)
                st.write('Sentences:', sentences)
            elif option == 'Stop Word Removal':
                st.write('Filtered Text:', remove_stopwords(text_input))
            elif option == 'POS Tagging':
                st.write('POS Tags:', pos_tagging(text_input))
            elif option == 'Name Entity Recognition':
                st.write('Named Entities:', name_entity_recognition(text_input))
            elif option == 'Sentiment Analysis':
                polarity = sentiment_analysis(text_input)
                st.write('Sentiment Score:', polarity)
