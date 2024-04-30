import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from spellchecker import SpellChecker

def normalize_repeated_characters(text):
    """Normalize repeated characters in the given text."""
    normalized_text = re.sub(r'(.)\1+', r'\1\1', text)
    return normalized_text

def spellcheck(text):
    """Checks for misspelled words and corrects it."""
    spell = SpellChecker()
    tokenized_words = word_tokenize(text.lower())
    tokenized_words = " ".join(tokenized_words)
    #  print(tokenized_words)
    normalized_text = normalize_repeated_characters(tokenized_words)
    words = normalized_text.split()
    #  print(words)
    misspelled = spell.unknown(words)
    corrected_text = [spell.correction(word) if word in misspelled else word for word in words]
    print(corrected_text)
    return corrected_text

def sentiment_analysis():
    """Returns the sentiment score of the user input."""
    text = input("Tell us how you feel right now: ")

    corrected_text = spellcheck(text)
    stop_words = set(stopwords.words("english"))
    filtered_tokenized_text = [word for word in corrected_text if word.isalnum() and word not in stop_words]
    filtered_text = " ".join(filtered_tokenized_text)
    filtered_text = re.sub(r'[\U00010000-\U0010ffff]', lambda match: f":{match.group(0)[1:]}:", filtered_text)
    print(filtered_text)

    sentiment_score = SentimentIntensityAnalyzer().polarity_scores(filtered_text)
    return sentiment_score

def categorize_mood():
    mood_categories = {
        "happy": 0.1,
        "sad": -0.1,
        "bored": -0.5,
        "excited": 0.5,
        "depressed": -0.8,
        "anxious": -0.7,
        "angry": -0.6,
        "calm": 0.3
    } # The ranges for each categories need to be updated to avoid overlap, while inclusive of all sentiment scores.
    pass

def main():
     print(sentiment_analysis())
    
if __name__ == "__main__":
     main()