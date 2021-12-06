"""A module which uses the FuzzyWuzzy libary to dictate if two strings are similar.

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Ron Varshavsky, and Elsie (Muhan) Zhu.
"""
from fuzzywuzzy import fuzz


def is_misinformation(phrase: str, sample: str) -> bool:
    """Return if phrase is misinformation ars according to sample

    Preconditions:
        - phrase != ''
        - sample = ''

    >>> is_misinformation('5G waves DO NOT spread COVID-19', '5G Waves Cause COVID-19')
    False
    >>> is_misinformation('5G waves spread COVID-19', '5G Waves Cause COVID-19')
    True
    """

    return any(check_similarity_score(sentence, sample)
               and not is_false_positive(sentence) for sentence in phrase.split('.'))


def check_similarity_score(phrase: str, sample: str) -> bool:
    """Return the similarity score between the phrase, and a sample from the article.

    If the function considers it has found a match, return True, otherwise, return False.

    Preconditions:
        - phrase != ''
        - sample != ''

    >>> check_similarity_score("fuzzy was a bear", "fuzzy fuzzy was a bear")
    True
    >>> check_similarity_score("My cousin in Trinidad won’t get the vaccine cuz his friend got it & became impotent." \
                                "His testicles became swollen. His friend was weeks away from getting married, now" \
                                 "the girl called off the wedding. So just pray on it & make sure you’re comfortable" \
                                  "with ur decision, not bullied", "vaccine swollen testicles")
    True
    >>> check_similarity_score("The vaccine booster shot does not protect against the new omicron variant.", \
        "vaccine lowers risk of severe disease with COVID-19")
    False
    """
    threshold = 70.0
    score = fuzz.token_set_ratio(sample.lower(), phrase.lower())
    if score >= threshold:
        return True
    return False


def is_false_positive(phrase: str) -> bool:
    """Returns whether check_similarity_score accidentally caught a false positive.

    This is done by checking if the phrase flagged is actually a negation of the original phrase.

    Preconditions:
        - phrase != ''

    >>> is_false_positive('5G waves DO NOT spread COVID-19')
    True
    >>> is_false_positive('5G waves DO spread COVID-19')
    False
    """
    with open('texts/negation_words.txt') as f:
        negation_words = f.read().splitlines()  # if you do f.readlines(), will be \n at the end

    # TODO: make this more sophisticated (sometimes it catches true positives as false positives.
    #   ex, when Nicki Minaj tweeted about the vaccine making testicles swell, her tweet says the
    #   word won't, which is a negation so it triggers false positive
    # TODO: split word into sentences, try to figure out an algorithm for when words are similar
    #   i.e, swollen vs. swell vs. swelling ,etc.
    # TODO: consider a thesaurus API
    # TODO: token sort ratio for words which appear in sample (i.e check swell and swollen with
    #   similar words function)

    for negation_word in negation_words:
        if negation_word in phrase.lower():
            return True
    return False
