import xml.etree.ElementTree as ET
import os
import urllib
import urllib2
from math import ceil


#This will play mp3's using the computer's default action	
#TODO: Do some research to see if any podcasts use formats other than mp3
def os_play_mp3(location):
	if location.endswith('.mp3'):
		os.startfile(location)

#we will use a feeds.txt file to store the podcast feeds
#TODO: Maybe don't hardcode the filename?
def check_and_create_feedstxt():
	if not os.path.isfile("feeds.txt"):
		f = open("feeds.txt", "w")
		f.close()
	
def handle_feed_choice():
	i = 0
	choice_list = []
	feed_file = open("feeds.txt", "r")
	
	#print the menu of podcast feeds, while simultaneously storing them in a list. We store it in a list so we no longer have to keep the file open, but we also can add a new entry in case the user inputs one
	print ""
	for line in feed_file:
		choice_list.append(line)
		print str(i+1) + ". " + line
		i+=1
	
	#read the user input
	print ""
	xml_choice = raw_input("Choose a feed from the list, or type in a new URL to read: \n")
	feed_file.close()
	
	#attempt to convert it to an int first
	#kinda ugly because we're depending on
	#an exception to determine the value
	#of the variable, plus we just have
	#a blank except block
	try:
		xml_choice = int(xml_choice)
	except:
		pass
	
	#if the xml_choice is an int, we check if the number is in the correct range of choices, and use it if possible
	#'type(42)' should just return the int type, I just wasn't sure how to write the int type without doing this
	if type(xml_choice) == type(42):
		if xml_choice <= len(choice_list) and xml_choice > 0:
			return choice_list[xml_choice - 1]
		else:
			print "Your choice was not in the correct range\n\n"
			return None
	
	#if the xml_choice variable is a string, we want to treat it as a link to a podcast. We check this by seeing if we can access it online
	elif type(xml_choice) == type("a"):
		try:
			urllib2.urlopen(xml_choice)
		except:
			print "You entered an invalid URL\n"
			return None
		else:
			if xml_choice in choice_list:
				return xml_choice
			
			
			choice_list.append(xml_choice)
			feed_file = open("feeds.txt", "w")
			for entry in choice_list:
				if entry.endswith("\n"):
					feed_file.write(entry)
				else:
					feed_file.write(entry+"\n")
			feed_file.close()
			return xml_choice
			
	#We probably won't ever get to this block because raw_input() always returns a string.
	#Better safe than sorry, though.
	else:
		print "Invalid input\n"
		return None
	
	
def remove_xml_entry(xml_path):
	#Read into a list
	f = open("feeds.txt", "r")
	l = []
	for line in f:
		l.append(line)
	f.close()
	
	
	f = open("feeds.txt", "w")
	#write out to the file, unless the current is the one we've found to be invalid, in which case we skip past it
	#we could just pop the invalid entry from the list with l.pop(l.index(line)), but we have to iterate through the list
	#to write it back anyway, so we might as well do it this way
	for entry in l:
		if entry.strip().rstrip() != xml_path:
			f.write(entry)
	f.close()

	
	
#Main Section

check_and_create_feedstxt()

#Read the xml path until the choice given is valid
xml_path = handle_feed_choice()
while xml_path == None:
	xml_path = handle_feed_choice()


#we must do this because the list is newline delimited
xml_path = xml_path.strip().rstrip()


#once we get to this point, it is possible that the entry could just be a random, non-xml webpage
#if this is the case, then the following will fail.  To remedy this, I have used try-catch here, 
#and also implemented a method that will remove the invalid page from the list
xml_data = urllib2.urlopen(xml_path).read()
try:
	root = ET.fromstring(xml_data)
except:
	print "The XML of your podcast was not in the correct format. It may be an HTML page."
	remove_xml_entry(xml_path)
	exit(1)

item_list = []

