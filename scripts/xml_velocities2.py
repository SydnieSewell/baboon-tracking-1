from xml.etree import ElementTree as ET
import math
import cv2
import csv
# Edit these as necessary.
VIDEO_FILEPATH = "./../data/input.mp4"
XML_FILEPATH = "./../xml&velocities/DJI_0870_mp4.xml"
OUTPUT_FILEPATH = "./../xml&velocities/DJI_0870_velocity.csv"

# Velocity threshold to filter
velocityThreshold = 1

# Get fps of video
cap = cv2.VideoCapture(VIDEO_FILEPATH)
FPS = cap.get(cv2.CAP_PROP_FPS)

# Loads XML data into python using etree package


def loadXML(xmlPath):
    XMLtree = ET.parse(xmlPath)
    root = XMLtree.getroot()
    return root

# Finds centroid to be center point between top-left and bottom-right bounding points


def getCentroid(boxElement):
    xtl = float(boxElement.get('xtl'))
    ytl = float(boxElement.get('ytl'))
    xbr = float(boxElement.get('xbr'))
    ybr = float(boxElement.get('ybr'))
    centroid_x = xtl + ((xbr-xtl)/2)
    centroid_y = ytl + ((ybr-ytl)/2)
    return centroid_x, centroid_y

# Computes velocity between previous position (centroid1) and current position(cenroid2)


def computeVelocity(centroid1, centroid2, FPS=FPS):
    if centroid1 is None or centroid2 is None:
        return None
    #Velocity = Distance / Time
    # Distance Formula = sqrt((x2-x1)^2 + (y2-y1)^2 )
    distance = math.sqrt(math.pow(
        centroid2[0]-centroid1[0], 2) + math.pow(centroid2[1]-centroid1[1], 2))
    return distance/(1/FPS)


# Outputs a CSV file containing headers "baboon id", "frame", "centroid_x", "centroid_y", "velocity"
def outputToFile(fileContents, OUTPUT_FILEPATH=OUTPUT_FILEPATH):
    with open(OUTPUT_FILEPATH, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(fileContents)


print("Loading XML into Python")
XML = loadXML(XML_FILEPATH)
print("Loaded file ", XML_FILEPATH)

csvContents = [['baboon id', 'frame', 'centroid_x', 'centroid_y', 'velocity']]

# iter through each baboon in file - labeled "track" in XML
for baboon in XML.iter('track'):
    # prev centroid used to displace velocity
    last_centroid = None
    # iter through each frame the baboon appears in - labeled "box" in XML
    for box in baboon.iter('box'):
        # get centroid from bounding box - returns set with x-dim at 0 & y-dim at 1
        centroid = getCentroid(box)
        velocity = computeVelocity(last_centroid, centroid)
        csvContents.append([baboon.get('id'), box.get(
            'frame'), centroid[0], centroid[1], velocity])
        last_centroid = centroid

# copy of csvContents to filter velocity
csvFilteredContents = csvContents
for dataPoint in csvFilteredContents:
    if dataPoint[4] < velocityThreshold:
        csvFilteredContents.remove(dataPoint)


print("Velocities computed, outputting to ", OUTPUT_FILEPATH)
outputToFile(csvContents)
print("Velocities filtered, outputting to ", OUTPUT_FILEPATH)
outputToFile(csvFIlteredContents)
print("Completed.")