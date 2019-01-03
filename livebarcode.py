from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2

#argparser
ap = argparser.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes.csv", help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())

#init vid stream - wait for warm up
print("[Info] starting video stream...")
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

#open output csv and initialize barcode set
csv = open(args["output"], "w")
found = set()

#loop over frames
while True:
  #get frame and resize to max width of 400px
  frame = vs.read()
  frame = imutils.resize(frame, width=400)

  #find barcodes and decode
  barcodes = pyzbar.decode(frame)
  for barcode in barcodes:
    #find bounds of barcode in image
    #draw box around barcode in image
    (x,y,w,h) = barcode.rect
    cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)

    #barcode date is a bytes obj must convert to string
    barcodeData = barcode.data.decode("utf-8")
    barcodeType = barcode.type

    #draw barcode data and type on image
    text = "{} ({})".format(barcodeData, barcodeType)
    cv2.putText(img, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

    #print the barcode and type to terminalk
    print("[INFO] found {} barcode: {}".format(barcodeType, barcodeData))

    #if barcode text not in csv write to csv
    if barcodeData not in found():
      csv.write("{},{},{}\n".format(datetime.datetime.now(), barcodeData, barcodeType)
      csv.flush()
      found.add(barcodeData)
  #show output frame
  cv2.imshow("Barcode Scanner", frame)
  key = cv2.waitKey(1) & 0xFF

  # if the `q` key was pressed, break from the loop
  if key == ord("q"):
    break

# close the output CSV file do a bit of cleanup
print("[INFO] cleaning up...")
csv.close()
cv2.destroyAllWindows()
vs.stop()