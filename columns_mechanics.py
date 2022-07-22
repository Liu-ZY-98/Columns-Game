# Zhiyuan Liu

class InvalidMoveError(Exception):
    '''Raised whenever an invalid move is made'''
    pass

class Faller:
    def __init__(self,fall_command: str):
        self._column = int(fall_command[2])
        self._first = fall_command[4]
        self._second = fall_command[6]
        self._last = fall_command[8]
        self._f_pos = -3
        self._s_pos = -2
        self._l_pos = -1

    def first_pos(self) -> int:
        '''get the first position'''
        return self._f_pos

    def second_pos(self) -> int:
        '''get the second position'''
        return self._s_pos

    def last_pos(self) -> int:
        '''get the position of the lowest one in a faller'''
        return self._l_pos

    def rotate(self) -> [str]:
        '''make the faller's letter change when the user wants it to rotate'''
        first = self._last
        second = self._first
        last = self._second
        self._first = first
        self._second = second
        self._last = last
        return [self._first, self._second, self._last]

    def left(self) -> int:
        '''change the column num of the faller to one less'''
        self._column -= 1
        return self._column

    def right(self) -> int:
        '''add one to the faller's column num'''
        self._column += 1
        return self._column

    def column(self) -> int:
        '''return the column num of the faller'''
        return self._column

    def last_pos(self) -> int:
        '''return the lowest element's position in a faller'''
        return self._l_pos

    def change_last_pos(self) -> int:
        '''add one to the faller's lowest element's position'''
        self._l_pos += 1
        return self._l_pos

    def change_second_pos(self) -> int:
        '''add one to the second position of a faller'''
        self._s_pos += 1
        return self._s_pos

    def change_first_pos(self) -> int:
        '''add one to the first position of a faller'''
        self._f_pos += 1
        return self._f_pos

    def first(self) -> str:
        '''return the first element in a faller'''
        return self._first

    def second(self) -> str:
        '''return the faller's second element'''
        return self._second

    def last(self) -> str:
        '''return the faller's lowest element'''
        return self._last

    


    
