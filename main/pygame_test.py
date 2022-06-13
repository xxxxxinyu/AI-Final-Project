import sys

import pygame
from pygame.locals import QUIT

# 初始化
pygame.init()
# 建立 window 視窗畫布，(x*y), flags=0 (預設為0，可自行設定)
window_surface = pygame.display.set_mode((1200, 600))
# 設置視窗標題
pygame.display.set_caption('腦鍛鍊')
# 清除畫面並填滿背景色
window_surface.fill((255, 255, 255))

# 宣告 font 文字物件 字型, 字體大小
head_font = pygame.font.SysFont(None, 20)
# 渲染方法會回傳 surface 物件 把head font樣式渲染到text surface上，內容, 是否平滑, 字體顏色(rgb), [背景色(rgb)] 
text_surface = head_font.render('Hello World!', True, (0, 0, 0), (255, 0, 0))
text_rect = text_surface.get_rect() # 獲得矩形座標<rect(0, 0, 77, 13)> x=0, width=77, y=3, height=13
text_rect.center = (600, 300) # 把text的中點移到視窗中間<rect(562, 294, 77, 13)>
# blit 用來把其他元素渲染到另外一個 surface 上，這邊是 window 視窗
window_surface.blit(text_surface, (1000, 10)) # x座標, y座標
window_surface.blit(text_surface, text_rect) #渲染第二個到中間

face = pygame.Surface((50,50),flags=pygame.HWSURFACE)
face.fill(color='pink')
window_surface.blit(face, (100, 100))
# 更新畫面，等所有操作完成後一次更新（若沒更新，則元素不會出現
pygame.display.flip()
# pygame.display.update() 更新部分視窗用這個

# 事件迴圈監聽事件，進行事件處理
while True:
    # 迭代整個事件迴圈，若有符合事件則對應處理
    for event in pygame.event.get():
        # 當使用者結束視窗(按叉叉)，程式也結束
        if event.type == QUIT:
            pygame.quit()
            sys.exit()