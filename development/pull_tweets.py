"""
Randomly pulls valid tweets using their IDs from the Twitter dataset and writes them into a file
sorted by month using our twitter_post module, the CSV library, and the list of month-year
combinations generated from pull_tweets_classes.py

Copyright and Usage Information
==================================================

All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2021 Ron Varshavsky and Elsie (Muhan) Zhu.
"""

from typing import IO
import csv
import twitter_post
from pull_tweets_classes import generate_month_year_list, MonthYear


def isolate_ids() -> None:
    """Isolates the ID's of the Twitter dataset. Writes the new ID's to a file."""

    with open("./data/twitter_ids", "w") as f:
        with open('data/COVID19_twitter_full_dataset.csv') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                row_id = list(row)[0].split(',')[0]
                f.write(row_id + '\n')


def check_post_valid(row_id: str, f: IO) -> None:
    """Writes to file f if the twitter post exists by its id"""
    server = twitter_post.ServerManager()
    user = twitter_post.ClientManager()

    # call the getQuery() method
    user.get_query(row_id)
    # build the server response
    user.call_server(server)

    if server.response != '':
        f.write(str(server.response) + '\n')


def pull_direct_tweets() -> None:
    """Pulls the direct Twitter ID's for 900 tweets (rate limit)"""
    # cannot use with for this because we pass f as a parameter into a helper function
    #   keep in mind, we close it at the end.
    f = open('./data/filtered_twitter_ids_random', 'w', encoding='utf-8')

    with open('./data/twitter_ids') as data:
        next(data)  # skip first line

        for line in data:
            check_post_valid(line.strip(), f)
            for _ in range(30000):  # skip n lines
                next(data)
    f.close()


def compile_into_file() -> None:
    """Compiles the set of 'randomly' pulled tweets into a single file"""
    with open('./data/filtered_twitter_ids_compiled', encoding='utf-8', mode='w') as f:
        for i in range(1, 20):
            with open('./data/filtered_twitter_ids_random_' + str(i), encoding='utf-8') as f2:
                for line in f2:
                    f.write(line)


def sort_by_month() -> None:
    """Sorts the tweets which were compiled into a single file by the month and year they were
        posted"""
    month_year_list = generate_month_year_list()

    files_open = []
    for item in month_year_list:
        file = './data/' + item.month + item.year
        # this is a list of open files, it would be tedious to use with open for all of these
        files_open.append(open(file, mode='w', encoding='utf-8'))

    with open('./data/filtered_twitter_ids_compiled', encoding='utf-8') as f:
        for line in f:
            stripped = line.strip().split(' ')
            for i in range(len(month_year_list)):
                isolate_text_write_to_file(month_year_list, files_open, stripped, i, line)

    for file in files_open:
        file.close()


def isolate_text_write_to_file(month_year_list: list[MonthYear], files_open: list[IO],
                               stripped: list[str], i: int, line: str) -> None:
    """A helper function for sort_by_month() which isolates for the text of the line, and
        writes it to the file

    Representation Invariants:
        - month_year_list == generate_month_year_list()
        - files_open != []
        - all files in files_open are open
        - len(line) >= 119
    """
    if month_year_list[i].month + month_year_list[i].year \
            == stripped[2] + stripped[6][:4]:
        index = 119  # the index where the text begins
        while line[index] != "'":
            index += 1
        files_open[i].write(line[118:index] + '\n')


if __name__ == '__main__':
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # Leave this code uncommented when you submit your files.
    #
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts', 'twitter_post', 'csv', 'pull_tweets_classes'],
        'allowed-io': ['isolate_ids', 'pull_direct_tweets', 'compile_into_file', 'sort_by_month'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })

    import python_ta.contracts

    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()
