import cv2
import json
from tensorflow.keras.models import load_model
from tensorflow.keras.models import model_from_json

# 讀訓練好的model

with open('model_trained.json','r') as f:
    model_json = json.load(f)
loaded_model = model_from_json(model_json)
loaded_model.load_weights('model_trained.h5')

def run(hand_image, s, r, p, other):  
    res = 'no_sign'
    result = loaded_model.predict(hand_image.reshape(1, 128, 128, 1), verbose = 0)
    
    predict = { 
        'scissors': result[0][0],
        'rocks': result[0][1],    
        'papers': result[0][2]
        }
    #print(predict)
    if ((predict['scissors'] == 1.0) & (predict['rocks']==0.0) & (predict['papers']==0.0)):
         s += 1
    elif ((predict['scissors'] == 0.0) & (predict['rocks']==1.0) & (predict['papers']==0.0)):
         r += 1
    elif ((predict['scissors'] == 0.0) & (predict['rocks']==0.0) & (predict['papers']==1.0)):
         p += 1
    else:
        other += 1

    if s == 5:
      res = 'Scissors'
    elif r == 5:
      res = 'Rocks'
    elif p == 5:
      res = 'Papers'
    elif other == 5:
        res = 'Other'
    return res,s,r,p,other
      
def game():
    camera = cv2.VideoCapture(0)
    wzs = 158
    X1,Y1,X2,Y2 = 160,140,400,360 
    image_q = cv2.THRESH_BINARY
    s, r, p, other = 0, 0, 0, 0

    while True:
        _, FrameImage = camera.read()
        FrameImage = cv2.flip(FrameImage, 1) 
        cv2.rectangle(FrameImage, (X1, Y1), (X2, Y2), (0,255,0) ,1)
        INPUT = FrameImage[Y1:Y2, X1:X2]
        INPUT = cv2.resize(INPUT, (128, 128)) 
        INPUT = cv2.cvtColor(INPUT, cv2.COLOR_BGR2GRAY)
        _, output = cv2.threshold(INPUT, wzs, 255, image_q)
        SHOW = cv2.resize(INPUT, (256, 256))
        _, output2 = cv2.threshold(SHOW, wzs, 255, image_q)
        cv2.imshow("HAND", output2)
        
        k = cv2.waitKey(10)
        res,s,r,p,other = run(output,s,r,p,other)
        if res != 'no_sign':
            print(res)
            s, r, p, other = 0, 0, 0, 0 #restart
            #time.sleep(3)
            
        if k == 27: # esc
            break
        
    camera.release()
    cv2.destroyAllWindows()