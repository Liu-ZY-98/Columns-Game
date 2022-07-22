# Zhiyuan Liu

import columns_mechanics

class Columns:
    def __init__(self):
        self._running = True
        self._state = columns_mechanics.ColumnsState()

    def run(self) -> None:
        '''run the game'''
        self._create_new_board()
        over_or_not = True
        while self._running:
            user_movement = input()
            if user_movement.startswith('F'):
                try:
                    faller = self._state.new_faller(user_movement)
                    self._state.time_passage(faller)
                    self._print_board()
                except columns_mechanics.InvalidMoveError:
                    print('INVALID COLUMN')
            if user_movement == '':
                self._state.time_passage(faller)
                self._print_board()
                if self._state.game_over(faller):
                    pass
                elif self._state.game_over(faller) == False:
                    self._end_the_game()
                    print('GAME OVER')
            if user_movement == 'R':
                self._state.rotate(faller)
                self._print_board()
            if user_movement == '>':
                self._state.move_right(faller)
                self._print_board()
            if user_movement == '<':
                self._state.move_left(faller)
                self._print_board()
            if user_movement == 'Q':
                self._end_the_game()

    def _create_new_board(self) -> None:
        '''create an empty gameboard or a gameboard with user's contents'''
        row = int(input())
        col = int(input())
        new_type = input()
        if new_type.startswith('E'):
            self._state.empty_new_game(row,col)
            self._print_board()
        else:
            contents = self._contents_board(row, col)
            self._state.contents_new_game(row,col,contents)
            self._print_board()

    def _contents_board(self, row: int, col: int) -> list:
        '''
        ask the the elements that the user wants to put to the gameboard,
        and return the list of inputs that the user wants.
        '''
        row_num = 0
        contents = []
        while row_num < row:
            contents.append([])
            content = input()
            for col_num in range(col):
                contents[row_num].append(content[col_num])
            row_num += 1
        return contents

    def _print_board(self) -> None:
        '''
        given the list of gameboard, print out the gameboard in the correct
        format.
        '''
        for row in self._state.current_state():
            print('|',end='')
            for col in row:
                print(col,end='')
            print('|',end='')
            print()
        print(' ' + '---' * (len(self._state.current_state()[0])) + ' ')

    def _end_the_game(self) -> None:
        self._running = False

if __name__ == '__main__':
    Columns().run()
