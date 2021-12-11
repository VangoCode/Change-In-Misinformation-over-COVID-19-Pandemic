import similarity
from pull_tweets_classes import generate_month_year_list


def compute_misinformation_count_for_month(month: str, year: str) -> (int, int):
    """Returns the number of misinformation detected for the month inputted as well as the rate"""
    filename = './data/' + str.capitalize(month) + year

    count = 0
    total = 0
    myth_set = get_myths()

    with open(filename, mode='r', encoding='utf-8') as f:
        for line in f:
            for myth in myth_set:
                if similarity.is_misinformation(line, myth):
                    count += 1
            total += 1
    return count, count / total


def get_myths() -> set[str]:
    """Returns a list of myths in str format"""
    # ACCUMULATOR
    myths = set()

    with open('./myths/extracted_myths.txt') as f:
        for line in f:
            myths.add(line.strip().lower())

    with open('./myths/extra_added_myths.txt') as f:
        for line in f:
            myths.add(line.strip().lower())

    return myths


def get_myths_for_every_month() -> [list[int], list[int]]:
    """Computes the misinformation counts that were generated for every month available
        in the dataset"""
    # ACCUMULATORS
    misinformation_count_list = []
    misinformation_rate_list = []

    month_year_list = generate_month_year_list()

    print('--------\nGENERATING MISINFORMATION COUNTS\n--------')

    for item in month_year_list:
        count = compute_misinformation_count_for_month(item.month,
                                                       item.year)
        misinformation_count_list.append(count[0])
        misinformation_rate_list.append(count[1])
        print('Generated misinformation count for ' + item.month + ' ' + item.year + ": ")
        print('Hard Values: ' + str(misinformation_count_list[-1]) + '\tPercent Values: ' +
              str(misinformation_rate_list[-1]) + '\n--------')

    return [misinformation_count_list, misinformation_rate_list]


def output_myths_count_into_file(filename: str) -> None:
    """Generates a file with filename that contains the amount of myths detected for each month"""
    generated_myths_count = get_myths_for_every_month()
    month_year_list = generate_month_year_list()

    with open(filename + '_hard-values', mode='w', encoding='utf-8') as f:
        for i in range(len(month_year_list)):
            f.write(month_year_list[i].month + month_year_list[i].year + ': ' + str(generated_myths_count[0][i]) + '\n')

    with open(filename + '_percent-values', mode='w', encoding='utf-8') as f2:
        for i in range(len(month_year_list)):
            f2.write(month_year_list[i].month + month_year_list[i].year + ': ' + str(generated_myths_count[1][i]) + '\n')
