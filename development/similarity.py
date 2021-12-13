"""A module which uses the FuzzyWuzzy libary to dictate if two strings are similar,
implying they contain misinformation.

Copyright and Usage Information
==================================================

All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited.

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

    sentences = phrase.split('.')  # split the phrase into sentences

    for negation_word in negation_words:
        for sentence in sentences:
            if negation_word in sentence.lower():
                return True
    return False


if __name__ == '__main__':
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # Leave this code uncommented when you submit your files.
    #
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts'],
        'allowed-io': ['run_example_break'],
        # HERE. All functions that use I/O must be stated here. For example, if do_this() has print in, then add 'do_this()' to allowed-io.
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })

    import python_ta.contracts

    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()
