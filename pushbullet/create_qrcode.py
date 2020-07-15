"""
.. module:: create_qrcode

"""
import pyqrcode

file_name = "myqr.png"

#Source: https://www.geeksforgeeks.org/python-generate-qr-code-using-pyqrcode-module/

def create_qr_code(first_name, last_name, email):
	"""
	Create the QR code
	
	"""
	#String which represents QR code
	s = "First Name: {}, Surname: {}, email {}".format(first_name, last_name, email)

	#Generate the QR code
	url = pyqrcode.create(s)

	#Create and save the png file naming "myqr.png"
	url.png(file_name, scale = 6)

	return "QR code created"
