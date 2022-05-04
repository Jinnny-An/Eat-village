from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from mainpage import recommend_ml
from glob import glob
import re
from numpy import rec
# Create your views here.
# import recommend_ml as rc


user_ingre = []
# Create your views here.

def main(request):      
    return render(request, 'mainpage/mainpage.html')

def ingred_recomm(request):
        
    # recommend_data = recommend_ml.recommend_recipe(user_data,recipe_data)
    # return render(request, 'mainpage/recipe_recom.html', {'recommend' : recommend_data})
    
    return render(request, 'mainpage/recipe_recom.html')

def recipe_search(request):
    return render(request, 'mainpage/recipe_search.html')

def ingred_result(request): # 여기가 추가 데이터 처리하는 페이지

    user_data = list(set(user_ingre))
    # 당근,사과,오이,양파
    user_data.append('당근')
    user_data.append('사과')
    user_data.append('오이')
    user_data.append('양파')
    # re_data = recipe_data.objects.all()
    recommend_data = recommend_ml.recommend_recipe(user_data,recipe_data)
    
    # return render(request,'mainpage/ingredients_result.html',{'user' : user_data, 'recommend' : recommend_data})
    return render(request,'mainpage/ingredients_result.html',{'user_data' : user_data,'recommend' : recommend_data,})
    # return render(request, 'mainpage/ingredients_result.html')

def ingred_change(request):
    return render(request, 'mainpage/ingredients_change.html')


# def test(request):
#     user_data = list(set(user_ingre))
#     # 당근,사과,오이,양파
#     user_data.append('당근')
#     user_data.append('사과')
#     user_data.append('오이')
#     user_data.append('양파')
#     re_data = recipe_data.objects.all()
#     recommend_data = recommend_ml.recommend_recipe(user_data,recipe_data)
    
#     # return render(request,'recipe/test.html',{'data' : re_data, 'user' : user_data, 'recommend' : recommend_data})
#     return render(request,'mainpage/ingred_result.html',{'data' : re_data, 'user' : user_data, 'recommend' : recommend_data, 'user_ingre' : user_ingre})     
# ------------------------------------------------------------------------------
from django.shortcuts import render
from django.http import StreamingHttpResponse
import yolov5,torch
from yolov5.utils.general import (check_img_size, non_max_suppression, scale_coords, 
                                  check_imshow, xyxy2xywh, increment_path)
from yolov5.utils.torch_utils import select_device, time_sync
from yolov5.utils.plots import Annotator, colors
from deep_sort.deep_sort import DeepSort
from deep_sort.utils.parser import get_config
from time import time

import cv2
from PIL import Image as im
# Create your views here.

print(torch.cuda.is_available())
#load model
model = yolov5.load('yolov5s.pt')
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
device = select_device('') # 0 for gpu, '' for cpu
# initialize deepsort
cfg = get_config()
cfg.merge_from_file("deep_sort/configs/deep_sort.yaml")
deepsort = DeepSort('osnet_x0_25',
                    device,
                    max_dist=cfg.DEEPSORT.MAX_DIST,
                    max_iou_distance=cfg.DEEPSORT.MAX_IOU_DISTANCE,
                    max_age=cfg.DEEPSORT.MAX_AGE, n_init=cfg.DEEPSORT.N_INIT, nn_budget=cfg.DEEPSORT.NN_BUDGET,
                    )
# Get names and colors
names = model.module.names if hasattr(model, 'module') else model.names

def stream():
    global user_ingre
    
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # cap = cv2.VideoCapture(1)
    # model.conf = 0.65
    # model.iou = 0.5
    # model.classes = [1,2,3,4,6,7,8,10,11]
    
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: failed to capture image")
            break
        
        results = model(frame, augment=True)
        # proccess
        annotator = Annotator(frame, line_width=2, pil=not ascii) 
        det = results.pred[0]
        if det is not None and len(det):   
            xywhs = xyxy2xywh(det[:, 0:4])
            confs = det[:, 4]
            clss = det[:, 5]
            outputs = deepsort.update(xywhs.cpu(), confs.cpu(), clss.cpu(), frame)
            if len(outputs) > 0:
                for j, (output, conf) in enumerate(zip(outputs, confs)):

                    bboxes = output[0:4]
                    id = output[4]
                    cls = output[5]

                    c = int(cls)  # integer class
                    label = f'{id} {names[c]} {conf:.2f}'
                    annotator.box_label(bboxes, label, color=colors(c, True))
                    # print(c,label) # set 형식으로 받아야한다. 그래야 중복데이터가 안들어 오기 때문이다.
                    
                    label = label.split(' ')
                    # print(label[1])
                    user_ingre.append(label[1]) # user_ingre 데이터에 인식된 값을 추가한다. 이걸로 추천시스템 구현
                    
                    # user_ingre_set = list(set(user_ingre))
                    user_ingre = list(set(user_ingre))
                    print(user_ingre)
        else:
            deepsort.increment_ages()

        # print(det)
        im0 = annotator.result()    
        image_bytes = cv2.imencode('.jpg', im0)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image_bytes + b'\r\n')
    
def video_feed(request):
    return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame')