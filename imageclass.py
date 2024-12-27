import pygame
from typing import *
import constants as c
class myImage:
    image:pygame.sprite.Sprite
    rect:Any
    def __init__(self,imgdir):
        self.image=pygame.image.load(imgdir)
        rect_t=self.image.get_rect()
        h=rect_t.height*c.CellSize//rect_t.width
        self.image=pygame.transform.scale(self.image,(c.CellSize,h))
        self.rect=self.image.get_rect()

    def reload(self,imgdir):
        self.__init__(imgdir)
    def draw(self,rx:int,ry:int,camera:Tuple[int,int],win):
        self.rect.move_ip(rx-c.CellSize//2 +camera[0],ry+c.CellSize//2-self.rect.height +camera[0])
        win.blit(self.image,self.rect)
    def drawG(self,gx:int,gy:int,camera:Tuple[int,int],win): # 按网格坐标渲染
        self.rect.move_ip(gx*c.CellSize +camera[0],(gy+1)*c.CellSize-self.rect.height +camera[1])
        win.blit(self.image,self.rect)

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

