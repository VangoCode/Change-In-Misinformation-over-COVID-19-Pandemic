"""The main python file for COVID-19 misinformation over time"""
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
