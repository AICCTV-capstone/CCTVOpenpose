import io
import time
import base64
import paho.mqtt.client as mqtt
import json
from PIL import Image
import cv2
import camera
import detect

flag = False

# 연결이 되면 바로 'command' 토픽으로 서브스크라이브 한다
def on_connect(client, userdata, flag, rc):
        client.subscribe("action", qos = 0)

# 'command'라는 토픽으로 데이터가 오면 호출된다
def on_message(client, userdata, msg) :
        global flag

        command = msg.payload.decode("utf-8")
        if command == "goStop" :
                flag = True if(flag == False) else False
            
#MQTT브로커의 IP 주소로 설정하며, 'clien.connect()'를 호출하여 브로커에 연결
broker_ip = "43.201.14.40"

client = mqtt.Client()  # mqtt 객체를 생성한다
client.on_connect = on_connect  # on_connect 콜백함수 등록
client.on_message = on_message  # on_message 콜백함수 등록

client.connect(broker_ip, 1883)
client.loop_start()

# 카메라 객체와 물체 탐지 객체를 생성한다
camera.init(camera_id="./fall.mp4", height = 240, width = 320, fps = 30)
saver.init(dir='./video', fps = 10, width = 320, height = 240, minutes = 10)
detect.init()

#숫자 값을 저장하기 위한 변수
number = 0
prev = 0
start = time.time() #start는 시간 측정을 위한 변수
counter = 0
ticker = 0 #ticker와 sendticker는 타이밍을 제어하기 위한 변수
sendticker = 0

while True :
    #'most_recent' 매개병수가 'True'로 설정되어 있으므로 -> 가장 최근의 이미지를 가져옴
    image = camera.take_picture(most_recent = True) # 카메라에서 이미지를 가져오기
    if image is None:
        camera.final()
        camera.init(camera_id="./fall.mp4", height = 240, width = 320, fps = 30)
        continue
        
sendticker = (sendticker + 1) % 1 #sendticker 변수를 사용하여 일정한 간격으로 이미지를 전송
    if sendticker != 0:
        continue

counter += 1 #현재까지 수신한 프레임 수를 추적하기 위해 사용
    fps = counter / (time.time() - start) # 초당 프레임 수를 구함
  
ticker = (ticker + 1) % 4 #ticker 변수를 사용하여 일정한 간격으로 객체 탐지 작업 수행
if ticker == 0:
    objects = detect.detect_object(image) # 입력 이미지에서 물체를 탐지
    count = detect.count_person(objects) #탐지된 객체 중 사람의 수 계산 후 반환
    client.publish("cmlee1", count, qos=0) # MQTT 클라이언트 사용해서 토빅으로 사람수 게시
    visualized_image = detect.visualize(image, objects, fps) #탐지된 객체와 이미지를 시각화
else:
    visualized_image = image
    
stream = io.BytesIO() #io.BytesIO() 객체를 생성하여 메모리 버퍼에 이미지 데이터 저장
Image.fromarray(visualized_image).save(stream, format='JPEG') #이미지 변환후 JPEG 형식으로 이미지를 저장
stream.seek(0) #버퍼의 파일 포인터 위치를 처음으로 이동.stream에서 읽은 데이터를 Base64로 인코딩
base64Image = base64.b64encode(stream.read()) #stream에서 데이터를 읽어 데이터를 Base64 형식으로 인코딩
asciiImage = base64Image.decode('ascii') #ASCII 문자열로 디코딩,디코딩된 문자열은 asciiImage 변수에 저장

client.publish("cmlee", asciiImage, qos=0) #MQTT 클라이언트를 사용하여 asciiImage를 "cmlee" 토픽으로 게시

camera.final()
client.loop_end()
client.disconnect()
