"""
Randomly pulls valid tweets using their IDs from the Twitter dataset and writes them into a file
sorted by month using our twitter_post module, the CSV library, and the list of month-year
combinations generated from pull_tweets_classes.py

Copyright and Usage Information
==================================================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2021 Ron Varshavsky and Elsie (Muhan) Zhu.
"""

import twitter_post
import csv
from pull_tweets_classes import generate_month_year_list


def isolate_ids() -> None:
    """Isolates the ID's of the Twitter dataset. Writes the new ID's to a file."""
    f = open("./data/twitter_ids", "w")

    with open('data/COVID19_twitter_full_dataset.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            id = list(row)[0].split(',')[0]
            f.write(id + '\n')
    f.close()


def check_post_valid(id: str, f):
    """Returns if a twitter post exists by its id"""
    server = twitter_post.ServerManager()
    user = twitter_post.ClientManager()

    # call the getQuery() method
    user.get_query(id)
    # build the server response
    user.call_server(server)

    if server.response != '':
        f.write(str(server.response) + '\n')


def pull_direct_tweets() -> None:
    """Pulls the direct Twitter ID's for 900 tweets (rate limit)"""
    f = open('./data/filtered_twitter_ids_random_20', 'w', encoding='utf-8')

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
        files_open.append(open(file, mode='w', encoding='utf-8'))

    with open('./data/filtered_twitter_ids_compiled', encoding='utf-8') as f:
        for line in f:
            stripped = line.strip().split(' ')
            for i in range(len(month_year_list)):
                if month_year_list[i].month + month_year_list[i].year \
                        == stripped[2] + stripped[6][:4]:
                    index = 119  # the index where the text begins
                    while line[index] != "'":
                        index += 1
                    files_open[i].write(line[118:index] + '\n')

    for file in files_open:
        file.close()


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
