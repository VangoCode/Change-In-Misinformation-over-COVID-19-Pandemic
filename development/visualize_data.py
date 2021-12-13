"""
Visualizes the data of misinformation during the COVID-19 pandemic using the Pygame Library
and Sys Library.

Copyright and Usage Information
==================================================

All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2021 Ron Varshavsky and Elsie (Muhan) Zhu.
"""
import sys
import pygame
from pull_tweets_classes import generate_month_year_list, MonthYear
from visualize_data_classes import ButtonRow, PygameValues


def draw_game(pyval: PygameValues, month_year_list: list[MonthYear], data: list[float],
              current_misinformation: float) -> tuple[int, int, float]:
    """Draws the pygame screen so that we can visualize the data.

    Returns the current size of the square"""
    pyval.screen.fill((255, 255, 255))

    square_size = 300

    center_rect = pygame.Rect((pyval.width // 2 - square_size // 2,
                               pyval.height // 2 - square_size // 2 + 50,
                               square_size, square_size))

    # variable size, changes on which month you press
    full_rect = pygame.Rect((100, 0, 600, 100))
    variable_rect = pygame.Rect((100, 0, pyval.current_size, 100))

    variable_rect.centery = center_rect.centery
    full_rect.centery = center_rect.centery

    pygame.draw.rect(pyval.screen, (155, 155, 155), full_rect)
    pygame.draw.rect(pyval.screen, (255, 0, 0), variable_rect)

    cur_c = 0
    for i in range(3):
        pyval.button_rows[i].update_positions(pyval.width)
        pyval.button_rows[i].draw_row(pyval.screen, pyval.font, month_year_list, cur_c)
        button_clicked = pyval.button_rows[i].check_click(cur_c)
        if button_clicked != -1:
            for j in range(3):
                pyval.button_rows[j].update_all_colours((255, 0, 0))
            pyval.button_rows[i].update_colour(button_clicked, (0, 255, 0))
            pyval.target_size = round(1000 * data[button_clicked])
            current_misinformation = data[button_clicked]

        if pyval.target_size - pyval.current_size < 0:
            pyval.current_size -= 1
        if pyval.target_size - pyval.current_size > 0:
            pyval.current_size += 1

        cur_c += len(pyval.button_rows[i])

    pyval.screen.blit(pyval.font.render('Misinformation Found: '
                                        + str(round(current_misinformation * 100, 1))
                                        + '% of tweets',
                                        True, (0, 0, 0)), (10, 150))

    return pyval.current_size, pyval.target_size, current_misinformation


# CODE PARTLY TAKEN FROM TUTORIAL 4
def visualize() -> None:
    """Starts a pygame window to visualize the data filtered"""
    pygame.init()
    in_play = True

    button_rows = [ButtonRow(0, 50), ButtonRow(50, 50),
                   ButtonRow(2 * 50, 50)]

    with open('outputted_myths.txt_percent-values', mode='r', encoding='utf-8') as file:
        # ACCUMULATOR
        data = []

        for line in file:
            data.append(float(line[9:].strip()))

    for i in range(3):
        for _ in range(7):
            button_rows[i].add_button()

    pygame.display.set_caption('Twitter Misinformation Visualizer')
    font = pygame.font.SysFont('Arial', 28)
    month_year_list = generate_month_year_list()
    current_size = 0
    current_misinformation = 0.0
    target_size = current_size

    while in_play:
        for event in pygame.event.get():  # Check for any events
            if event.type == pygame.QUIT:  # If user clicked close
                in_play = False

        screen = pygame.display.set_mode((800, 600))
        pyval = PygameValues(screen, 800, 600, button_rows, font, current_size, target_size)

        current_size, target_size, current_misinformation = draw_game(pyval, month_year_list,
                                                                      data, current_misinformation)

        pygame.display.update()

    pygame.display.quit()
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # Leave this code uncommented when you submit your files.
    #
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts', 'pygame', 'sys', 'pull_tweets_classes',
                          'visualize_data_classes'],
        'allowed-io': ['visualize'],
        # HERE. All functions that use I/O must be stated here. For example,
        #   if do_this() has print in, then add 'do_this()' to allowed-io.
        'max-line-length': 100,
        'disable': ['R1705', 'C0200'],
        'generated-members': ['pygame.*']
    })

    import python_ta.contracts

    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()
