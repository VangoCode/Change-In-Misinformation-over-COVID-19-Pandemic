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
    user.getQuery(id)
    # build the server response
    user.callServer(server)

    if server.response is not False:
        f.write(str(server.response) + '\n')


def pull_direct_tweets() -> None:
    """Pulls the direct Twitter ID's for 900 tweets (rate limit)"""
    f = open('./data/filtered_twitter_ids_random_20', 'w', encoding='utf-8')

    with open('./data/twitter_ids') as data:
        next(data)  # skip first line
        for i in range(334 * 7):
            next(data)

        for i in range(242 * 50):
            next(data)

        for i in range(90 * 150):
            next(data)

        for i in range(628 * 1200):
            next(data)

        for i in range(637 * 1200):
            next(data)

        for i in range(650 * 1500):
            next(data)

        for i in range(661 * 1500):
            next(data)

        for i in range(235 * 2100):
            next(data)

        for i in range(402 * 4500):
            next(data)

        for i in range(700 * 12000):
            next(data)

        for i in range(713 * 25000):
            next(data)

        for i in range(712 * 30000):
            next(data)

        for i in range(711 * 30000):
            next(data)

        for i in range(704 * 30000):
            next(data)

        for i in range(725 * 30000):
            next(data)

        for i in range(724 * 30000):
            next(data)

        for i in range(770 * 30000):
            next(data)

        for i in range(377 * 30000):
            next(data)

        for i in range(413 * 30000):
            next(data)

        for i in range(364 * 30000):
            next(data)

        for line in data:
            check_post_valid(line.strip(), f)
            for i in range(30000):  # skip n lines
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
        file = item.month + item.year
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
