# https://u9534056.medium.com/mediapipe-%E7%B0%A1%E5%96%AE%E6%98%93%E7%94%A8%E7%9A%84%E6%B7%B1%E5%BA%A6%E5%AD%B8%E7%BF%92%E6%8E%A8%E7%90%86%E6%A1%86%E6%9E%B6-4898eed9f839
# https://ai.googleblog.com/2019/08/on-device-real-time-hand-tracking-with.html
# https://blog.csdn.net/weixin_38346042/article/details/123399492
import sys
import pygame
import cv2
from pygame.locals import QUIT
import random
import bisect
import mediapipe as mp
import math

BLACK = (0, 0, 0)
GRAY = (155, 155, 155)
WHITE = (255, 255, 255)
RED = (230, 0, 0)
YELLOW = (209, 181, 21)
QUESTION_NUM = 30
COUNTDOWN = 3
class Recognition:
    def __init__(self):
    #     self.mp_drawing = mp.solutions.drawing_utils
    #     self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands

    def vector_2d_angle(self, v1, v2):
        v1_x = v1[0]
        v1_y = v1[1]
        v2_x = v2[0]
        v2_y = v2[1]
        try:
            angle_= math.degrees(math.acos((v1_x*v2_x+v1_y*v2_y)/(((v1_x**2+v1_y**2)**0.5)*((v2_x**2+v2_y**2)**0.5))))
        except:
            angle_ = 180
        return angle_

    def hand_angle(self, hand_):
        angle_list = []
        # thumb 大拇指角度
        angle_ = self.vector_2d_angle(
            ((int(hand_[0][0])- int(hand_[2][0])),(int(hand_[0][1])-int(hand_[2][1]))),
            ((int(hand_[3][0])- int(hand_[4][0])),(int(hand_[3][1])- int(hand_[4][1])))
            )
        angle_list.append(angle_)
        # index 食指角度
        angle_ = self.vector_2d_angle(
            ((int(hand_[0][0])-int(hand_[6][0])),(int(hand_[0][1])- int(hand_[6][1]))),
            ((int(hand_[7][0])- int(hand_[8][0])),(int(hand_[7][1])- int(hand_[8][1])))
            )
        angle_list.append(angle_)
        # middle 中指角度
        angle_ = self.vector_2d_angle(
            ((int(hand_[0][0])- int(hand_[10][0])),(int(hand_[0][1])- int(hand_[10][1]))),
            ((int(hand_[11][0])- int(hand_[12][0])),(int(hand_[11][1])- int(hand_[12][1])))
            )
        angle_list.append(angle_)
        # ring 無名指角度
        angle_ = self.vector_2d_angle(
            ((int(hand_[0][0])- int(hand_[14][0])),(int(hand_[0][1])- int(hand_[14][1]))),
            ((int(hand_[15][0])- int(hand_[16][0])),(int(hand_[15][1])- int(hand_[16][1])))
            )
        angle_list.append(angle_)
        # pink 小拇指角度
        angle_ = self.vector_2d_angle(
            ((int(hand_[0][0])- int(hand_[18][0])),(int(hand_[0][1])- int(hand_[18][1]))),
            ((int(hand_[19][0])- int(hand_[20][0])),(int(hand_[19][1])- int(hand_[20][1])))
            )
        angle_list.append(angle_)
        return angle_list
    
    def hand_pos(self, finger_angle):
        f1 = finger_angle[0]   # 大拇指角度
        f2 = finger_angle[1]   # 食指角度
        f3 = finger_angle[2]   # 中指角度
        f4 = finger_angle[3]   # 無名指角度
        f5 = finger_angle[4]   # 小拇指角度

        # 小於 50 表示手指伸直，大於等於 50 表示手指捲縮
        if f1<50 and f2>=50 and f3>=50 and f4>=50 and f5>=50:
            return 'good'
        elif f1>=50 and f2>=50 and f3<50 and f4>=50 and f5>=50:
            return 'no!!!'
        elif f1<50 and f2<50 and f3>=50 and f4>=50 and f5<50:
            return 'ROCK!'
        elif f1>=50 and f2>=50 and f3>=50 and f4>=50 and f5>=50:
            return '0'
        elif f1>=50 and f2>=50 and f3>=50 and f4>=50 and f5<50:
            return 'pink'
        elif f1>=50 and f2<50 and f3>=50 and f4>=50 and f5>=50:
            return '1'
        elif f1>=50 and f2<50 and f3<50 and f4>=50 and f5>=50:
            return '2'
        elif f1>=50 and f2>=50 and f3<50 and f4<50 and f5<50:
            return 'ok'
        elif f1<50 and f2>=50 and f3<50 and f4<50 and f5<50:
            return 'ok'
        elif f1>=50 and f2<50 and f3<50 and f4<50 and f5>50:
            return '3'
        elif f1>=50 and f2<50 and f3<50 and f4<50 and f5<50:
            return '4'
        elif f1<50 and f2<50 and f3<50 and f4<50 and f5<50:
            return '5'
        elif f1<50 and f2>=50 and f3>=50 and f4>=50 and f5<50:
            return '6'
        elif f1<50 and f2<50 and f3>=50 and f4>=50 and f5>=50:
            return '7'
        elif f1<50 and f2<50 and f3<50 and f4>=50 and f5>=50:
            return '8'
        elif f1<50 and f2<50 and f3<50 and f4<50 and f5>=50:
            return '9'
        else:
            return ''

    def detect_hand(self, img):
        with self.mp_hands.Hands(
                model_complexity=0,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as hands:
            w, h = 480, 480                              # 影像尺寸
            img = cv2.resize(img, (w,h))                 # 縮小尺寸，加快處理效率
            results = hands.process(img)                # 偵測手勢
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    finger_points = []                   # 記錄手指節點座標的串列
                    for i in hand_landmarks.landmark:
                        # 將 21 個節點換算成座標，記錄到 finger_points
                        x = i.x*w
                        y = i.y*h
                        finger_points.append((x,y))
                    if finger_points:
                        finger_angle = self.hand_angle(finger_points) # 計算手指角度，回傳長度為 5 的串列
                        # print(finger_angle)                     # 印出角度 ( 有需要就開啟註解 )
                        text = self.hand_pos(finger_angle)            # 取得手勢所回傳的內容
                        return text
        
class Game:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.window = self.set_window(title)

        self.start_rect = None
        self.again_rect = None

        self.start_clicked = False
        self.again_clicked = False
        self.is_get_ques = False
        self.ques_num = 0
        self.update_ques = True
        self.is_correct = False

        self.clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        self.counter, self.counterText = COUNTDOWN, str(COUNTDOWN)

        self.start = -1
        self.timer = -1

        self.key = None
        self.state = 'initial'
        self.last = -1
        self.cooldown = 500
        self.images = {}

        self.cap = self.set_camera()
        self.pic = None
        self.bg = self.load_bg()
        self.recog = Recognition()

        self.grades = []
        self.is_exec = False
        self.rank = -1

    def reset(self):
        self.again_clicked = False
        self.is_get_ques = False
        self.ques_num = 0
        self.update_ques = True
        self.is_correct = False
        self.counter, self.counterText = COUNTDOWN, str(COUNTDOWN)

        self.start = -1
        self.timer = -1

        self.key = None
        self.state = 'main'
        self.last = -1

        self.pic = None
        self.grades = []
        self.is_exec = False
        self.rank = -1

    def set_window(self, title):
        pygame.init()
        pygame.display.set_caption(title)
        return pygame.display.set_mode((self.width, self.height))

    def load_bg(self):
        bg = pygame.image.load("assets/images/bg.jpg")
        bg = pygame.transform.scale(bg, (self.width/2, self.height))
        return bg

    def show_bg(self):
        self.window.blit(self.bg, (0, 0))
    
    def show_overlay(self):
        overlay = pygame.Surface((self.width, self.height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(160)
        self.window.blit(overlay, (0, 0))

    def set_camera(self):
        #0 Is the built in camera
        cap = cv2.VideoCapture(0) ##
        #Gets fps of your camera
        # fps = cap.get(cv2.CAP_PROP_FPS)
        # print("fps:", fps)
        #If your camera can achieve 60 fps
        #Else just have this be 1-30 fps
        # cap.set(cv2.CAP_PROP_FPS, 60)
        return cap

    def show_camera(self):
        X1, Y1, X2, Y2 = 80, 0, 560, 480
        success, frame = self.cap.read()
        if not success:
            return False, None
            
        frame = cv2.flip(frame, 1) ## 
        # frame = np.rot90(frame)
        cv2.rectangle(frame, (X1, Y1), (X2, Y2), (0,255,0) ,1)
        frame = frame[Y1:Y2, X1:X2]
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) ##
        frame = cv2.transpose(frame)
        # image_q = cv2.THRESH_BINARY ##
        # _, pic = cv2.threshold(frame, 158, 255, image_q) ##

        # _, output = cv2.threshold(frame, 158, 255, image_q) ##
        surf = pygame.surfarray.make_surface(frame)
        self.window.blit(surf, (self.height, 0))
        return True, frame

    def show_text(self, content, color, size, x, y, pos='center'):
        style = pygame.font.Font('assets/fonts/cubic.ttf', size)
        text = style.render(content, True, color)
        rect = text.get_rect()
        if pos == 'center':
            rect.center = (x, y)
        elif pos == 'topleft':
            rect.topleft = (x, y)
        self.window.blit(text, rect)

    def draw_rect(self, width, height, x, y, color):
        rect = pygame.Rect(0, 0, width, height)
        rect.center = (x, y)
        pygame.draw.rect(self.window, color, rect, 4)
        return rect

    def load_image(self, name, filename, pos):
        image = pygame.image.load("assets/images/" + filename).convert_alpha()
        self.images[name] = []
        self.images[name].append(image)
        rect = image.get_rect()
        rect.center = (pos[0], pos[1])
        self.images[name].append(rect)

    def show_timer(self):
        timer = pygame.time.get_ticks() - self.start
        timer = timer / 1000 #('%.2f'%timer)
        self.show_text(('%.2f'%timer).rjust(7), BLACK, 50, 300, 10, 'topleft')
        self.timer = timer

    def show_grade(self, filename, grade):
        if self.is_exec:
            pass
        else:
            self.write_grade(filename, float(grade))
        for i in range(5):
            color = YELLOW if i == self.rank else WHITE
            point = str(self.grades[i]) if i < len(self.grades) else '_____'
            self.show_text(str(i+1)+'. '+point, color, 30, self.height-10, 160 + i*40)

    def write_grade(self, filename, grade):
        try:
            f = open("assets/grade/"+ filename, 'r')
            self.grades = f.read().splitlines()
            f.close()
        except FileNotFoundError:
            pass
        self.grades = [float(i) for i in self.grades]
        rank = bisect.bisect_right(self.grades, grade)
        if rank < 5:
            self.grades.insert(rank, grade)
        f = open("assets/grade/"+ filename, 'w')
        for i in range(len(self.grades)):
            f.write(str(self.grades[i]))
            if i != len(self.grades)-1:
                f.write('\n')
        f.close()
        self.is_exec = True
        self.rank = rank

class RPS(Game):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.ques = [('rock_q', '贏', 'paper_a'), ('rock_q', '平手', 'rock_a'), ('rock_q', '輸', 'scissor_a'),
                     ('paper_q', '贏', 'scissor_a'), ('paper_q', '平手', 'paper_a'), ('paper_q', '輸', 'rock_a'),
                     ('scissor_q', '贏', 'rock_a'), ('scissor_q', '平手', 'scissor_a'), ('scissor_q', '輸', 'paper_a')]

        self.q = None
        self.ans = ''
        self.load_rps_image()
        # self.model = self.load_model()
        self.s = 0
        self.r = 0
        self.p = 0
        self.other = 0

    def reset(self):
        super().reset()
        self.q = None
        self.ans = ''
        self.s = 0
        self.r = 0
        self.p = 0
        self.other = 0

    def load_rps_image(self):
        pos_q = (230, 300)
        pos_a = (730, 270)
        rps = ['rock', 'paper', 'scissor']
        for i in rps:
            self.load_image(i + '_q', i + '.png', pos_q)
            self.load_image(i + '_a', i + '_gray.png', pos_a)
        self.load_image('circle', 'circle.png', pos_q)
        self.load_image('cross', 'cross.png', pos_q)

    def show_init(self):
        self.start_rect = self.draw_rect(240, 50, 230, 300, BLACK)
        self.show_text("反應力測試", BLACK, 50, 230, 200)
        self.show_text("開始遊戲", BLACK, 35, 230, 300)
        pygame.draw.line(self.window, BLACK, [80, 240], [380, 240], width=4)
        self.show_text("請讓手掌完整顯示", GRAY, 30, 730, 80)
        pygame.draw.line(self.window, GRAY, [580, 105], [880, 105], width=4)

    def show_countdown(self):
        self.show_text("請根據指示出拳", BLACK, 30, 230, 80)
        pygame.draw.line(self.window, BLACK, [100, 105], [360, 105], width=4)
        self.show_text(self.counterText, BLACK, 100, 230, 250)
        self.start = pygame.time.get_ticks()

    def get_ques(self):
        self.q = random.choice(self.ques)
        self.ques_num += 1
        self.is_get_ques = True

    def show_ques(self):
        self.show_text(str(self.ques_num)+'.', BLACK, 50, 10, 10, 'topleft')
        self.show_text(self.q[1], BLACK, 50, 230, 100)
        self.window.blit(self.images[self.q[0]][0], self.images[self.q[0]][1])

    # def load_model(self):
    #     with open('assets/model/model_trained.json','r') as f:
    #         model_json = json.load(f)
    #     model = model_from_json(model_json)
    #     model.load_weights('assets/model/model_trained.h5')
    #     return model

    # def predict_gesture(self, hand_image, last_gesture):
    #     res = last_gesture
    #     result = self.model.predict(hand_image.reshape(3, 128, 128, 1), verbose = 0)
        
    #     predict = { 
    #         'scissors': result[0][0],
    #         'rocks': result[0][1],    
    #         'papers': result[0][2]
    #         }
    #     #print(predict)
    #     if ((predict['scissors'] == 1.0) & (predict['rocks']==0.0) & (predict['papers']==0.0)):
    #         self.s += 1
    #     elif ((predict['scissors'] == 0.0) & (predict['rocks']==1.0) & (predict['papers']==0.0)):
    #         self.r += 1
    #     elif ((predict['scissors'] == 0.0) & (predict['rocks']==0.0) & (predict['papers']==1.0)):
    #         self.p += 1
    #     else:
    #         self.other += 1

    #     if self.s == 5:
    #         res = 'scissor_a'
    #         self.s, self.r, self.p, self.other = 0, 0, 0, 0
    #     elif self.r == 5:
    #         res = 'rock_a'
    #         self.s, self.r, self.p, self.other = 0, 0, 0, 0
    #     elif self.p == 5:
    #         res = 'paper_a'
    #         self.s, self.r, self.p, self.other = 0, 0, 0, 0
    #     elif self.other == 5:
    #         res = None
    #         self.s, self.r, self.p, self.other = 0, 0, 0, 0
    #     return res

    def show_predict(self, hand_image):
        ans_dict = {'2': 'scissor_a', '5': 'paper_a', '0': 'rock_a'}
        ans = self.recog.detect_hand(hand_image)
        img = None
        if ans in ans_dict:
            img = ans_dict[ans]
            self.window.blit(self.images[img][0], self.images[img][1])
        elif ans == '':
            pass
        else:
            self.show_text('?', GRAY, 300, 750, 260)
        return img

    def exec_game(self, ans):
        if not self.is_get_ques:
            self.get_ques()
            if self.ques_num > QUESTION_NUM: # jump to end
                self.state = 'end'
                return
        self.show_ques()
        self.show_timer()
        if ans == self.q[2]:
            self.is_correct = True
            if self.last == -1:
                self.last = pygame.time.get_ticks()

        if self.is_correct:
            self.window.blit(self.images['circle'][0], self.images['circle'][1])
            now = pygame.time.get_ticks()
            if now - self.last >= self.cooldown:
                self.last = -1
                self.is_correct = False
                self.is_get_ques = False
                self.ans = None
                self.key = None   
        
    def show_end(self):
        self.show_overlay()
        self.show_text('你的成績：'+('%.2f'%self.timer), WHITE, 50, self.height-10, 100)
        self.show_grade('rps.txt', ('%.2f'%self.timer))
        self.again_rect = self.draw_rect(240, 50, 480, 400, WHITE)
        self.show_text("重新開始", WHITE, 35, 480, 400)

    def show_error(self):
        self.show_overlay()
        self.show_text('未連接鏡頭或鏡頭無法運作 :(', WHITE, 50, 480, 240)

def main():
    game = RPS(960, 480, '反應力測試')
    ans = None
    while True:
        game.clock.tick(60)
        sucess, pic = game.show_camera()
        ans = game.show_predict(pic)
        if not sucess:
            game.state = 'error'
        game.show_bg()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.state == 'initial':
                    if game.start_rect.collidepoint(event.pos):
                        game.start_clicked = True
                if game.state == 'end':
                    if game.again_rect.collidepoint(event.pos):
                        game.again_clicked = True

            if event.type == pygame.KEYDOWN:
                game.key = event.key

            if event.type == pygame.USEREVENT and game.start_clicked and game.counter > 0: 
                game.counter -= 1
                game.counterText = str(game.counter) if game.counter > 0 else ''

        if game.state == 'initial':
            game.show_init()
            if game.start_clicked:
                game.state = 'main'
        elif game.state == 'main':
            if game.counter > 0:
                game.show_countdown()
            else:
                game.exec_game(ans)
        elif game.state == 'end':
            game.show_end()
            if game.again_clicked:
                game.reset()
        elif game.state == 'error':
            game.show_error()

        pygame.display.flip()

if __name__ == '__main__':
    main()
    
# <a href='https://www.freepik.com/photos/notebook-background'>Notebook background photo created by kues - www.freepik.com</a>
# <a href="https://www.flaticon.com/free-icons/rock-paper-scissors" title="rock paper scissors icons">Rock paper scissors icons created by Freepik - Flaticon</a>