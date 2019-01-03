from pyzbar import pyzbar
import argparse
import cv2

#argparse
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

#load image
img = cv2.imread(args["image"])

#find barcodes
barcodes=pyzbar.decode(img)

#loop over barcodes
for barcodes in barcodes:
  #find bounds of barcode in image
  #draw box around barcode in image
  (x,y,w,h) = barcode.rect
  cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)

  #barcode date is a bytes obj must convert to string
  barcodeData = barcode.data.decode("utf-8")
  barcodeType = barcode.type

  #draw barcode data and type on image
  text = "{} ({})".format(barcodeData, barcodeType)
  cv2.putText(img, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

  #print the barcode and type to terminalk
  print("[INFO] found {} barcode: {}".format(barcodeType, barcodeData))

#show image output
cv2.imshow("Image", img)
cv2.waitKey(0)