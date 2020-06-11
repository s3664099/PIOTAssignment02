# USAGE
# python3 barcode_scanner_console.py

## Acknowledgement
## This code is adapted from:
## https://www.pyimagesearch.com/2018/05/21/an-opencv-barcode-and-qr-code-scanner-with-zbar/
## pip3 install pyzbar

# import the necessary packages
from imutils.video import VideoStream
from pyzbar import pyzbar
import imutils
import cv2
import time


def read_qr_no_webcam(first_name, last_name):

	name = "{}{}".format(first_name,last_name)

	frame = cv2.imread('{}.png'.format(name))
	barcodeData = decode_frame(frame)

	return barcodeData

def decode_frame(frame):

	barcodes = pyzbar.decode(frame)

	# loop over the detected barcodes
	for barcode in barcodes:
		# the barcode data is a bytes object so we convert it to a string
		barcodeData = barcode.data.decode("utf-8")
			
		return barcodeData

def read_qr_webcam(first_name, last_name):

	name = "{}{}".format(first_name,last_name)

	# initialize the video stream and allow the camera sensor to warm up
	print("[INFO] starting video stream...")
	vs = VideoStream(src = 0).start()
	time.sleep(2.0)

	frame = cv2.imread('{}.png'.format(name))

	found_data = False

	# loop over the frames from the video stream
	while found_data == False:
		# grab the frame from the threaded video stream and resize it to
		# have a maximum width of 400 pixels
		frame = vs.read()

		frame = imutils.resize(frame, width = 400)

		barcodeData = decode_frame(frame)

		if barcodeData != None:
			found_data = True
	
		# wait a little before scanning again
		time.sleep(1)

	return barcodeData
