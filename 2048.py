import random

class Check:
    def __init__(self):
        self.value = 0

class Game:
    START = 1
    OVER = 2
    WIN = 3
    def __init__(self):
        self.matrix = []
        self.changes = False
        self.state = Game.START
        self.score = 0
        self.oder = {'w': "self.matrix[j][i]", 's': "self.matrix[3 - j][i]",
                     'd': "self.matrix[i][3 - j]", 'a': "self.matrix[i][j]"}
    def start(self):
        self.init_matrix()
        self.random()
        while self.state is Game.START:
            print("操作: (W)上 (S)下 (A)左 (D)右")
            print('***** 2048 *****')
            self.show()
            print('***** Game *****')
            print('分数: ', self.score)
            key = input('输入: ')
            self.do(self.oder[key.lower()])
            if self.changes:
                self.random()
    def show(self):
        print('-----------------')
        for row in self.matrix:
            line = []
            for item in row:
                if item.value is 0:
                    line.append('')
                else:
                    line.append(str(item.value))
            print('| {}\t| {}\t| {}\t| {}\t|\n-----------------'.format(line[0], line[1], line[2], line[3]))
    def init_matrix(self):
        self.matrix = []
        for i in range(4):
            self.matrix.append([])
            for j in range(4):
                self.matrix[i].append(Check())
    def random(self):
        zero = []
        for i in range(4):
            for j in range(4):
                if self.matrix[i][j].value is 0:
                    zero.append(self.matrix[i][j])
        if len(zero):
            slot = random.randint(0, len(zero) - 1)
            zero[slot].value = 2
        else:
            self.state = Game.OVER
    def do(self, code):
        self.changes = False
        for i in range(4):
            row = []
            for j in range(4):
                row.append(eval(code))
            self.overlay(row)
    def overlay(self, row):
        for index in range(4):
            next_index = index + 1
            while next_index < 4:
                if row[next_index].value is 0:
                    next_index += 1
                elif row[index].value is 0:
                    row[index].value = row[next_index].value
                    row[next_index].value = 0
                    self.changes = True
                elif row[index].value is row[next_index].value:
                    self.score += row[index].value
                    row[index].value *= 2
                    row[next_index].value = 0
                    self.changes = True
                else:
                    next_index += 1

game = Game()
game.start()