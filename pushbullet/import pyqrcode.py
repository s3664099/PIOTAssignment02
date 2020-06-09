import pyqrcode

#Source: https://www.geeksforgeeks.org/python-generate-qr-code-using-pyqrcode-module/

def create_qr_code(first_name, last_name, email):
	#String which represents QR code
	s = "First Name: {}, Last Name: {}, Email: {}".format(first_name, last_name, email)

	#Generate the QR code
	url = pyqrcode.create(s)

	#Create and save the png file naming "myqr.png"
	url.png('myqr.png', scale = 6)

	return "QR code created"
