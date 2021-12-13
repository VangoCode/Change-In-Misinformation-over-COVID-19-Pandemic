"""The main Python file for COVID-19 Misinformation Over Time

Copyright and Usage Information
==================================================

All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2021 Ron Varshavsky and Elsie (Muhan) Zhu.
"""
import compute_similarity
import visualize_data
import pull_tweets


if __name__ == '__main__':
    # sort data into months
    pull_tweets.sort_by_month()
    # generate a file that contains the amount of myths detected for each month
    compute_similarity.output_myths_count_into_file('outputted_myths.txt')
    # draw the visual representation of the data
    visualize_data.visualize()
