import cv2
import os

#init folder and check number of images in each folder
path = 'data'
if not os.path.exists(path):
    os.makedirs(path)
img = (
    {'name':'scissors', 'index': 0}, 
    {'name':'rocks', 'index': 0},
    {'name':'papers', 'index': 0},
    )
for i in range(3):
    if not os.path.exists(os.path.join(path,img[i]['name'])):
        os.makedirs(os.path.join(path,img[i]['name']))
    img[i]['index'] = len(os.listdir(os.path.join(path,img[i]['name'])))

print('1: SCISSORS, 2: ROCKS, 3: PAPERS')
print('l: lower quality, u: upper quality')
print("------------ESC TO EXIT!------------")
#------------------------------------------------------#
camera = cv2.VideoCapture(0)
wzs = 158
X1,Y1,X2,Y2 = 160,140,400,360 

while True:
    _, FrameImage = camera.read()
    FrameImage = cv2.flip(FrameImage, 1) 
    cv2.rectangle(FrameImage, (X1, Y1), (X2, Y2), (0,255,0) ,1)
    hand = FrameImage[Y1:Y2, X1:X2]
    hand = cv2.resize(hand, (256, 256)) 
    hand = cv2.cvtColor(hand, cv2.COLOR_BGR2GRAY)
    _, output = cv2.threshold(hand, wzs, 255, cv2.THRESH_BINARY)
    cv2.imshow("HAND", output)
    
    k = cv2.waitKey(1) #input by keyboard
    if 0 <= k-49 < 3:
        i=k-49
        print("YOU CHOOSE:", img[i]['name'])
        print('SPACE TO START TAKE A PICTURE!')
    elif k & 0xFF == ord('l'): # lower wzs quality
        wzs-=5
    elif k & 0xFF == ord('u'): # upper wzs quality
        wzs+=5
    elif k == 32: #space
        img[i]['index']+=1
        print(img[i]['index'])
        cv2.imwrite(os.path.join(path,img[i]['name'],str(img[i]['index'])+'.jpg'),output)
    if k == 27: #esc
        break
        
camera.release()
cv2.destroyAllWindows()