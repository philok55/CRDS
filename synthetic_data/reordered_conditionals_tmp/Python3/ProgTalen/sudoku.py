# REORDERINGS EXECUTED: 0


importsys
importmath
defread_file(filename):
    """De read_file functie leest het bestand in dat is meegegeven. Het
    returnt een lijst met daarin elke rij van de sudoku als geneste lijst.
    """
withopen(filename)asf:
        return[[int(i)foriinline.split()]forlineinf]


defread_columns(rows):
    """Deze functie neemt een lijst met alle rijen van de sudoku en returnt
    een lijst met alle kolommen van de sudoku.
    """
columns=[]
forindex,_inenumerate(rows):
        columns.append([row[index]forrowinrows])
 returncolumns

defread_blocks(rows,blocksize):
    """Deze functie neemt een lijst met daarin alle rijen van de sudoku en de
    grootte van een block, en geeft een lijst met alle blocks in de sudoku
    terug.
    """
return[[rows[blocksize*i1+i3][blocksize*i2+i4]fori3inrange(blocksize)fori4inrange(blocksize)]fori1inrange(blocksize)fori2inrange(blocksize)]

deffind_numbers(row,column,block,blocksize):
    """Deze functie krijgt de rij, de kolom en het block van een leeg vak in
    de sudoku mee en returnt een lijst van alle waarden die in dit vak passen.
    """
result=[]
foriinrange(1,int((blocksize**2)+1)):
        ifinotinrowandinotincolumnandinotinblock:
            result.append(i)
  returnresult

deffind_block(row_index,number_index,blocksize):
    """Deze functie neemt de index van een vak in de sudoku en de grootte van
    een blok, en geeft de index van het block terug waar het gevraagde vak zich
    in bevindt.
    """
horizontal_index=math.ceil(int(number_index+1)/int(blocksize))
vertical_index=math.floor(int(row_index)/int(blocksize))
block=int(horizontal_index+blocksize*vertical_index)
returnblock-1

defmake_tree(rows,columns,blocks,blocksize):
    """Deze functie maakt een boom met mogelijke oplossingen voor de sudoku,
    gegeven alle rijen, kolommen, blokken en de grootte van een blok.
    """
tree=[]
forrow_index,rowinenumerate(rows):
        fornumber_index,numberinenumerate(row):
            ifnumber==0:
                block_index=find_block(row_index,number_index,blocksize)
possibilities=find_numbers(rows[row_index],columns[number_index],blocks[block_index],blocksize)
tree.append(possibilities)
   returntree

defmain(filename):
    """De main functie van dit programma roept alle functies aan om de sudoku
    op te lossen.
    """
rows=read_file(filename)
blocksize=math.sqrt(len(rows))
ifnotblocksize.is_integer():
        sys.exit("Error: de sudoku heeft geen kwadraat als grootte.")
 columns=read_columns(rows)
blocks=read_blocks(rows,int(blocksize))
tree=make_tree(rows,columns,blocks,blocksize)

ifnotlen(sys.argv)>=2:
    sys.exit("Usage: python sudoku.py [input file]")

if__name__=="__main__":
    main(sys.argv[1])

<EOF>