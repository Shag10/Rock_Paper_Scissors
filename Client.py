import pygame
from network import Network
import pickle
pygame.font.init()

w=700
h=700
win=pygame.display.set_mode((w,h))
pygame.display.set_caption("Client")

bg=pygame.transform.scale(pygame.image.load("download.jpg"),(w,h))
class Button:
    def __init__(self,text,x,y,color):
        self.text=text
        self.x=x
        self.y=y
        self.color=color
        self.width=150
        self.height=100

    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.height))
        f=pygame.font.SysFont("comicsans",40)
        text=f.render(self.text,1,(0,0,0))
        win.blit(text,(self.x+round(self.width/2)-round(text.get_width()/2),self.y+round(self.height/2)-round(text.get_height()/2)))

    def click(self,pos):
        x1=pos[0]
        y1=pos[1]
        if self.x<=x1<=self.x+self.width and self.y<=y1<=self.y+self.height:
            return True
        else:
            return False

        
def redrawwin(win,game,p):
    win.blit(bg,(0,0))
    #win.fill((128,128,128))
    if not(game.connect()):
        f=pygame.font.SysFont("comicsans",80)
        text=f.render("Waiting for player...",1,(255,0,0),True)
        win.blit(text,(w/2-text.get_width()/2,h/2-text.get_height()/2))
    else:
        f=pygame.font.SysFont("comicsans",60)
        text=f.render("Your Move",1,(0,0,255))
        win.blit(text,(80,200))

        text=f.render("Opponents",1,(255,0,0))
        win.blit(text,(380,200))
        m1=game.player_move(0)
        m2=game.player_move(1)

        if game.bothmove():
            txt1=f.render(m1,1,(0,0,0))
            txt2=f.render(m2,1,(0,0,0))
        else:
            if game.p1move and p==0:
                txt1=f.render(m1,1,(0,0,0))
            elif game.p1move:
                txt1=f.render("Locked In",1,(255,255,0))
            else:
                txt1=f.render("Waiting...",1,(255,255,0))

            if game.p2move and p==1:
                txt2=f.render(m2,1,(0,0,0))
            elif game.p2move:
                txt2=f.render("Locked In",1,(255,255,0))
            else:
                txt2=f.render("Waiting...",1,(255,255,0))

        if p==1:
            win.blit(txt2,(100,350))
            win.blit(txt1,(400,350))
        else:
            win.blit(txt1,(100,350))
            win.blit(txt2,(400,350))

        for b in btn:
            b.draw(win)
    pygame.display.update()
        
btn=[Button("Rock",50,500,(255,0,0)),Button("Paper",250,500,(0,255,0)),Button("Scissors",450,500,(0,0,255))]


def main():
    run=True
    clock=pygame.time.Clock()
    n=Network()
    player=int(n.getP())
    print("You are player",player)
    while run:
        clock.tick(60)
        try:
            game=n.send("get")
        except:
            run=False
            print("Couldn't get game")
            break
        if game.bothmove():
            redrawwin(win,game,player)
            pygame.time.delay(500)
            try:
                game=n.send("reset")
            except:
                run=False
                print("No game available")
                break
            f=pygame.font.SysFont("comicsans",90)
            if (game.win()==1 and player==1) or (game.win()==0 and player==0):
                text=f.render("You Won",1,(210,105,30))
            elif game.win()==-1:
                text=f.render("Tie Game!",1,(210,105,30))
            else:
                text=f.render("You Lost...",1,(210,105,30))
            win.blit(text,(w/2-text.get_width()/2,h/2-text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                run=False
                pygame.quit()

            if e.type==pygame.MOUSEBUTTONDOWN:
                pos=pygame.mouse.get_pos()
                for b in btn:
                    if (b.click(pos)) and (game.connect()):
                        if player==0:
                            if not game.p1move:
                                n.send(b.text)
                        else:
                            if not game.p2move:
                                n.send(b.text)
        redrawwin(win,game,player)
def screen():
    run=True
    clock=pygame.time.Clock()
    while run:
        clock.tick(60)
        win.fill((128,128,128))
        f=pygame.font.SysFont("comicsans",60)
        text=f.render("Click to Play!",1,(0,0,0))
        win.blit(text,(100,200))
        pygame.display.update()
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                run=False
                pygame.quit()
            if e.type==pygame.MOUSEBUTTONDOWN:
                run=False
    main()

while True:
    screen()
