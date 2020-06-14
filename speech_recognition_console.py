"""
.. module:: speech_recognition_console

"""
import speech_recog as recog
import requests

#Performs a search from the vehicles
def search():
	"""
	Search
	
	"""
	#Calls the voice recognition module
	search = recog.get_speech()

	#Gets the first work in the response
	search = search.split(" ")
	search = search[0]

	#Calls the database to return the vehicles
	url = ("http://127.0.0.1:5000/searchallcars/"+search)
	response = requests.get(url)


	#Prints the vehicles is query is correct, otherwise advises none found
	if response.json() == "Not Found":
		print("No vehicles of the description {} have been found".format(search))
	else:
		for x in response.json():
			print("Rego: {} Make: {} Model: {} Colour: {} Seats: {} Cost: ${}0 ".format(x["rego"], x["make"], x["model"], 
				x["colour"], x["seats"], x["b.colour"]))
	return

#Main voice search console
def main():
	"""
	Main console

	"""
	running = True

	while running == True:
		print("1) Voice Search")
		print("2) Quit")
		query = input("Select Option: ")

		if query == "1":
			search()
		elif query == "2":
			running = False
			print("goodbye")
		else:
			print("Incorrect input, please try again")

#Execute Program
if __name__ == "__main__":
	main()