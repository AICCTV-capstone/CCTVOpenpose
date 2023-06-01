#위 코드는 TensorFlow Lite와 OpenCV를 사용하여 물체 탐지를 수행

import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision

detector = None

def init(model='object_detection.tflite'): #모델 파일 경로(model)를 인자로 받기
    global detector #물체 탐지기(detector)를 생성

    # 물체 탐지기를 위한 옵션 설정
    base_options = core.BaseOptions(file_name=model, num_threads=4)
    
    #탐지할 수 있는 최대 결과 수는 5개로 설정, 점수(threshold) 임계값은 0.3으로 설정
    detection_options = processor.DetectionOptions(max_results=5, score_threshold=0.3)
    options = vision.ObjectDetectorOptions(base_options=base_options, detection_options=detection_options)

    # 물체 탐지기 생성
    detector = vision.ObjectDetector.create_from_options(options)



#입력 이미지에서 물체를 탐지하는 함수
def detect_object(image): 
    global counter

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # 이미지를 RGB로 변환, 해당 이미지를 텐서 이미지로 변환
    input_tensor = vision.TensorImage.create_from_array(rgb_image) # 텐서플로어용 이미지로 변환
    objects = detector.detect(input_tensor)    # 이미지에서 물체들 탐지

    return objects

def count_person(objects): #탐지된 객체 중에서 사람의 수를 계산하여 반환
    count = 0
    for detection in objects.detections:
        first_category = detection.categories[0]
        if first_category.category_name == 'person':
            count += 1 #객체의 카테고리(category_name)가 'person'인 경우에만 카운트를 증가
    return count





def visualize(image, results, fps): #물체 탐지 결과를 시각화
    for detection in results.detections:
        first_category = detection.categories[0]
        (name, score) = (first_category.category_name, round(first_category.score, 2))
        if name != 'person':
            continue
            
        
        bbox = detection.bounding_box
        start_point = bbox.origin_x, bbox.origin_y
        end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
        cv2.rectangle(image, start_point, end_point, (0, 255, 0), 2)

        #물체의 이름과 점수를 텍스트로 출력하고, 해당 텍스트를 이미지 위에 표시
        result_text = name + ' (' + str(score) + ')'
        text_location = (bbox.origin_x+10, bbox.origin_y+20)
        cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)

    return image



def final():
    global detector 
    detector = None #함수를 호출하면 detector 객체를 None으로 설정하여 정리