class ColumnsState:
    def __init__(self):
        self._columns = []

    def current_state(self) -> list:
        '''return the current state of the gameboard'''
        return self._columns


    def empty_new_game(self, rows: int, columns: int) -> None:
        '''make a list of gameboard with no user's inputs'''
        for row in range(rows):
            self._columns.append([])
            for col in range(columns):
                self._columns[-1].append('   ')


    def contents_new_game(self, rows: int, columns: int, contents: list) -> None:
        '''return a list of gameboard that has the elements that the user wants'''
        self._columns = self.empty_new_game(rows, columns)
        for row in range(rows):
            for col in range(columns):
                self._columns[row][col] = ' ' + contents[row][col] + ' '


    def new_faller(self, fall_command: str) -> Faller:
        '''create a new faller givin the user's command'''
        if int(fall_command[2]) > len(self._columns[0]) or int(fall_command[2]) < 1:
            raise InvalidMoveError()
        else:
            return Faller(fall_command)


    def time_passage(self, faller: Faller) -> None:
        '''make change to the list of gameboard as the time passes'''
        if faller:
            self._handle_faller_down(faller)



    def rotate(self, faller: Faller) -> None:
        '''make change to the list of gameboard as the faller in the list rotates'''
        if self._columns[faller.last_pos()][faller.column()-1][0] == '[':
            list_of_color = faller.rotate()
            first = list_of_color[0]
            second = list_of_color[1]
            last = list_of_color[2]
            if faller.last_pos() >= 0:
                self._columns[faller.last_pos()][faller.column()-1] = '[' + last + ']'
            if faller.second_pos() >= 0:
                self._columns[faller.second_pos()][faller.column()-1] = '[' + second + ']'
            if faller.first_pos() == 0:
                self._columns[faller.first_pos()][faller.column()-1] = '[' + first + ']'
            if faller.first_pos() > 0:
                self._columns[faller.first_pos()][faller.column()-1] = '[' + first + ']'
                self._columns[faller.first_pos()-1][faller.column()-1] = '   '


    def move_right(self, faller: Faller) -> None:
        '''change the gameboard as the faller moves to the right'''
        f_move = False
        s_move = False
        l_move = False
        if faller.last_pos() >= 0 and faller.column() < (len(self._columns[0])):
            if self._columns[faller.last_pos()][faller.column()] == '   ':
                l_move = True
                if faller.second_pos() < 0:
                    s_move = l_move
                if faller.first_pos() < 0:
                    f_move = l_move
        if faller.second_pos() >= 0 and faller.column() < (len(self._columns[0])):
            if self._columns[faller.second_pos()][faller.column()] == '   ':
                s_move = True
        if faller.first_pos() >= 0 and faller.column() < (len(self._columns[0])):
            if self._columns[faller.first_pos()][faller.column()] == '   ':
                f_move = True
        if l_move and s_move and f_move and self._columns[faller.last_pos()][
            faller.column()-1].startswith('['):
            column = faller.right()
            if faller.last_pos() >= 0:
                self._columns[faller.last_pos()][column-1] = '[' + faller.last() + ']'
                self._columns[faller.last_pos()][column-2] = '   '
            if faller.second_pos() >= 0:
                self._columns[faller.second_pos()][column-1] = '[' + faller.second() + ']'
                self._columns[faller.second_pos()][column-2] = '   '
            if faller.first_pos() == 0:
                self._columns[faller.first_pos()][column-1] = '[' + faller.first() + ']'
                self._columns[faller.first_pos()][column-2] = '   '
            if faller.first_pos() > 0:
                self._columns[faller.first_pos()][column-1] = '[' + faller.first() + ']'
                self._columns[faller.first_pos()-1][column-1] = '   '
                self._columns[faller.first_pos()][column-2] = '   '


    def move_left(self, faller: Faller) -> None:
        '''change the gameboard as the faller moves to the left'''
        f_move = False
        s_move = False
        l_move = False
        if faller.last_pos() >= 0 and faller.column() > 1:
            if self._columns[faller.last_pos()][faller.column()-2] == '   ':
                l_move = True
                if faller.second_pos() < 0:
                    s_move = l_move
                if faller.first_pos() < 0:
                    f_move = l_move
        if faller.second_pos() >= 0 and faller.column() > 1:
            if self._columns[faller.second_pos()][faller.column()-2] == '   ':
                s_move = True
        if faller.first_pos() >= 0 and faller.column() > 1:
            if self._columns[faller.first_pos()][faller.column()-2] == '   ':
                f_move = True
        if l_move and s_move and f_move and self._columns[faller.last_pos()][
            faller.column()-1].startswith('['):
            column = faller.left()
            if faller.last_pos() >= 0:
                self._columns[faller.last_pos()][column-1] = '[' + faller.last() + ']'
                self._columns[faller.last_pos()][column] = '   '
            if faller.second_pos() >= 0:
                self._columns[faller.second_pos()][column-1] = '[' + faller.second() + ']'
                self._columns[faller.second_pos()][column] = '   '
            if faller.first_pos() == 0:
                self._columns[faller.first_pos()][column-1] = '[' + faller.first() + ']'
                self._columns[faller.first_pos()][column] = '   '
            if faller.first_pos() > 0:
                self._columns[faller.first_pos()][column-1] = '[' + faller.first() + ']'
                self._columns[faller.first_pos()-1][column-1] = '   '
                self._columns[faller.first_pos()][column] = '   '
        

    def _handle_faller_down(self, faller: Faller) -> None:
        '''
        This method will handle everything that could happen to the gameboard
        when the user wants the time to pass.
        '''
        faller_col = faller.column()
        faller_last = faller.last()
        faller_second = faller.second()
        faller_first = faller.first()
        next_in_col = faller.last_pos() + 1
                       
        if (next_in_col == len(self._columns) or self._columns[
            next_in_col][faller_col - 1] != '   ') and self._columns[faller.last_pos()][
                faller_col-1].startswith('['):

            if faller.last_pos() >= 0:
                self._columns[faller.last_pos()][faller_col-1] = '|' + faller_last + '|'
            if faller.second_pos() >= 0:
                self._columns[faller.second_pos()][faller_col-1] = '|' + faller_second + '|'
            if faller.first_pos() >= 0:
                self._columns[faller.first_pos()][faller_col-1] = '|' + faller_first + '|'

        elif (next_in_col != len(self._columns)) and self._columns[next_in_col][faller_col - 1] == '   ':
            faller_last_pos = faller.change_last_pos()
            faller_second_pos = faller.change_second_pos()
            faller_first_pos = faller.change_first_pos()
            if faller_last_pos >= 0:
                self._columns[faller_last_pos][faller_col-1] = '[' + faller_last + ']'
            if faller_second_pos >= 0:
                self._columns[faller_second_pos][faller_col-1] = '[' + faller_second + ']'
            if faller_first_pos == 0:
                self._columns[faller_first_pos][faller_col-1] = '[' + faller_first + ']'
            if faller_first_pos > 0:
                self._columns[faller_first_pos][faller_col-1] = '[' + faller_first + ']'
                self._columns[faller_first_pos-1][faller_col-1] = '   '

        else:
            for row in range(len(self._columns)):
                for col in range(len(self._columns[0])):
                    if self._columns[row][col].startswith('|'):
                        self._columns[row][col] = ' ' + self._columns[row][col][1] + ' '
    

    
    def game_over(self, faller: Faller) -> bool:
        '''This method will check whether the game is over or not'''
        over = True
        if self._columns[faller.last_pos()][faller.column()-1].startswith('|'):
            if faller.first_pos() < 0 or faller.second_pos() < 0:
                over = False
        return over
