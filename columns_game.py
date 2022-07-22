import pygame
import columns_mechanics
import random

class ColumnsGame:
    def __init__(self):
        self._running = True
        self._state = columns_mechanics.ColumnsState()
        self._row = 12        
        self._col = 6
        self._whether_new_faller = True
        self._faller = None

    def run(self) -> None:
        '''run the game'''
        pygame.init()

        self._resize_surface((300,600))

        clock = pygame.time.Clock()

        self._new_game()

        time = 0
        
        while self._running:
            clock.tick(30)
            self._new_faller_or_not()
            if self._whether_new_faller:
                self._faller = self._state.new_faller(self._rand_faller_command())
            time += 1
            if time == 0 or time % 30 == 0:
                self._state.time_passage(self._faller)
            self._handle_events(self._faller)
            self._redraw()
            

        pygame.quit()

    def _new_game(self) -> None:
        '''create an empty new game with 12 rows and 6 columns'''
        self._state.empty_new_game(self._row, self._col)

    def _new_faller_or_not(self):
        '''determines the time that a new faller is needed'''
        for row in self._state.current_state():
            for content in row:
                if content.startswith('[') or content.startswith('|'):
                    self._whether_new_faller = False
                    break
                else:
                    self._whether_new_faller = True
            if self._whether_new_faller == False:
                break


    def _rand_faller_command(self) -> str:
        '''generates a string of faller command with random column num and colors'''
        faller_col = random.randint(1,self._col)
        faller_color_list = random.sample('ABCDEFGHIJ', 3)
        faller_color = ''
        for color in faller_color_list:
            faller_color = faller_color + color + ' '
        faller_command = 'F ' + str(faller_col) + ' ' + faller_color
        return faller_command
    
    def _handle_events(self, faller: columns_mechanics.Faller) -> None:
        '''handle all the events including key presses'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()
            elif event.type == pygame.VIDEORESIZE:
                self._resize_surface(event.size)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self._move_left(faller)
                elif event.key == pygame.K_RIGHT:
                    self._move_right(faller)
                elif event.key == pygame.K_SPACE:
                    self._rotate(faller)
                    

    def _move_right(self, faller: columns_mechanics.Faller) -> None:
        '''moves the faller to the right'''
        self._state.move_right(faller)

    def _move_left(self, faller: columns_mechanics.Faller) -> None:
        '''moves the faller to the left'''
        self._state.move_left(faller)

    def _rotate(self, faller: columns_mechanics.Faller) -> None:
        '''rotate the faller'''
        self._state.rotate(faller)


    def _redraw(self) -> None:
        '''draw the surface'''
        surface = pygame.display.get_surface()
        surface.fill(pygame.Color(255, 255, 255))
        self._draw_gameboard(surface)
        pygame.display.flip()

    

    def _columns_color(self, color_letter: str) -> pygame.Color:
        '''give each letter representing color a color in pygame'''
        if color_letter == 'A':
            return pygame.Color(255,0,0)
        if color_letter == 'B':
            return pygame.Color(255,0,238)
        if color_letter == 'C':
            return pygame.Color(255,0,255)
        if color_letter == 'D':
            return pygame.Color(63,4,181)
        if color_letter == 'E':
            return pygame.Color(0,0,255)
        if color_letter == 'F':
            return pygame.Color(0,170,255)
        if color_letter == 'G':
            return pygame.Color(0,255,195)
        if color_letter == 'H':
            return pygame.Color(0,255,0)
        if color_letter == 'I':
            return pygame.Color(255,225,0)
        if color_letter == 'J':
            return pygame.Color(227,152,23)

    def _draw_gameboard(self, surface: pygame.Surface) -> None:
        '''draw the gameboard on the surface'''

        topleft_pixel_x = 0
        topleft_pixel_y = 0

        surface = pygame.display.get_surface()
        width = surface.get_width()
        height = surface.get_height()
        
        column_width = width/self._col
        column_height = height/self._row

        for row in self._state.current_state():
            for content in row:
                if content == '   ':
                    pygame.draw.rect(
                        surface, pygame.Color(255, 255, 255),
                        pygame.Rect(
                            topleft_pixel_x, topleft_pixel_y,
                            column_width, column_height))
                    topleft_pixel_x += column_width
                elif content.startswith('[') or content.startswith('|'):
                    pygame.draw.ellipse(
                        surface, self._columns_color(content[1]),
                        pygame.Rect(
                            topleft_pixel_x, topleft_pixel_y,
                            column_width, column_height))
                    topleft_pixel_x += column_width
                else:
                    pygame.draw.rect(
                        surface, self._columns_color(content[1]),
                        pygame.Rect(
                            topleft_pixel_x, topleft_pixel_y,
                            column_width, column_height))
                    topleft_pixel_x += column_width
                    
            topleft_pixel_y += column_height
            topleft_pixel_x = 0


    def _end_game(self) -> None:
        '''ends the game by setting running to false'''
        self._running = False        


    def _resize_surface(self, size: (int, int)) -> None:
        '''makes the user able to change the size of the display'''
        pygame.display.set_mode(size, pygame.RESIZABLE)

if __name__ == '__main__':
    ColumnsGame().run()
