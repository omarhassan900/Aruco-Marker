import cv2

if __name__ == '__main__':

    cap = cv2.VideoCapture(0)
    cap.set(3, 1024)
    cap.set(4, 720)

    while True:
        success, img = cap.read()
        cv2.imshow('vid', img)
