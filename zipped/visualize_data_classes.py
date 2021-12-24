"""
Creates a row of buttons using the Pygame Library.

Copyright and Usage Information
==================================================

All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2021 Ron Varshavsky and Elsie (Muhan) Zhu.
"""
from dataclasses import dataclass
from typing import Optional
import pygame
from pull_tweets_classes import MonthYear


@dataclass
class Button:
    """A class that creates a button for pygame

    Instance Attributes:
        - x: the x-position of the button
        - y: the y-position of the button
        - width: the width of the button
        - height: the height of the button
        - text: the text of the button
        - colour: the colour of the button outline

    Representation Invariants:
        - 0 <= self.x <= 800
        - 0 <= self.y <= 600
        - 0 <= self.width <= 800
        - 0 <= self.height <= 600
        - all(0 <= i <= 255 for i in self.colour)
    """
    x: Optional[int] = 0
    y: Optional[int] = 0
    width: Optional[int] = 100
    height: Optional[int] = 100
    text: Optional[str] = ''
    colour: Optional[tuple[int, int, int]] = (255, 0, 0)


class ButtonRow:
    """A class that pertains to a row of buttons

    Stores the buttons and draws them relative to the number of buttons in a row

    Instance Attributes:
        - num_of_buttons: the number of buttons in the row
        - y: the y-position of the number row, where y is the top of the buttons
        - height: the height of the buttons
    """
    # Private Instance Attributes:
    #   - buttons: a list containing the buttons in the row. The list is ordered left-to-right
    _buttons: list[Button]
    num_of_buttons: int
    y: int
    height: int

    def __init__(self, y: int, height: int) -> None:
        """Initalize an empty row of buttons"""
        self._buttons = []
        self.num_of_buttons = 0
        self.y = y
        self.height = height

    def __len__(self) -> int:
        """Returns the number of buttons"""
        return self.num_of_buttons

    def add_button(self) -> None:
        """Adds a button to the row of buttons

        >>> buttons = ButtonRow(0, 100)
        >>> buttons.add_button()
        >>> buttons._buttons
        [Button(x=0, y=0, width=100, height=100)]
        >>> buttons.num_of_buttons
        1
        """
        self._buttons.append(Button(y=self.y, height=self.height))
        self.num_of_buttons += 1

    def remove_button(self, position: int) -> Button:
        """Removes a button from the row of buttons at position which is indexed to 1.

        Returns the button which was removed

        Representation Invariants:
            - self.buttons != []
            - 1 <= position <= len(buttons)

        >>> buttons = ButtonRow(5, 200)
        >>> buttons.add_button()
        >>> buttons._buttons
        [Button(x=0, y=5, width=100, height=200)]
        >>> buttons.num_of_buttons
        1
        >>> buttons.remove_button(1)
        Button(x=0, y=5, width=100, height=200)
        >>> buttons._buttons
        []
        >>> buttons.num_of_buttons
        0
        """
        self.num_of_buttons -= 1
        return self._buttons.pop(position - 1)

    def update_positions(self, screen_width: int) -> None:
        """Updates every button in the button row

        Representation Invariants:
            - self.num_of_buttons <= screen_width <= 1920

        >>> buttons = ButtonRow(0, 0)
        >>> buttons.add_button()
        >>> buttons.update_positions(800)
        >>> buttons._buttons
        [Button(x=0, y=0, width=800, height=0)]
        >>> buttons.add_button()
        >>> buttons.y = 200
        >>> buttons.height = 200
        >>> buttons.update_positions(800)
        >>> buttons._buttons
        [Button(x=0, y=200, width=400, height=200), Button(x=400, y=200, width=400, height=200)]
        """
        self._update_button_x_positions(screen_width)
        self._update_button_y_positions()

    def update_all_colours(self, colour: tuple[int, int, int]) -> None:
        """Mutates self to change all colours of _buttons to match colour"""
        for button in self._buttons:
            button.colour = colour

    def update_colour(self, button_index: int, colour: tuple[int, int, int]) -> None:
        """Mutates self to change button at button_index to colour"""
        button_index = button_index % 7
        self._buttons[button_index].colour = colour

    def draw_row(self, screen: pygame.display, font: pygame.font, month_year: list[MonthYear],
                 cur_c: int) -> None:
        """Draws the button row in a pygame screen"""
        c = cur_c
        for button in self._buttons:
            pygame.draw.rect(screen, button.colour,
                             (button.x, button.y, button.width, button.height), 1)
            screen.blit(font.render(month_year[c].month + ' ' + month_year[c].year,
                                    True, button.colour), (button.x + 5, button.y + 5))
            c += 1

    def check_click(self, cur_c: int) -> int:
        """Returns the number of the button that was clicked. If no button was clicked return -1"""
        c = cur_c
        if pygame.mouse.get_pressed(3)[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for button in self._buttons:
                if button.x <= mouse_x <= button.x + button.width and \
                        button.y <= mouse_y <= button.y + button.height:
                    return c
                c += 1
        return -1

    def _calculate_button_x_positions(self, screen_width: int) -> list[tuple[int, int]]:
        """Calculates the x, and width of the buttons based on the number of buttons in the
            row

        Representation Invariants:
            - self.num_of_buttons <= screen_width <= 1920

        >>> buttons = ButtonRow(0, 0)
        >>> buttons.add_button()
        >>> buttons._calculate_button_x_positions(800)
        [(0, 800)]
        >>> buttons.add_button()
        >>> buttons._calculate_button_x_positions(800)
        [(0, 400), (400, 400)]
        """
        # ACCUMULATOR
        positions = []

        widths = screen_width // self.num_of_buttons

        for i in range(self.num_of_buttons):
            positions.append((i * widths, widths))

        return positions

    def _update_button_x_positions(self, screen_width: int) -> None:
        """Updates every button in the button row's position so that it is evenly spread in a row

        >>> buttons = ButtonRow(0, 100)
        >>> buttons.add_button()
        >>> buttons.add_button()
        >>> buttons._update_button_x_positions(800)
        >>> buttons._buttons
        [Button(x=0, y=0, width=400, height=100), Button(x=400, y=0, width=400, height=100)]
        """
        new_positions = self._calculate_button_x_positions(screen_width)

        for i in range(len(self._buttons)):
            self._buttons[i].x = new_positions[i][0]
            self._buttons[i].width = new_positions[i][1]

    def _update_button_y_positions(self) -> None:
        """Updates every button in the button row's position and height so that it matches its
            y and height

        >>> buttons = ButtonRow(0, 100)
        >>> buttons.add_button()
        >>> buttons.add_button()
        >>> buttons.y = 200
        >>> buttons._update_button_y_positions()
        >>> buttons._buttons
        [Button(x=0, y=200, width=100, height=100), Button(x=0, y=200, width=100, height=100)]
        """
        for button in self._buttons:
            button.y = self.y
            button.height = self.height


@dataclass
class PygameValues:
    """A dataclass that collects all of the values surrounding pygame"""
    screen: pygame.display
    width: int
    height: int
    button_rows: list[ButtonRow]
    font: pygame.font
    current_size: int
    target_size: int


if __name__ == '__main__':
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # Leave this code uncommented when you submit your files.
    #
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts', 'pygame', 'pull_tweets_classes'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })

    import python_ta.contracts

    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()
