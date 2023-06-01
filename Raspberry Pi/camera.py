#OpenCV를 사용하여 카메라에서 프레임을 읽어오는 함수들을 정의

import cv2

camera = None

def init(camera_id=0, fps=10, width=640, height=480, buffer_size=1):
    global camera
    camera = cv2.VideoCapture(camera_id)  # 카메라 객체 생성
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)  # 프레임의 가로 크기 설정
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)  # 프레임의 세로 크기 설정
    camera.set(cv2.CAP_PROP_BUFFERSIZE, buffer_size)  # 버퍼 크기 설정
    camera.set(cv2.CAP_PROP_FPS, fps)  # FPS(Frames Per Second) 설정

def take_picture(most_recent=True): #take_picture() 함수는 카메라에서 프레임을 읽어오기
    global camera

    # most_recent가 True이면 버퍼에 저장된 모든 프레임을 버립니다.
    len = 0 if most_recent == False else camera.get(cv2.CAP_PROP_BUFFERSIZE)
    while len > 0:
        camera.grab()  # 버퍼에 저장된 프레임을 버리고, 최신 프레임 가져옴
        len -= 1

    success, image = camera.read()  # 카메라로부터 프레임을 읽어오기
    if not success:
        return None

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # 이미지의 색상 체계를 BGR에서 RGB로 변환
    return image

def final():
    global camera
    if camera is not None:
        camera.release()  # 카메라를 해제
    camera = None





