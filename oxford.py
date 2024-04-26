import re
from spellchecker import SpellChecker

def normalize_repeated_characters(text):
    """Normalize repeated characters in the given text."""
    normalized_text = re.sub(r'(.)\1+', r'\1\1', text)
    return normalized_text

def spellcheck(text):
     """Checks for misspelled words and corrects it."""
     spell = SpellChecker()
     normalized_text = normalize_repeated_characters(text)
     words = normalized_text.split()
    #  print(words)
     misspelled = spell.unknown(words)
     corrected_text = [spell.correction(word) if word in misspelled else word for word in words]
    #  print(corrected_text)
     return corrected_text

spellcheck("soooo happpppppy")