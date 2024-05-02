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
    # print(corrected_text)
    return corrected_text

def sentiment_analysis(text):
    """Returns the compound sentiment score of the user input."""
    corrected_text = spellcheck(text)
    stop_words = set(stopwords.words("english"))
    filtered_tokenized_text = [word for word in corrected_text if word.isalnum() and word not in stop_words]
    filtered_text = " ".join(filtered_tokenized_text)
    filtered_text = re.sub(r'[\U00010000-\U0010ffff]', lambda match: f":{match.group(0)[1:]}:", filtered_text)
    # print(filtered_text)

    sentiment_score = SentimentIntensityAnalyzer().polarity_scores(filtered_text)["compound"]
    print(sentiment_score)
    return sentiment_score

def categorize_mood(sentiment_score):
    mood_categories = {
        "happy": (0.5, 1.0),
        "sad": (-1.0, -0.5),
        "bored": (0, 0.3),
        "excited": (0.7, 1.0),
        "depressed": (-1.0, -0.8),
        "anxious": (-0.7, -0.8),
        "angry": (-0.8, -0.5),
        "calm": (0.3, 0.5)
    }
    for mood, score_range in mood_categories.items():
        lower_bound, upper_bound = score_range
        if lower_bound <= sentiment_score <= upper_bound:
            return mood
    
    return "Sorry, I'm not sure I understand what you are saying."

def main():
    # print(sentiment_analysis())
    text = input("How are you feeling right now: ")
    sentiment_score = sentiment_analysis(text)

    print(categorize_mood(sentiment_score))
    
if __name__ == "__main__":
     main()