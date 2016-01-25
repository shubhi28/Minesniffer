import sys
from itertools import combinations

class Minesniffer():
    def __init__(self,filename):
        self.filename = filename
        fin = open(filename,'r')
        arr = fin.readline().strip().split(' ')
        self.n = int(arr[0])
        self.m = int(arr[1].strip(' '))
        self.num_mines = 0
        rawState = [[0 for x in range(self.m)] for x in range(self.n)]
        for i in range(self.n):
            rawState[i] = fin.readline().strip().split(',')

    # updating game state with all 0
        Board = [[0 for x in range(self.m)] for x in range(self.n)]

    # update board positions
        for i in range(self.n):
            for j in range(self.m):
                if rawState[i][j] == 'X':
                    self.num_mines +=1
                    Board[i][j] = -self.num_mines
                else:
                    Board[i][j] = int(rawState[i][j])

        fin.close()
        self.board = Board

    def neighbours(self, pos):
        m = self.m
        n = self.n
        neighbours = []
        surrounding = ((-1,-1),(-1,-0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        x = pos[0]
        y = pos[1]
        for (dx,dy) in surrounding:
            nx = x+dx
            ny = y+dy
            if 0 <= nx < n and 0 <=ny < m:
                neighbours.append((nx,ny))
        return neighbours

    def neighbours_mines(self,pos):
        num_mines = self.neighbours(pos)
        n_mines=[]
        for i in num_mines:
            if self.board[i[0]][i[1]] < 0:
                n_mines.append(self.board[i[0]][i[1]])
        return n_mines

    def get_cells(self):
        cells = []
        for i in range(self.n):
            for j in range(self.m):
                if self.board[i][j]>=0:
                    cells.append((i,j))
        return cells

def parse_file(filename):
    MinesnifferObject = Minesniffer(filename)
    return (MinesnifferObject)

def convert2CNF(board, output):
    # interpret the number constraints
    fout = open(output, 'w')
    fout.write("c Here is a comment \n")
    fx =[]
    cells = board.get_cells()
    for pos in cells:
        abs_n_mines = []
        k = board.board[pos[0]][pos[1]]
        n_mines = board.neighbours_mines(pos)
        for i in n_mines:
            abs_n_mines.append(abs(i))
        n= len(n_mines)
        x = combinations(n_mines,k+1)
        y = combinations(abs_n_mines,(n-k+1))
        for mines in x:
            if mines not in fx:
                fx.append(mines)
        for mines in y:
            if mines not in fx:
                fx.append(mines)
    l = len(fx)
    fout.write("p cnf "+str(board.num_mines)+" "+str(l)+"\n")
    for com in fx:
        for i in com:
            fout.write(str(i)+" ")
        fout.write("0\n")
    fout.close()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Layout or output file not specified.'
        exit(-1)
    board = parse_file(sys.argv[1])

    convert2CNF(board, sys.argv[2])