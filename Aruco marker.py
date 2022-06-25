import cv2
import cv2.aruco as aruco
import paho.mqtt.client as mqtt  # import the client
import time
import numpy as np
import os
import  math


def getCameraMatrix():
    with np.load('System.npz') as X:
        print()
        camera_matrix, dist_coeff, _, _ = [X[i] for i in ('mtx', 'dist', 'rvecs', 'tvecs')]
    return camera_matrix, dist_coeff


def findArucoMarker(img, markersize=6, totalmarkers=250, draw=True):
    imgGray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   #Convert colored image to B&W image
    key=getattr(aruco,f'DICT_{markersize}X{markersize}_{totalmarkers}')   #Access the aruco marker as an attribute object
    arucoDict= aruco.Dictionary_get(key)
    arucoparam= aruco.DetectorParameters_create()

    bbox , ids, rejected= aruco.detectMarkers(imgGray,arucoDict, parameters=arucoparam) # this function returns the 1-boundary box edges  2- id of Arduco marker 3-number of unknown aruco markers
    #print(ids)
    #print(bbox)

    if draw:
        aruco.drawDetectedMarkers(img,bbox) # Draw the boundary box in the image


    return [ids,bbox]


def _map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def calc_angle(x1,y1,x2,y2):
    m1 = 0
    m2 = (y2 - y1) / (x2 - x1)
    tanTheta = abs((m1 - m2) / (1 + m1 * m2))
    angle = math.degrees(math.atan(tanTheta))

    # print(x1,y1,"  ",x2,y2)

    if x1 > x2 and y1 > y2:
        angle = _map(angle, 0, 90, 90, 0) + 270

    if x1 < x2 and y1 < y2:
        angle = _map(angle, 90, 0, 0, 90) + 90

    if x2 > x1 and y1 > y2:
        angle = angle + 180

    return angle

def main():
    cap=cv2.VideoCapture(0) # Capture data from the camera
  #  broker_address = "10.5.5.3"
    # broker_address
    print("creating new instance")
 #   client = mqtt.Client("P1")  # create new instance with a name P1
    print("connecting to broker")
#    client.connect(broker_address)  # connect to broker
    #print("Subscribing to topic", "house/bulbs/bulb1")
    #client.subscribe("house/bulbs/bulb1")
    #print("Publishing message to topic", "house/bulbs/bulb1")
# client.publish("senssoe/location", "OFF")

    while True:
        sccuess, img= cap.read()   # convert the video data to images
        arucoFound=findArucoMarker(img) # the above function that detect the Aruco marker and return the bbox and the ID
        #print(arucoFound[1])
        bbox_data = arucoFound[1]    # boundary box
        if bbox_data:                #if Aruco marker founded
            bbox_data=arucoFound[1]
            ed=bbox_data[0]
            edges=ed[0]
            lcorner=edges[0]
            rcorner=edges[3]

            x1=lcorner[0]#-330   #-140
            y1=lcorner[1]  #+250  # -82
            x2=rcorner[0]
            y2=rcorner[1]
            angle=calc_angle(x1,y1,x2,y2)


            location = str([x1, y1])    #convert the X and Y positions to a string to send it to the Mqtt server

           #print(angle," ",location)
            print("a7aaa")

            rows, cols, _ =img.shape
            print(rows," ",cols)






        #  print(location)
        #           client.publish("sensor/location", location)     #publish the data string to the mqtt broker with name "sensor/location"
        #time.sleep(0.5)
        #print(lcorner)
        #print (edges[1])
        cv2.imshow("Image",img)        #show the image in a new window
        cv2.waitKey(1)



if __name__ == "__main__":
    main()
