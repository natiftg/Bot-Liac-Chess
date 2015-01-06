import time
import sys
import random

from base_client import LiacBot

WHITE = 1
BLACK = -1
NONE = 0

# BOT =========================================================================
class MyBot(LiacBot):
    name = "Natalia's Bot"

    def __init__(self):
        super(MyBot, self).__init__()
        self.last_move = None

    def on_move(self, state):
        board = Board(state)

        if state['bad_move']:
            print state['board']
            raw_input()
        
        moveList = []
        for p in board.AllPieces:
            if p.team == board.BotTeam:
                for moveAux in p.possibleMoves:
                    if p.possibleMoves:
                        moveList.append([p.position, moveAux])

        del board
        
        
        # EVALUATE each possible move and it's possible responses
        #for move in moveList: 
        move = random.choice(moveList)
        del moveList[:]
        
        i = 0
        while move[0] < 2**63:
            move[0] = move[0] << 1
            i += 1
        ArgFrom = (i//8, i%8)
        print 'From: ', ArgFrom
           
        i = 0
        while move[1] < 2**63:
            move[1] = move[1] << 1
            i += 1
        ArgTo = (i//8, i%8)
        print 'To:   ', ArgTo
    
        print 'Move translated'
        self.last_move = [ArgFrom, ArgTo]
        self.send_move(ArgFrom, ArgTo)
        print 'Move sent'

        

    def on_game_over(self, state):
        print 'Game Over.'
        # sys.exit()
# =============================================================================

# MODELS ======================================================================
class Board(object):
    def __init__(self, state):
        self.AllPieces = []
        self.Pawns = []
        self.Rooks = []
        self.Bishops = []
        self.Queens = []
        self.Knights = []
        self.OccupiedCells = {}
        self.EmptyCells  = 0
        self.Value = 0
        self.BotTeam = None

        self.getBotTeam(state)
    
    

        self.getIndividualPositions(state)
            
        self.AllPieces.extend(self.Pawns)
        self.AllPieces.extend(self.Rooks)
        self.AllPieces.extend(self.Bishops)
        self.AllPieces.extend(self.Queens)
        self.AllPieces.extend(self.Knights)

        self.OccupiedCells['white'] = 0
        self.OccupiedCells['black'] = 0
        
        for p in self.AllPieces:
            if p.team == 'white':
                self.OccupiedCells['white'] += p.position
            elif p.team == 'black':
                self.OccupiedCells['black'] += p.position

        self.EmptyCells = ~( self.OccupiedCells['white'] | self.OccupiedCells['black'] )

        for p in self.AllPieces:
            p.generatePossibleMoves(self)

        self.getBoardValue()


    def getBotTeam(self, state):
        if state['who_moves'] == WHITE:
            self.BotTeam = 'white'
        elif state['who_moves'] == BLACK:
            self.BotTeam = 'black'
            

    def getBoardValue(self):
        for p in self.AllPieces:
            if p.team == self.BotTeam:
                self.Value += p.value
            else:
                self.Value -= p.value
                
    def getIndividualPositions(self, state):
        i = 0
        j = 0
        k = 0
        l = 0
        m = 0
        n = 0
        bitboardBase = 0b1000000000000000000000000000000000000000000000000000000000000000
        for p in state['board']:
            if p == p.lower():
                team = 'black'
            else:
                team = 'white'
            if p.lower() == 'p':
                self.Pawns.append(Pawn(bitboardBase >> i, team, self))
                j += 1
            elif p.lower() == 'r':
                self.Rooks.append(Rook(bitboardBase >> i, team, self))
                k += 1
            elif p.lower() == 'b':
                self.Bishops.append(Bishop(bitboardBase >> i, team, self))
                l += 1
            elif p.lower() == 'q':
                self.Queens.append(Queen(bitboardBase >> i, team, self))
                m += 1
            elif p.lower() == 'n':
                self.Knights.append(Knight(bitboardBase >> i, team, self))
                n += 1
            i += 1
            
        Pawn.Alive = j
        Rook.Alive = k
        Bishop.Alive = l
        Queen.Alive = m
        Knight.Alive = n

        


class Piece(object):
    def __init__(self):
        self.position = None
        self.team = None
        self.possibleMoves = []
        self.value = None
        self.char = None
        

class Pawn(Piece):
    Alive = None
    def __init__(self, p, t, board):
        self.position = p
        self.team = t
        if self.team == 'black':
            self.char = 'p'
            i = 0
            aux = self.position
            while aux < 2**64:
                aux = aux << 8
                i += 1
            self.value = i*i
        elif self.team == 'white':
            self.char = 'P'
            i = 0
            aux = self.position
            while aux > 0:
                aux = aux >> 8
                i += 1
            self.value = i*i      
        
    def generatePossibleMoves(self, board):
        SecondRow  = 0b0000000010000000000000000000000000000000000000000000000000000000
        ThirdRow  = 0b0000000000000000100000000000000000000000000000000000000000000000

        SeventhRow  = 0b0000000000000000000000000000000000000000000000001000000000000000
        EighthRow  = 0b0000000000000000000000000000000000000000000000000000000010000000

        moves = []

        '''if self.team == 'black' and ((self.position >> 8) & board.OccupiedCells['white']) == 0:
            moves.append(self.position >> 8)
            if (self.position >= SecondRow) and (self.position > ThirdRow) and ((self.position >> 16) & board.OccupiedCells['white']) == 0:
                moves.append(self.position >> 16)
        elif self.team == 'white' and ((self.position << 8) & board.OccupiedCells['black']) == 0:
            moves.append(self.position << 8)
            if (self.position >= SeventhRow) and (self.position < EighthRow) and ((self.position << 16) & board.OccupiedCells['black']) == 0:
                moves.append(self.position << 16)'''
                
        self.possibleMoves = moves
   

class Rook(Piece):
    Alive = None
    def __init__(self, p, t, board):
        self.position = p
        self.team = t
        if self.team == 'black':
            self.char = 'r'
        elif self.team == 'white':
            self.char = 'R'
        self.value = 10
        

    def generatePossibleMoves(self, board):
        FirstColumn = 0b1000000010000000100000001000000010000000100000001000000010000000
        EighthColumn = 0b0000000100000001000000010000000100000001000000010000000100000001  
        moves = []
        previousMove = self.position
        # while the move doesn't overlap other pieces from the same team and doesn't leave the board
        while (((previousMove >> 8) & board.OccupiedCells[self.team]) == 0) and ((previousMove >> 8) > 0):
            moves.append(previousMove >> 8)
            previousMove = previousMove >> 8

        previousMove = self.position
        while (((previousMove << 8 ) & board.OccupiedCells[self.team]) == 0) and ((previousMove << 8)%(2**64) != 0):
            moves.append(previousMove << 8)
            previousMove = previousMove << 8

        previousMove = self.position
        while (((previousMove >> 1 ) & board.OccupiedCells[self.team]) == 0) and ((previousMove | EighthColumn) != EighthColumn):
            moves.append(previousMove >> 1)
            previousMove = previousMove >> 1

        previousMove = self.position
        while (((previousMove << 1 ) & board.OccupiedCells[self.team]) == 0) and ((previousMove | FirstColumn) != FirstColumn):
            moves.append(previousMove << 1)
            previousMove = previousMove << 1
            
        self.possibleMoves = moves


class Bishop(Piece):
    Alive = None
    def __init__(self, p, t, board):
        self.position = p
        self.team = t
        if self.team == 'black':
            self.char = 'b'
        elif self.team == 'white':
            self.char = 'B'
        self.value = 12
        

    def generatePossibleMoves(self, board):
        FirstColumn = 0b1000000010000000100000001000000010000000100000001000000010000000
        EighthColumn = 0b0000000100000001000000010000000100000001000000010000000100000001
        moves = []
        previousMove = self.position
        # while the move doesn't overlap other pieces from the same team and doesn't leave the board
        while ((((previousMove >> 8) << 1) & board.OccupiedCells[self.team]) == 0) and ((previousMove >> 8) > 0) and ((previousMove | FirstColumn) != FirstColumn):
            moves.append((previousMove >> 8) << 1)
            previousMove = (previousMove >> 8) << 1

        previousMove = self.position
        while ((((previousMove << 8) >> 1) & board.OccupiedCells[self.team]) == 0) and ((previousMove << 8)%(2**64) != 0) and ((previousMove | EighthColumn) != EighthColumn):
            moves.append((previousMove << 8) >> 1)
            previousMove = (previousMove << 8) >> 1

        previousMove = self.position
        while ((((previousMove >> 1 ) >> 8) & board.OccupiedCells[self.team]) == 0) and ((previousMove >> 8) > 0) and ((previousMove | EighthColumn) != EighthColumn):
            moves.append((previousMove >> 1) >> 8)
            previousMove = (previousMove >> 1) >> 8

        previousMove = self.position
        while ((((previousMove << 1 ) << 8) & board.OccupiedCells[self.team]) == 0) and ((previousMove << 8)%(2**64) != 0) and ((previousMove | FirstColumn) != FirstColumn):
            moves.append((previousMove << 1) << 8)
            previousMove = (previousMove << 1) << 8
      
        self.possibleMoves = moves
        

class Queen(Piece):
    Alive = None
    def __init__(self, p, t, board):
        self.position = p
        self.team = t
        if self.team == 'black':
            self.char = 'q'
        elif self.team == 'white':
            self.char = 'Q'
        self.value = 20
        

    def generatePossibleMoves(self, board):
        FirstColumn = 0b1000000010000000100000001000000010000000100000001000000010000000
        EighthColumn = 0b0000000100000001000000010000000100000001000000010000000100000001
        moves = []
        previousMove = self.position
        # while the move doesn't overlap other pieces from the same team and doesn't leave the board
        while ((((previousMove >> 8) << 1) & board.OccupiedCells[self.team]) == 0) and ((previousMove >> 8) > 0) and ((previousMove | FirstColumn) != FirstColumn):
            moves.append((previousMove >> 8) << 1)
            previousMove = (previousMove >> 8) << 1

        previousMove = self.position
        while ((((previousMove << 8) >> 1) & board.OccupiedCells[self.team]) == 0) and ((previousMove << 8)%(2**64) != 0) and ((previousMove | EighthColumn) != EighthColumn):
            moves.append((previousMove << 8) >> 1)
            previousMove = (previousMove << 8) >> 1

        previousMove = self.position
        while ((((previousMove >> 1 ) >> 8) & board.OccupiedCells[self.team]) == 0) and ((previousMove >> 8) > 0) and ((previousMove | EighthColumn) != EighthColumn):
            moves.append((previousMove >> 1) >> 8)
            previousMove = (previousMove >> 1) >> 8

        previousMove = self.position
        while ((((previousMove << 1 ) << 8) & board.OccupiedCells[self.team]) == 0) and ((previousMove << 8)%(2**64) != 0) and ((previousMove | FirstColumn) != FirstColumn):
            moves.append((previousMove << 1) << 8)
            previousMove = (previousMove << 1) << 8
   
        previousMove = self.position
        while (((previousMove >> 8) & board.OccupiedCells[self.team]) == 0) and ((previousMove >> 8) > 0):
            moves.append(previousMove >> 8)
            previousMove = previousMove >> 8

        previousMove = self.position
        while (((previousMove << 8 ) & board.OccupiedCells[self.team]) == 0) and ((previousMove << 8)%(2**64) != 0):
            moves.append(previousMove << 8)
            previousMove = previousMove << 8

        previousMove = self.position
        while (((previousMove >> 1 ) & board.OccupiedCells[self.team]) == 0) and ((previousMove | EighthColumn) != EighthColumn):
            moves.append(previousMove >> 1)
            previousMove = previousMove >> 1

        previousMove = self.position
        while (((previousMove << 1 ) & board.OccupiedCells[self.team]) == 0) and ((previousMove | FirstColumn) != FirstColumn):
            moves.append(previousMove << 1)
            previousMove = previousMove << 1
        
        self.possibleMoves = moves

class Knight(Piece):
    Alive = None
    def __init__(self, p, t, board):
        self.position = p
        self.team = t
        if self.team == 'black':
            self.char = 'n'
        elif self.team == 'white':
            self.char = 'N'
        self.value = 10
        

    def generatePossibleMoves(self, board):
        '''FirstColumn = 0b1000000010000000100000001000000010000000100000001000000010000000
        SecondColumn = 0b0100000001000000010000000100000001000000010000000100000001000000
        SeventhColumn = 0b0000001000000010000000100000001000000010000000100000001000000010
        EighthColumn = 0b0000000100000001000000010000000100000001000000010000000100000001
        moves = [(self.position >> 16) >> 1,
                 (self.position >> 16) << 1,
                 (self.position << 16) >> 1,
                 (self.position << 16) << 1,
                 (self.position >> 8) >> 2,
                 (self.position >> 8) << 2,
                 (self.position << 8) >> 2,
                 (self.position << 8) << 2]

        if (self.position | FirstColumn) == FirstColumn:
            moves.remove((self.position >> 16) << 1)
            moves.remove((self.position << 16) << 1)
            moves.remove((self.position >> 8) << 2)
            moves.remove((self.position << 8) << 2)
        elif (self.position | SecondColumn) == SecondColumn:
            moves.remove((self.position >> 8) << 2)
            moves.remove((self.position << 8) << 2)
        elif (self.position | SeventhColumn) == SeventhColumn:
            moves.remove((self.position >> 8) >> 2)
            moves.remove((self.position << 8) >> 2)
        elif (self.position | EighthColumn) == EighthColumn:
            moves.remove((self.position >> 16) >> 1)
            moves.remove((self.position << 16) >> 1)
            moves.remove((self.position >> 8) >> 2)
            moves.remove((self.position << 8) >> 2)
                
        for m in moves:
            if (m < 1) or (m > 2**63) or ((m & board.OccupiedCells[self.team]) != 0):
                moves.remove(m)'''
        moves = []

        self.possibleMoves = moves

   
# =============================================================================

if __name__ == '__main__':
    color = 0
    port = 50100

    if len(sys.argv) > 1:
        if sys.argv[1] == 'black':
            color = 1
            port = 50200

    bot = MyBot()
    bot.port = port

    bot.start()

