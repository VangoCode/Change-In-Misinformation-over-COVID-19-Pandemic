import pygame
import sys
from pull_tweets_classes import generate_month_year_list, MonthYear
from visualize_data_classes import ButtonRow


# CODE TAKEN FROM TUTORIAL 4
def visualize() -> None:
    """Starts a pygame window to visualize the data filtered"""
    pygame.init()
    in_play = True

    width = 800
    height = 600

    button_height = 50
    button_rows = [ButtonRow(0, button_height), ButtonRow(button_height, button_height),
                   ButtonRow(2 * button_height, button_height)]

    file = open('outputted_myths.txt_percent-values', mode='r', encoding='utf-8')
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
    current_size = 300
    current_misinformation = 0.0
    target_size = current_size

    while in_play:
        for event in pygame.event.get():  # Check for any events
            if event.type == pygame.QUIT:  # If user clicked close
                in_play = False

        screen = pygame.display.set_mode((width, height))

        current_size, target_size, current_misinformation = draw_game(screen, width, height,
                                                                      button_rows, font,
                                                                      month_year_list, data,
                                                                      current_size, target_size,
                                                                      current_misinformation)

        pygame.display.update()

    pygame.display.quit()
    pygame.quit()
    sys.exit()


def draw_game(screen: pygame.display, width: int, height: int, button_rows: list[ButtonRow],
              font: pygame.font, month_year_list: list[MonthYear], data: list[float],
              current_size: int, target_size: int, current_misinformation: float) -> tuple[int, int, float]:
    """Draws the pygame screen so that we can visualize the data.

    Returns the current size of the square"""
    screen.fill((255, 255, 255))

    square_size = 300

    center_rect = pygame.Rect((width // 2 - square_size // 2, height // 2 - square_size // 2 + 50,
                               square_size, square_size))

    # variable size, changes on which month you press
    variable_rect = pygame.Rect((0, 0, current_size, current_size))

    variable_rect.center = center_rect.center

    pygame.draw.rect(screen, (255, 0, 0), variable_rect)

    cur_c = 0
    for i in range(3):
        button_rows[i].update_positions(width)
        button_rows[i].draw_row(screen, font, month_year_list, cur_c)
        button_clicked = button_rows[i].check_click(screen, cur_c)
        if button_clicked != -1:
            for j in range(3):
                button_rows[j].update_all_colours((255, 0, 0))
            button_rows[i].update_colour(button_clicked, (0, 255, 0))
            target_size = round(1000 * data[button_clicked])
            current_misinformation = data[button_clicked]

        if target_size - current_size < 0:
            current_size -= 1
        if target_size - current_size > 0:
            current_size += 1

        cur_c += len(button_rows[i])

    screen.blit(font.render('Misinformation Found: ' + str(round(current_misinformation * 100, 1)) + '% of tweets',
                            True, (0, 0, 0)), (10, 150))

    return current_size, target_size, current_misinformation
