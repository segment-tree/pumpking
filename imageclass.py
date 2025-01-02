import pygame
from typing import *
import constants as c
class myImage:
    image:pygame.sprite.Sprite
    rect:Any
    mode:int
    # mode==0:以当前格子左下为基准绘制
    # mode==1:以当前格子中心为基准绘制
    def __init__(self,imgdir,zoom=1,mode=0):
        self.image=pygame.image.load(imgdir)
        rect_t=self.image.get_rect()
        h=(rect_t.height*c.CellSize*zoom//rect_t.width)//c.CellRatio
        self.image=pygame.transform.scale(self.image,(int(c.CellSize*zoom)//c.CellRatio,h))
        self.rect=self.image.get_rect()
        self.mode=mode

    def reload(self,imgdir):
        self.__init__(imgdir)
    def draw(self,rx:int,ry:int,camera:Tuple[int,int],win):
        self.rect=self.image.get_rect()
        match self.mode:
            case 0:
                self.rect.move_ip(
                    ( rx-c.CellSize//2 -camera[0] )//c.CellRatio,
                    ( ry+c.CellSize//2-self.rect.height*c.CellRatio -camera[1] )//c.CellRatio
                )
            case 1:
                self.rect.move_ip(
                    ( rx-self.rect.width *c.CellRatio//2 -camera[0] )//c.CellRatio,
                    ( ry-self.rect.height*c.CellRatio//2 -camera[1] )//c.CellRatio
                )
        win.blit(self.image,self.rect)
    def drawG(self,gx:int,gy:int,camera:Tuple[int,int],win): # 按网格坐标渲染
        self.rect=self.image.get_rect()
        match self.mode:
            case 0:
                self.rect.move_ip(
                    ( gx*c.CellSize -camera[0] )//c.CellRatio,
                    ( (gy+1)*c.CellSize-self.rect.height*c.CellRatio -camera[1] )//c.CellRatio
                )
            case 1:
                self.rect.move_ip(
                    ( gx*c.CellSize+c.CellSize//2-self.rect.width *c.CellRatio//2 -2 -camera[0] )//c.CellRatio,
                    ( gy*c.CellSize+c.CellSize//2-self.rect.height*c.CellRatio//2 -2 -camera[1] )//c.CellRatio
                )
        win.blit(self.image,self.rect)

class dialog:
    content:str
    funclist:any #
    usellm:bool
    keysleepcnt:int
    def __init__(self):
        self.content=None
        self.usellm=False
        self.keysleepcnt=c.FPS//2
    def __call__(self, funclist, usellm:bool):
        self.funclist=funclist;self.usellm=usellm
        self.content=next(self.funclist)
        self.keysleepcnt=c.FPS//2
    def keyboard(self):
        if self.content==None:return
        # 检查键盘输入，用于llm，如果有的话
        if self.usellm:
            pass
        self.keysleepcnt-=1
        keys = pygame.key.get_pressed()
        if self.keysleepcnt<=0 and keys[c.KeyboardConDialog]:
            try:
                self.content=next(self.funclist)
            except StopIteration:
                self.content=None
                self.funclist=None
            self.keysleepcnt=c.FPS//2
        if self.keysleepcnt<=0 and keys[c.KeyboardEscDialog]:
            self.content=None
            self.funclist=None
    def draw(self,win):
        if self.content==None:return
        image=pygame.image.load('./assets/utils/dialog.png')
        rect_t=image.get_rect()
        w=c.WinWidth*c.CellSize-c.CellSize
        h=rect_t.height*w//rect_t.width
        image=pygame.transform.scale(image,(w//c.CellRatio,h//c.CellRatio))
        rect=image.get_rect()
        rect.move_ip(int((c.WinWidth-13.5)*c.CellSize/c.CellRatio),int((c.WinHeight-4.5)*c.CellSize/c.CellRatio))
        win.blit(image,rect)
        font = pygame.font.SysFont(None, 32)
        surface = font.render(self.content, True, (0, 0, 0))#目前没接入ai，不能用中文
        win.blit(surface, (c.CellSize/c.CellRatio,int((c.WinHeight-4)*c.CellSize/c.CellRatio)))
        print(self.content)# TODO

class segmentDraw:
    @classmethod
    def drawR(self, gx:int, gy:int, length:int, camera:Tuple[int,int], win):
        color = (255,0,0)
        segment=pygame.Surface((c.CellSize*length//c.CellRatio, c.CellSize//10//c.CellRatio))
        segment.fill(color)
        rect = segment.get_rect()
        rect.move_ip((gx*c.CellSize-camera[0])//c.CellRatio,(gy*c.CellSize-camera[1])//c.CellRatio)
        win.blit(segment,rect)
    @classmethod
    def drawC(self, gx:int, gy:int, length:int, camera:Tuple[int,int], win):
        color = (255,0,0)
        segment=pygame.Surface((c.CellSize//10//c.CellRatio, c.CellSize*length//c.CellRatio))
        segment.fill(color)
        rect = segment.get_rect()
        rect.move_ip((gx*c.CellSize-camera[0])//c.CellRatio,(gy*c.CellSize-camera[1])//c.CellRatio)
        win.blit(segment,rect)

def displayCreateWin():
    if pygame.display.Info().current_w >= 2000:
        c.CellRatio=1
    win = pygame.display.set_mode((c.WinWidth*c.CellSize//c.CellRatio,c.WinHeight*c.CellSize//c.CellRatio))
    return win

#test
import sys
if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock() # 用于控制循环刷新频率的对象
    win = pygame.display.set_mode((c.WinWidth*c.CellSize,c.WinHeight*c.CellSize))
    while True:
        clock.tick(c.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        tree=myImage('./assets/t/54px-Pine_Stage_4.png')
        # tree.drawG(1,0,win)
        tree.draw(c.CellSize//2,c.CellSize+c.CellSize//2,(0,0),win)
        pygame.display.update()
        print(tree.rect)

