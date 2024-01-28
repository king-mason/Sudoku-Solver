import numpy
import uuid


class Cell:
    def __init__(self, row, col, value=0, given=False, correct=False, candidates=None):
        self.row = row
        self.col = col
        self.value = value
        self.given = given
        self.correct = correct
        self._id = uuid.uuid4()
        if candidates:
            self.candidates = candidates
        else:
            self.candidates = {i + 1 for i in range(9)}

    def __str__(self):
        return f'{self.value}'

    def __repr__(self):
        return f'Cell({self.value})'

    def __eq__(self, other):
        if type(other) is int or type(other) is float:
            return self.value == other
        return self.value == other.value

    def __hash__(self):
        return int(self._id)

    def copy(self):
        return Cell(self.row, self.col, self.value, self.given, self.correct, self.candidates.copy())


class Grid:
    """9x9 Sudoku Grid"""
    def __init__(self, code=None):
        self.board = numpy.array([[Cell(i, j) for j in range(9)] for i in range(9)])
        if code:
            self.import_code(code)

    @property
    def cells(self):
        return {cell for row in self.board for cell in row}

    def copy(self):
        grid_copy = Grid()
        for i in range(9):
            for j in range(9):
                grid_copy.board[i, j] = self.board[i, j].copy()
        return grid_copy

    def fill(self, cell, value):
        self.board[cell.row, cell.col] = cell
        cell.value = value
        cell.correct = True
        for other_cell in self.scan(cell):
            if value in other_cell.candidates:
                other_cell.candidates.remove(value)

    def print_board(self):
        for i in range(9 + 9 // 3 + 1):
            print('—', end=' ')
        print()
        for row in range(9):
            if row > 0 and row % 3 == 0:
                print('|', end=' ')
                for i in range(9 + 9 // 3 - 1):
                    print('—', end=' ')
                print('|')
            for col in range(9):
                if col % 3 == 0:
                    print('|', end=' ')
                print(self.board[row, col], end=' ')

            print('|')
        for i in range(9 + 9 // 3 + 1):
            print('—', end=' ')
        print()

    def check_valid_cell(self, cell):
        for other_cell in self.scan(cell):
            if cell != 0 and cell == other_cell:
                return False
        return True

    def check_valid(self):
        for i in range(9):
            for j in range(9):
                if not self.check_valid_cell(self.board[i, j]):
                    return False
        return True

    def check_solved(self):
        for i in range(9):
            for j in range(9):
                cell = self.board[i, j]
                if cell == 0 or not self.check_valid_cell(cell):
                    return False
        return True

    def import_code(self, code):
        if len(code) != 81:
            raise (ValueError('Invalid import code'))
        code = code.replace('.', '0')
        for i in range(len(code)):
            given = False if int(code[i]) == 0 else True
            self.board[i // 9, i % 9] = Cell(i // 9, i % 9, int(code[i]), given=given, correct=given)

    def get_code(self):
        code = ''
        for i in range(9):
            for j in range(9):
                code += str(self.board[i, j].value)
        return code

    def test_code(self, code):
        if len(code) != 81:
            raise (ValueError('Invalid test code'))
        code = code.replace('.', '0')
        for i in range(len(code)):
            if self.board[i // 9, i % 9] != int(code[i]):
                return False
        return True

    def scan_row(self, cell):
        return {self.board[cell.row, i] for i in range(9) if i != cell.col}

    def scan_col(self, cell):
        return {self.board[i, cell.col] for i in range(9) if i != cell.row}

    def scan_subgrid(self, cell):
        subgrid = set()
        for i in range((cell.row // 3) * 3, (cell.row // 3) * 3 + 3):
            for j in range((cell.col // 3) * 3, (cell.col // 3) * 3 + 3):
                if i == cell.row and j == cell.col:
                    continue
                subgrid.add(self.board[i, j])
        return subgrid

    def scan(self, cell):
        visible_cells = set()

        # check row
        visible_cells = visible_cells.union(self.scan_row(cell))

        # check column
        visible_cells = visible_cells.union(self.scan_col(cell))

        # check subgrid
        visible_cells = visible_cells.union(self.scan_subgrid(cell))

        return visible_cells

    def fix_candidates(self):
        """Corrects all the options for each cell to fit the current board"""
        for i in range(9):
            for j in range(9):
                cell = self.board[i, j]
                if cell.correct:
                    cell.candidates = {cell.value}

                # remove value from visible cell options
                for other_cell in self.scan(cell):
                    if other_cell.value in cell.candidates:
                        cell.candidates.remove(other_cell.value)

    def count_differences(self, other):
        counter = 0
        for i in range(9):
            for j in range(9):
                if self.board[i, j] != other.board[i, j]:
                    counter += 1
        return counter


if __name__ == '__main__':
    grid = Grid()
    grid.board[1, 0].value = 1

    grid.print_board()
    # grid.import_code('004300209005009001070060043006002087190007400050083000600000105003508690042910300')
    grid.print_board()
    grid.fix_candidates()
    print(grid.check_valid())
    print(grid.check_solved())
    # print(len(grid.scan(grid.board[0, 0])))
    # print(grid.get_code())