#this works based off the structure of rss xml.  I don't really like how explicit it is, but it should work as long as the xml complies
for item in root.iter('item'):
	curr_map = {}
	curr_map['title'] = item.find('title').text
	curr_map['url'] = item.find("enclosure").get('url')
	item_list.append(curr_map)
	
	
	
#if this block hits, it probably means that the user gave us the path to a xml file,
#but not an rss podcast xml.
#TODO: Find a better way to check for invalid xml files
if len(item_list) == 0:
	print "The XML of your podcast was not in the correct format"
	remove_xml_entry(xml_path)
	exit(1)



entries_per_page = 15 #we can adjust the amount of items per page by changing this variable

curr_entries = 0 #kinda unnecessary variable because it can be derived from curr_page, but it improves readability so I'm keeping it
curr_page = 1
curr_increment = 0
list_range = int(ceil(len(item_list) / entries_per_page)) + 1

#this will basically act as our menu
#Even though infinite loops are generally bad style, we don't have a set number of iterations
#that we plan to reach as an ending-condition, so it makes the most sense to use an infinite loop.
#Also, I added a quit option for the user, so the loop doesnt require a selection in order to exit
while True:
	print ""
	print "Page ", curr_page
	
	#either print the correct increment, or if the page will have less than the correct increment, then print the remaining amount
	curr_increment = entries_per_page if len(item_list) - curr_entries >= entries_per_page else len(item_list) - curr_entries
	
	for j in range(curr_entries, curr_entries + curr_increment):
		print (j - curr_entries) + 1, ((item_list[j])['title']).encode('ascii', 'ignore')
	
	
	n = raw_input("Type the number of the entry you would like to play, type 'n' for next, type 'q' to quit: ")
	
	
	
	
	#the user wants the next page if they type 'n'
	if n == "n":
		if curr_page + 1 > list_range:
			exit(0)
		
		curr_entries += curr_increment
		curr_page += 1
		continue
		
	#A quit option for the sake of it
	elif n == "q":
		exit(0)
		
		
	#Hastily made page jump feature. Example: typing 'j10' will jump you to page 10
	elif n[0] == "j": 
		#in case someone types in something other than a number, they jump to page 1
		try:
			jump_page = int(n[1:])
		except:
			jump_page = 1
		
		#if they type a number lower than 1, they go to page 1
		if jump_page < 1:
			jump_page = 1
			
		#if they type a number higher than the max, they go to the last page
		elif jump_page > list_range:
			jump_page = list_range
		
		curr_page = jump_page
		curr_entries = entries_per_page * (jump_page-1)
		continue
	
	
	#I thought it made the most sense use continues in the previous options, because if we tried to convert the input as an int
	#straight away, then we would have to catch the exception in the case of text options, then handle text options while also
	#testing for invalid inputs.  Doing it this way allows me to explicitly define the text-based options, and then anything else
	#will be considered an error. Also, this flows a bit better logically because the break is at the very end of the loop
	try:
		n = int(n)
	except:
		print "Your input was invalid"
		continue #we can actually just move onto the next iteration if the user gives invalid input
	
	if n not in range(1, entries_per_page+1):
		print "Your input was outside the acceptable range"
		continue
	
	chosen_entry = (item_list[((curr_page-1)*entries_per_page) + (n-1)]) #this looks weird, but its because of all the math we have to do to get to the correct spot in the list
	url = chosen_entry['url']
	title = chosen_entry['title']
	print "Downloading episode: ", title
	file_name = url.split("/")[-1] #the file name will be the same as the original mp3
	if not os.path.isfile(file_name): #if we haven't already downloaded the file, download it. otherwise, we can play it straight away
		page = urllib.urlopen(url) #to handle redirects
		url = page.geturl()
		f = urllib.URLopener()
		f.retrieve(url, file_name) #downloads the file
	os_play_mp3(file_name) #plays the file
	break #once the person makes their selection, the loop can be broken