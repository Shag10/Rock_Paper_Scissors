class Game:
    def __init__(self,id):
        self.p1move=False
        self.p2move=False
        self.ready=False
        self.id=id
        self.moves=[None,None]
        self.wins=[0,0]
        self.ties=0

    def player_move(self,p):
        return self.moves[p]

    def play(self,player,move):
        self.moves[player]=move
        if player==0:
            self.p1move=True
        else:
            self.p2move=True

    def connect(self):
        return self.ready

    def bothmove(self):
        return self.p1move and self.p2move

    def win(self):
        p1=self.moves[0].upper()[0]
        p2=self.moves[1].upper()[0]

        winner=-1
        if p1=="R" and p2=="S":
            winner=0
        elif p1=="S" and p2=="R":
            winner=1
        elif p1=="P" and p2=="R":
            winner=0
        elif p1=="R" and p2=="P":
            winner=1
        elif p1=="S" and p2=="P":
            winner=0
        elif p1=="P" and p2=="S":
            winner=1
            
        return winner

    def reset(self):
        self.p1move=False
        self.p2move=False
