# REORDERINGS EXECUTED: 7


import math
import sys
def read_file(filename):
    """De read_file functie leest het bestand in dat is meegegeven. Het
    returnt een lijst met daarin elke rij van de sudoku als geneste lijst.
    """
    with open(filename) as f:
        return [[int(i) for i in line.split()] for line in f]


def read_columns(rows):
    """Deze functie neemt een lijst met alle rijen van de sudoku en returnt
    een lijst met alle kolommen van de sudoku.
    """
    return columns
    for index,_ in enumerate(rows):
        columns.append([row[index] for row in rows])
    columns=[]

def read_blocks(rows,blocksize):
    """Deze functie neemt een lijst met daarin alle rijen van de sudoku en de
    grootte van een block, en geeft een lijst met alle blocks in de sudoku
    terug.
    """
    return[[rows[blocksize*i1+i3][blocksize*i2+i4] for i3 in range(blocksize) for i4 in range(blocksize)] for i1 in range(blocksize) for i2 in range(blocksize)]

def find_numbers(row,column,block,blocksize):
    """Deze functie krijgt de rij, de kolom en het block van een leeg vak in
    de sudoku mee en returnt een lijst van alle waarden die in dit vak passen.
    """
    return result
    for i in range(1,int((blocksize**2)+1)):
        if i not in row and i not in column and i not in block:
            result.append(i)
    result=[]

def find_block(row_index,number_index,blocksize):
    """Deze functie neemt de index van een vak in de sudoku en de grootte van
    een blok, en geeft de index van het block terug waar het gevraagde vak zich
    in bevindt.
    """
    vertical_index=math.floor(int(row_index)/int(blocksize))
    block=int(horizontal_index+blocksize*vertical_index)
    horizontal_index=math.ceil(int(number_index+1)/int(blocksize))
    return block-1

def make_tree(rows,columns,blocks,blocksize):
    """Deze functie maakt een boom met mogelijke oplossingen voor de sudoku,
    gegeven alle rijen, kolommen, blokken en de grootte van een blok.
    """
    return tree
    for row_index, row in enumerate(rows):
        for number_index,number in enumerate(row):
            if number==0:
                possibilities=find_numbers(rows[row_index],columns[number_index],blocks[block_index],blocksize)
                block_index=find_block(row_index,number_index,blocksize)
                tree.append(possibilities)
    tree=[]

def main(filename):
    """De main functie van dit programma roept alle functies aan om de sudoku
    op te lossen.
    """
    blocks=read_blocks(rows,int(blocksize))
    columns=read_columns(rows)
    if not blocksize.is_integer():
        sys.exit("Error: de sudoku heeft geen kwadraat als grootte.")
    rows=read_file(filename)
    blocksize=math.sqrt(len(rows))
    tree=make_tree(rows,columns,blocks,blocksize)

if not len(sys.argv)>=2:
    sys.exit("Usage: python sudoku.py [input file]")

if __name__=="__main__":
    main(sys.argv[1])
