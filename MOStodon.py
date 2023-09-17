from mastodon import Mastodon
import re
from html.parser import HTMLParser
from io import StringIO
import textwrap
from datetime import datetime, timezone, timedelta
import socket
import os
from _thread import *
from funct import *
from anyascii import anyascii


#Add MOStodon app access token and Mastodon instance between Quotes !!!!!!!!!!!!!!!!!!!!!
########################################################################

mastodon = Mastodon(access_token = "",
api_base_url = "")

########################################################################

#DEFINE LISTENING HOST AND PORT
MOStodon = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
MOStodon.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
host = '' # leave empty for Server IP. Does not need to be set. 
port = 6502 # you can change the incoming port to any desired


#	Customize the Client	#

displayname_color = "pink"
time_color = "purple"
text_color = "lightblue"
alt_text_color = "cyan"
main_menu_color = "purple"
secondary_menu_color = "blue"
notification_color = "red"
boosted_displayname_color = "orange"
interaction_color = "red"	# Favourites Boosts Replies

'''
Colors to choose from.

white
red
green
blue
orange
black
brown
pink
dark gray
gray
lightgreen
lightblue
lightgrey
purple
yellow
cyan

'''




########################################################################
UsersCount = 0
user_id = mastodon.account_verify_credentials()
yourname = "@" + user_id["acct"]
user_id = user_id["id"]
notify_id = datetime.now(timezone.utc)

tl = "h"
home_tl = ""
local_tl = ""
federated_tl = ""
user_tl = ""
other_tl = ""
account_id=""
return_page_tl="h"
home_x = 0
local_x = 0
federated_x = 0
user_x = 0
other_x = 0
pinned = False
other_page = False
notification_loop = 0
previous_home_tl_old=""
previous_home_tl_temp=""
previous_home_x=0

previous_local_tl_old=""
previous_local_tl_temp=""
previous_local_x=0

previous_federated_tl_old=""
previous_federated_tl_temp=""
previous_federated_x=0

previous_user_tl_old=""
previous_user_tl_temp=""
previous_user_x=0

previous_other_tl_old=""
previous_other_tl_temp=""
previous_other_x=0

timeline_h = ""
timeline_l = ""
timeline_f = ""
timeline_y = ""

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(connection, html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def deEmojify(connection, text):
    regrex_pattern = re.compile("["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                u"\U00002702-\U000027B0"
                u"\U000024C2-\U0001F251"
                u"\U0001f926-\U0001f937"
                u'\U00010000-\U0010ffff'
                u"\u200d"
                u"\u2640-\u2642"
                u"\u2600-\u2B55"
                u"\u23cf"
                u"\u23e9"
                u"\u231a"
                u"\u3030"
                u"\ufe0f"
    "]+", flags=re.UNICODE)
    return regrex_pattern.sub(r'\b',text)

def toot(connection):
	global secondary_menu_color
	global text_color
	global notification_color
	global user_id
	choice_exit = False
	connection.send(b'\x13') #clear
	connection.send(b'\x93') #home
	send_cr(connection, secondary_menu_color)
	send_ln(connection, "Press (")
	connection.send(b'\x05') #white
	send_ln(connection, "t")
	send_cr(connection, secondary_menu_color)
	send_ln(connection, ") for a normal Toot.\n\n")
	send_ln(connection, "Press (")
	connection.send(b'\x05') #white
	send_ln(connection, "p")
	send_cr(connection, secondary_menu_color)
	send_ln(connection, ") for a private direct message.\nIf you already know their\n")
	connection.send(b'\x05') #white
	send_ln(connection, "@username")
	send_cr(connection, "pink") 
	send_ln(connection, "@server.com\n\n")
	send_cr(connection, secondary_menu_color)
	send_ln(connection, "Press (")
	connection.send(b'\x05') #white
	send_ln(connection, "1")
	send_cr(connection, secondary_menu_color)
	send_ln(connection, ") to search people you follow.\nThen send a Direct Message.\n\n")
	send_ln(connection, "Press (")
	connection.send(b'\x05') #white
	send_ln(connection, "2")
	send_cr(connection, secondary_menu_color)
	send_ln(connection, ") to search people who follow \nyou. Then send a Direct Message.\n\n")
	send_ln(connection, "Press (")
	connection.send(b'\x05') #white
	send_ln(connection, "x")
	send_cr(connection, secondary_menu_color)
	send_ln(connection, ") to exit.\n\n")
	send_cr(connection, "black")
	choice = get_char(connection)
	
	if choice == "t":
		connection.send(b'\x13') #clear
		connection.send(b'\x93') #home
		send_cr(connection, secondary_menu_color)
		send_ln(connection,"Don't forget to add any usernames.\n")
		send_ln(connection,"e.g. @somebody@instance.com\n")
		send_ln(connection,"You should only need @somebody if they\n")
		send_ln(connection,"are on the same instance as you.\n\n")
		send_cr(connection, notification_color)
		send_ln(connection,"Enter Toot..\n\n")
		send_cr(connection, text_color)
		toot = input_line(connection)
		try: #in case message was left blank..
			mastodon.status_post(toot)
		except:
			return

	
	if choice == "p":
		connection.send(b'\x13') #clear
		connection.send(b'\x93') #home
		send_cr(connection, secondary_menu_color)
		send_ln(connection, "Add the full username of the person\n")
		send_ln(connection, "you are messaging.\n\n")
		send_ln(connection, "e.g.  @somebody@instance.com \n")
		send_ln(connection, "You should only need @somebody if they\n")
		send_ln(connection, "are on the same instance as you.\n\n")
		send_cr(connection, notification_color)
		send_ln(connection,"Enter Direct Message..\n\n")
		send_cr(connection, text_color)
		toot = input_line(connection)
		try:
			mastodon.status_post(toot,visibility="direct")
		except:
			return
	
	
	if choice == "1": #following
		choice_exit = False
		connection.send(b'\x13') #clear
		connection.send(b'\x93') #home
		send_cr(connection, "white")
		send_ln(connection, "Remember the Followers Number!\n")
		following = mastodon.account_following(user_id,limit=80) #Loads up to 80. Most instances default to 80 per api page.
		x=0
		y=0
		for follow in following:
			print(str(x+1) + " " + following[x]["display_name"])
			connection.send(b'\x05') #white
			send_ln(connection, str(x+1) + " ")
			displayname= following[x]["display_name"]
			displayname = re.sub(r':.*:','',displayname)  
			displayname = deEmojify(connection ,displayname)
			displayname = anyascii(str(displayname))
			if len(displayname) == 1 or len(displayname) == 0 :
				displayname = following[x]["username"]
			username = "@" + following[x]["acct"]
			send_cr(connection, "pink")
			send_ln(connection, displayname + " ")
			send_cr(connection, text_color)
			send_ln(connection, username + "\n")
			if y==12:				
				send_cr(connection, text_color)
				send_ln(connection, "\nPress ")
				connection.send(b'\x05') #white
				send_ln(connection, "Space ") 
				send_cr(connection, text_color)
				send_ln(connection, "for next..\n(")
				connection.send(b'\x05') #white
				send_ln(connection, "e")
				send_cr(connection, text_color)
				send_ln(connection, ") to Enter choice. (")
				connection.send(b'\x05') #white
				send_ln(connection, "x")
				send_cr(connection, text_color)
				send_ln(connection, ") to Return.\n")
				send_cr(connection, "black")
				choice = get_char(connection)
				if choice == "x":
					return
				if choice == "e":
					choice_exit = True
					break
				connection.send(b'\x13') #clear
				connection.send(b'\x93') #home
				y=0
				x+=1
			else:
				x+=1
				y+=1
		#end of first page..
		if choice_exit == True:
			pass
		elif choice_exit == False:
			send_cr(connection, text_color)
			send_ln(connection, "\nPress ")
			connection.send(b'\x05') #white
			send_ln(connection, "Space ") 
			send_cr(connection, text_color)
			send_ln(connection, "for next..\n(")
			connection.send(b'\x05') #white
			send_ln(connection, "e")
			send_cr(connection, text_color)
			send_ln(connection, ") to Enter choice. (")
			connection.send(b'\x05') #white
			send_ln(connection, "x")
			send_cr(connection, text_color)
			send_ln(connection, ") to Return.\n")
			send_cr(connection, "black")
			choice = get_char(connection)
		if choice == "x":
			return
		if choice == "e":
			choice_exit = True
		if choice_exit == True:
			
			connection.send(b'\x13') #clear
			connection.send(b'\x93') #home
			connection.send(b'\x05') #white
			send_ln(connection, "Enter User's Number.\n\n")
			try: #prevents crash if invalid nubmer was entered.
				choice = int(input_line(connection))-1
				follower_username = following[choice]["acct"]
				follower_username = "@"+ follower_username
				send_cr(connection, secondary_menu_color)
				send_ln(connection, "Enter Direct Message.\nUsername automatically added.\n\n")
				send_cr(connection, text_color)
				message = input_line(connection)
				message = follower_username + " " + message
				mastodon.status_post(message,visibility="direct")
				return
			except:
				connection.send(b'\x13') #clear
				connection.send(b'\x93') #home
				connection.send(b'\x05') #white
				send_ln(connection, "Error.\nPress any key to Return.")
				get_char(connection)
				return
		
		#next page. If more than 80 it will load and continue to load the next pages.
		while True:
			connection.send(b'\x13') #clear
			connection.send(b'\x93') #home
			print("Next Page")
			if choice_exit == True:
				break	
			try:
				x=0
				y=0
				following = mastodon.fetch_next(following)
				for follow in following:
					print(str(x+1) + " " + following[x]["display_name"])
					connection.send(b'\x05') #white
					send_ln(connection, str(x+1) + " ")
					displayname= following[x]["display_name"]
					displayname = re.sub(r':.*:','',displayname)  
					displayname = deEmojify(connection ,displayname)
					displayname = anyascii(str(displayname))
					if len(displayname) == 1 or len(displayname) == 0 :
						displayname = following[x]["username"]
					username = "@" + following[x]["acct"]
					send_cr(connection, "pink")
					send_ln(connection, displayname + " ")
					send_cr(connection, text_color)
					send_ln(connection, username + "\n")
					
					if y==10:
						send_cr(connection, text_color)
						send_ln(connection, "\nPress ")
						connection.send(b'\x05') #white
						send_ln(connection, "Space ") 
						send_cr(connection, text_color)
						send_ln(connection, "for next..\n(")
						connection.send(b'\x05') #white
						send_ln(connection, "e")
						send_cr(connection, text_color)
						send_ln(connection, ") to Enter choice. (")
						connection.send(b'\x05') #white
						send_ln(connection, "x")
						send_cr(connection, text_color)
						send_ln(connection, ") to Return.\n")
						send_cr(connection, "black")
						choice = get_char(connection)
						if choice == "x":
							return
						if choice == "e":
							choice_exit = True
							break
						connection.send(b'\x13') #clear
						connection.send(b'\x93') #home
						y=0
						x+=1
					else:
						x+=1
						y+=1
			
				if choice_exit == True:
					pass
				elif choice_exit == False:
					send_cr(connection, text_color)
					send_ln(connection, "\nPress ")
					connection.send(b'\x05') #white
					send_ln(connection, "Space ") 
					send_cr(connection, text_color)
					send_ln(connection, "for next..\n(")
					connection.send(b'\x05') #white
					send_ln(connection, "e")
					send_cr(connection, text_color)
					send_ln(connection, ") to Enter choice. (")
					connection.send(b'\x05') #white
					send_ln(connection, "x")
					send_cr(connection, text_color)
					send_ln(connection, ") to Return.\n")
					send_cr(connection, "black")
					choice = get_char(connection)
				if choice == "x":
					return
				if choice == "e":
					choice_exit = True
				
				if choice_exit == True:
			
					connection.send(b'\x13') #clear
					connection.send(b'\x93') #home
					connection.send(b'\x05') #white
					send_ln(connection, "Enter User's Number.\n\n")
					try:
						choice = int(input_line(connection))-1
						follower_username = following[choice]["acct"]
						follower_username = "@"+ follower_username
						send_cr(connection, secondary_menu_color)
						send_ln(connection, "Enter Direct Message.\nUsername automatically added.\n\n")
						send_cr(connection, text_color)
						message = input_line(connection)
						message = follower_username + " " + message
						mastodon.status_post(message,visibility="direct")
						return
					except:
						connection.send(b'\x13') #clear
						connection.send(b'\x93') #home
						connection.send(b'\x05') #white
						send_ln(connection, "Error.\nPress any key to Return.")
						get_char(connection)
						return
			
			except:
				return
	
			connection.send(b'\x13') #clear
			connection.send(b'\x93') #home
			connection.send(b'\x05') #white
			send_ln(connection, "End of list.\nPress any key to Return.")
			get_char(connection)
			return
	
	

	if choice == "2": #following
		choice_exit = False
		connection.send(b'\x13') #clear
		connection.send(b'\x93') #home
		send_cr(connection, "white")
		send_ln(connection, "Remember the Followers Number!\n")
		followers = mastodon.account_followers(user_id,limit=80)
		x=0
		y=0
		for follow in followers:
			print(str(x+1) + " " + followers[x]["display_name"])
			connection.send(b'\x05') #white
			send_ln(connection, str(x+1) + " ")
			displayname= followers[x]["display_name"]
			displayname = re.sub(r':.*:','',displayname)  
			displayname = deEmojify(connection ,displayname)
			displayname = anyascii(str(displayname))
			if len(displayname) == 1 or len(displayname) == 0 :
				displayname = followers[x]["username"]
			username = "@" + followers[x]["acct"]
			send_cr(connection, "pink")
			send_ln(connection, displayname + " ")
			send_cr(connection, text_color)
			send_ln(connection, username + "\n")
			if y==12:
				send_cr(connection, text_color)
				send_ln(connection, "\nPress ")
				connection.send(b'\x05') #white
				send_ln(connection, "Space ") 
				send_cr(connection, text_color)
				send_ln(connection, "for next..\n(")
				connection.send(b'\x05') #white
				send_ln(connection, "e")
				send_cr(connection, text_color)
				send_ln(connection, ") to Enter choice. (")
				connection.send(b'\x05') #white
				send_ln(connection, "x")
				send_cr(connection, text_color)
				send_ln(connection, ") to Return.\n")
				send_cr(connection, "black")
				choice = get_char(connection)
				if choice == "x":
					return
				if choice == "e":
					choice_exit = True
					break
				connection.send(b'\x13') #clear
				connection.send(b'\x93') #home
				y=0
				x+=1
			else:
				x+=1
				y+=1
		#end of first page..
		if choice_exit == True:
			pass
			
		elif choice_exit == False:
			send_cr(connection, text_color)
			send_ln(connection, "\nPress ")
			connection.send(b'\x05') #white
			send_ln(connection, "Space ") 
			send_cr(connection, text_color)
			send_ln(connection, "for next..\n(")
			connection.send(b'\x05') #white
			send_ln(connection, "e")
			send_cr(connection, text_color)
			send_ln(connection, ") to Enter choice. (")
			connection.send(b'\x05') #white
			send_ln(connection, "x")
			send_cr(connection, text_color)
			send_ln(connection, ") to Return.\n")
			send_cr(connection, "black")
			choice = get_char(connection)
		
		if choice == "x":
			return
		if choice == "e":
			choice_exit = True
			
		if choice_exit == True:
			
			connection.send(b'\x13') #clear
			connection.send(b'\x93') #home
			connection.send(b'\x05') #white
			send_ln(connection, "Enter User's Number.\n\n")
			try: #prevents crash if invalid nubmer was entered.
				choice = int(input_line(connection))-1
				follower_username = followers[choice]["acct"]
				follower_username = "@"+ follower_username
				send_cr(connection, secondary_menu_color)
				send_ln(connection, "Enter Direct Message.\nUsername automatically added.\n\n")
				send_cr(connection, text_color)
				message = input_line(connection)
				message = follower_username + " " + message
				mastodon.status_post(message,visibility="direct")
				return
			except:
				connection.send(b'\x13') #clear
				connection.send(b'\x93') #home
				connection.send(b'\x05') #white
				send_ln(connection, "Error.\nPress any key to Return.")
				get_char(connection)
				return
		
		#next page
		while True:
			connection.send(b'\x13') #clear
			connection.send(b'\x93') #home
			print("Next Page")
			if choice_exit == True:
				break	
			try:
				x=0
				y=0
				followers = mastodon.fetch_next(followers)
				for follow in followers:
					print(str(x+1) + " " + followers[x]["display_name"])
					connection.send(b'\x05') #white
					send_ln(connection, str(x+1) + " ")
					displayname= followers[x]["display_name"]
					displayname = re.sub(r':.*:','',displayname)  
					displayname = deEmojify(connection ,displayname)
					displayname = anyascii(str(displayname))
					if len(displayname) == 1 or len(displayname) == 0 :
						displayname = followers[x]["username"]
					username = "@" + followers[x]["acct"]
					send_cr(connection, "pink")
					send_ln(connection, displayname + " ")
					send_cr(connection, text_color)
					send_ln(connection, username + "\n")
					
					if y==10:
						send_cr(connection, text_color)
						send_ln(connection, "\nPress ")
						connection.send(b'\x05') #white
						send_ln(connection, "Space ") 
						send_cr(connection, text_color)
						send_ln(connection, "for next..\n(")
						connection.send(b'\x05') #white
						send_ln(connection, "e")
						send_cr(connection, text_color)
						send_ln(connection, ") to Enter choice. (")
						connection.send(b'\x05') #white
						send_ln(connection, "x")
						send_cr(connection, text_color)
						send_ln(connection, ") to Return.\n")
						send_cr(connection, "black")
						choice = get_char(connection)
						if choice == "x":
							return
						if choice == "e":
							choice_exit = True
							break
						connection.send(b'\x13') #clear
						connection.send(b'\x93') #home
						y=0
						x+=1
					else:
						x+=1
						y+=1
				
				if choice_exit == True:
					pass
				elif choice_exit == False:
					send_cr(connection, text_color)
					send_ln(connection, "\nPress ")
					connection.send(b'\x05') #white
					send_ln(connection, "Space ") 
					send_cr(connection, text_color)
					send_ln(connection, "for next..\n(")
					connection.send(b'\x05') #white
					send_ln(connection, "e")
					send_cr(connection, text_color)
					send_ln(connection, ") to Enter choice. (")
					connection.send(b'\x05') #white
					send_ln(connection, "x")
					send_cr(connection, text_color)
					send_ln(connection, ") to Return.\n")
					send_cr(connection, "black")
					choice = get_char(connection)
				if choice == "x":
					return
				if choice == "e":
					choice_exit = True
				
				if choice_exit == True:
			
					connection.send(b'\x13') #clear
					connection.send(b'\x93') #home
					connection.send(b'\x05') #white
					send_ln(connection, "Enter User's Number.\n\n")
					try:
						choice = int(input_line(connection))-1
						follower_username = followers[choice]["acct"]
						follower_username = "@"+ follower_username
						send_cr(connection, secondary_menu_color)
						send_ln(connection, "Enter Direct Message.\nUsername automatically added.\n\n")
						send_cr(connection, text_color)
						message = input_line(connection)
						message = follower_username + " " + message
						mastodon.status_post(message,visibility="direct")
						return
					except:
						connection.send(b'\x13') #clear
						connection.send(b'\x93') #home
						connection.send(b'\x05') #white
						send_ln(connection, "Error.\nPress any key to Return.")
						get_char(connection)
						return
			
			except:
				return
	
			connection.send(b'\x13') #clear
			connection.send(b'\x93') #home
			connection.send(b'\x05') #white
			send_ln(connection, "End of list.\nPress any key to Return.")
			get_char(connection)
			return




def search(connection):
	global secondary_menu_color
	global text_color
	global notification_color
	global tl
	global other_tl
	global return_page_tl
	global user_id
	choice_exit = False
	other_tl = "" 
	return_page_tl = tl
	connection.send(b'\x13') #clear
	connection.send(b'\x93') #home
	send_cr(connection, secondary_menu_color)
	send_ln(connection, "Press (")
	connection.send(b'\x05') #white
	send_ln(connection, "1")
	send_cr(connection, secondary_menu_color)
	send_ln(connection, ") to search people you follow.\n\n")
	send_ln(connection, "Press (")
	connection.send(b'\x05') #white
	send_ln(connection, "2")
	send_cr(connection, secondary_menu_color)
	send_ln(connection, ") to search people who follow \nyou.\n\n")
	send_ln(connection, "Press (")
	connection.send(b'\x05') #white
	send_ln(connection, "3")
	send_cr(connection, secondary_menu_color)
	send_ln(connection, ") to search for people using\ntheir username.\n\n")
	send_ln(connection, "Press (")
	connection.send(b'\x05') #white
	send_ln(connection, "x")
	send_cr(connection, secondary_menu_color)
	send_ln(connection, ") to exit.\n\n")
	send_cr(connection, "black")
	choice = get_char(connection)
	
	
	if choice == "1": #following
		choice_exit = False
		connection.send(b'\x13') #clear
		connection.send(b'\x93') #home
		send_cr(connection, "white")
		send_ln(connection, "Remember the Followers Number!\n")
		following = mastodon.account_following(user_id,limit=80)
		x=0
		y=0
		for follow in following:
			print(str(x+1) + " " + following[x]["display_name"])
			connection.send(b'\x05') #white
			send_ln(connection, str(x+1) + " ")
			displayname= following[x]["display_name"]
			displayname = re.sub(r':.*:','',displayname)  
			displayname = deEmojify(connection ,displayname)
			displayname = anyascii(str(displayname))		
			if len(displayname) == 1 or len(displayname) == 0:
				displayname = following[x]["username"]
			username = "@" + following[x]["acct"]
			send_cr(connection, "pink")
			send_ln(connection, displayname + " ")
			send_cr(connection, text_color)
			send_ln(connection, username + "\n")
			if y==10:			
				send_cr(connection, text_color)
				send_ln(connection, "\nPress ")
				connection.send(b'\x05') #white
				send_ln(connection, "Space ")
				send_cr(connection, text_color)
				send_ln(connection, "for next..\n(")
				connection.send(b'\x05') #white
				send_ln(connection, "e")
				send_cr(connection, text_color)
				send_ln(connection, ") to Enter choice. (")
				connection.send(b'\x05') #white
				send_ln(connection, "x")
				send_cr(connection, text_color)
				send_ln(connection, ") to Return.\n")
				send_cr(connection, "black")
				choice = get_char(connection)
				if choice == "x":
					return
				if choice == "e":
					choice_exit = True
					break
				connection.send(b'\x13') #clear
				connection.send(b'\x93') #home
				y=0
				x+=1
			else:
				x+=1
				y+=1
		if choice_exit == True:
			pass
		elif choice_exit == False:
			send_cr(connection, text_color)
			send_ln(connection, "\nPress ")
			connection.send(b'\x05') #white
			send_ln(connection, "Space ")
			send_cr(connection, text_color)
			send_ln(connection, "for next..\n(")
			connection.send(b'\x05') #white
			send_ln(connection, "e")
			send_cr(connection, text_color)
			send_ln(connection, ") to Enter choice. (")
			connection.send(b'\x05') #white
			send_ln(connection, "x")
			send_cr(connection, text_color)
			send_ln(connection, ") to Return.\n")
			send_cr(connection, "black")
			choice = get_char(connection)
		if choice == "x":
			return
		if choice == "e":
			choice_exit = True
		if choice_exit == True:			
			connection.send(b'\x13') #clear
			connection.send(b'\x93') #home
			connection.send(b'\x05') #white
			send_ln(connection, "Enter User's Number.\n\n")
		try:
			choice = int(input_line(connection))-1
			account_id = following[choice]["id"]
			timeline = mastodon.account_statuses(account_id,exclude_reblogs=True,limit=1,max_id=datetime.now(timezone.utc)) 
			user_page(connection,timeline[0])
			return
		except:
				connection.send(b'\x13') #clear
				connection.send(b'\x93') #home
				connection.send(b'\x05') #white
				send_ln(connection, "Error.\nPress any key to Return.")
				get_char(connection)
				return
		
		while True:
			connection.send(b'\x13') #clear
			connection.send(b'\x93') #home
			print("Next Page")
			if choice_exit == True:
				break	
			try:
				x=0
				y=0
				following = mastodon.fetch_next(following)
				for follow in following:
					print(str(x+1) + " " + following[x]["display_name"])
					connection.send(b'\x05') #white
					send_ln(connection, str(x+1) + " ")
					displayname= following[x]["display_name"]
					displayname = re.sub(r':.*:','',displayname)  
					displayname = deEmojify(connection ,displayname)
					displayname = anyascii(str(displayname))
					if len(displayname) == 1 or len(displayname) == 0 :
						displayname = following[x]["username"]
					username = "@" + following[x]["acct"]
					send_cr(connection, "pink")
					send_ln(connection, displayname + " ")
					send_cr(connection, text_color)
					send_ln(connection, username + "\n")
					
					if y==10:
						send_cr(connection, text_color)
						send_ln(connection, "\nPress ")
						connection.send(b'\x05') #white
						send_ln(connection, "Space ")
						send_cr(connection, text_color)
						send_ln(connection, "for next..\n(")
						connection.send(b'\x05') #white
						send_ln(connection, "e")
						send_cr(connection, text_color)
						send_ln(connection, ") to Enter choice. (")
						connection.send(b'\x05') #white
						send_ln(connection, "x")
						send_cr(connection, text_color)
						send_ln(connection, ") to Return.\n")
						send_cr(connection, "black")
						choice = get_char(connection)
						if choice == "x":
							return
						if choice == "e":
							choice_exit = True
							break
						connection.send(b'\x13') #clear
						connection.send(b'\x93') #home
						y=0
						x+=1
					else:
						x+=1
						y+=1
				if choice_exit == True:
					pass
				elif choice_exit == False:
					send_cr(connection, text_color)
					send_ln(connection, "\nPress ")
					connection.send(b'\x05') #white
					send_ln(connection, "Space ")
					send_cr(connection, text_color)
					send_ln(connection, "for next..\n(")
					connection.send(b'\x05') #white
					send_ln(connection, "e")
					send_cr(connection, text_color)
					send_ln(connection, ") to Enter choice. (")
					connection.send(b'\x05') #white
					send_ln(connection, "x")
					send_cr(connection, text_color)
					send_ln(connection, ") to Return.\n")
					send_cr(connection, "black")
					choice = get_char(connection)
				if choice == "x":
					return
				if choice == "e":
					choice_exit = True
				
				if choice_exit == True:
			
					connection.send(b'\x13') #clear
					connection.send(b'\x93') #home
					connection.send(b'\x05') #white
					send_ln(connection, "Enter User's Number.\n\n")
					try:
						choice = int(input_line(connection))-1
						account_id = following[choice]["id"]
						timeline = mastodon.account_statuses(account_id,exclude_reblogs=True,limit=1,max_id=datetime.now(timezone.utc))
						user_page(connection,timeline[0])
						return
					except:
						connection.send(b'\x13') #clear
						connection.send(b'\x93') #home
						connection.send(b'\x05') #white
						send_ln(connection, "Error.\nPress any key to Return.")
						get_char(connection)
						return
			
			except:
				return

		connection.send(b'\x13') #clear
		connection.send(b'\x93') #home
		connection.send(b'\x05') #white
		send_ln(connection, "End of list.\nPress any key to Return.")
		get_char(connection)
		return


	if choice == "2": #following
		choice_exit = False
		connection.send(b'\x13') #clear
		connection.send(b'\x93') #home
		send_cr(connection, "white")
		send_ln(connection, "Remember the Followers Number!\n")
		followers = mastodon.account_followers(user_id,limit=80)
		x=0
		y=0
		for follow in followers:
			print(str(x+1) + " " + followers[x]["display_name"])
			connection.send(b'\x05') #white
			send_ln(connection, str(x+1) + " ")
			displayname= followers[x]["display_name"]
			displayname = re.sub(r':.*:','',displayname)  
			displayname = deEmojify(connection ,displayname)
			displayname = anyascii(str(displayname))
			if len(displayname) == 1 or len(displayname) == 0 :
				displayname = followers[x]["username"]
			username = "@" + followers[x]["acct"]
			send_cr(connection, "pink")
			send_ln(connection, displayname + " ")
			send_cr(connection, text_color)
			send_ln(connection, username + "\n")
			if y==10:
				send_cr(connection, text_color)
				send_ln(connection, "\nPress ")
				connection.send(b'\x05') #white
				send_ln(connection, "Space ")
				send_cr(connection, text_color)
				send_ln(connection, "for next..\n(")
				connection.send(b'\x05') #white
				send_ln(connection, "e")
				send_cr(connection, text_color)
				send_ln(connection, ") to Enter choice. (")
				connection.send(b'\x05') #white
				send_ln(connection, "x")
				send_cr(connection, text_color)
				send_ln(connection, ") to Return.\n")
				send_cr(connection, "black")
				choice = get_char(connection)
				if choice == "x":
					return
				if choice == "e":
					choice_exit = True
					break
				connection.send(b'\x13') #clear
				connection.send(b'\x93') #home
				y=0
				x+=1
			else:
				x+=1
				y+=1

		if choice_exit == True:
			pass
		elif choice_exit == False:
			send_cr(connection, text_color)
			send_ln(connection, "\nPress ")
			connection.send(b'\x05') #white
			send_ln(connection, "Space ")
			send_cr(connection, text_color)
			send_ln(connection, "for next..\n(")
			connection.send(b'\x05') #white
			send_ln(connection, "e")
			send_cr(connection, text_color)
			send_ln(connection, ") to Enter choice. (")
			connection.send(b'\x05') #white
			send_ln(connection, "x")
			send_cr(connection, text_color)
			send_ln(connection, ") to Return.\n")
			send_cr(connection, "black")
			choice = get_char(connection)
		if choice == "x":
			return
		if choice == "e":
			choice_exit = True
		if choice_exit == True:			
			connection.send(b'\x13') #clear
			connection.send(b'\x93') #home
			connection.send(b'\x05') #white
			send_ln(connection, "Enter User's Number.\n\n")
			try:
				choice = int(input_line(connection))-1
				account_id = followers[choice]["id"]
				timeline = mastodon.account_statuses(account_id,exclude_reblogs=True,limit=1,max_id=datetime.now(timezone.utc))
				user_page(connection,timeline[0])
				return
			except:
				connection.send(b'\x13') #clear
				connection.send(b'\x93') #home
				connection.send(b'\x05') #white
				send_ln(connection, "Error.\nPress any key to Return.")
				get_char(connection)
				return
		

		while True:
			connection.send(b'\x13') #clear
			connection.send(b'\x93') #home
			print("Next Page")
			if choice_exit == True:
				break	
			try:
				x=0
				y=0
				followers = mastodon.fetch_next(followers)
				for follow in followers:
					print(str(x+1) + " " + followers[x]["display_name"])
					connection.send(b'\x05') #white
					send_ln(connection, str(x+1) + " ")
					displayname= followers[x]["display_name"]
					displayname = re.sub(r':.*:','',displayname)  
					displayname = deEmojify(connection ,displayname)
					displayname = anyascii(str(displayname))
					if len(displayname) == 1 or len(displayname) == 0 :
						displayname = followers[x]["username"]
					username = "@" + followers[x]["acct"]
					send_cr(connection, "pink")
					send_ln(connection, displayname + " ")
					send_cr(connection, text_color)
					send_ln(connection, username + "\n")
					
					if y==10:
						send_cr(connection, text_color)
						send_ln(connection, "\nPress ")
						connection.send(b'\x05') #white
						send_ln(connection, "Space ")
						send_cr(connection, text_color)
						send_ln(connection, "for next..\n(")
						connection.send(b'\x05') #white
						send_ln(connection, "e")
						send_cr(connection, text_color)
						send_ln(connection, ") to Enter choice. (")
						connection.send(b'\x05') #white
						send_ln(connection, "x")
						send_cr(connection, text_color)
						send_ln(connection, ") to Return.\n")
						send_cr(connection, "black")
						choice = get_char(connection)
						if choice == "x":
							return
						if choice == "e":
							choice_exit = True
							break
						connection.send(b'\x13') #clear
						connection.send(b'\x93') #home
						y=0
						x+=1
					else:
						x+=1
						y+=1
			
				if choice_exit == True:
					pass
				elif choice_exit == False:
					send_cr(connection, text_color)
					send_ln(connection, "\nPress ")
					connection.send(b'\x05') #white
					send_ln(connection, "Space ")
					send_cr(connection, text_color)
					send_ln(connection, "for next..\n(")
					connection.send(b'\x05') #white
					send_ln(connection, "e")
					send_cr(connection, text_color)
					send_ln(connection, ") to Enter choice. (")
					connection.send(b'\x05') #white
					send_ln(connection, "x")
					send_cr(connection, text_color)
					send_ln(connection, ") to Return.\n")
					send_cr(connection, "black")
					choice = get_char(connection)

				if choice == "x":
					return
				if choice == "e":
					choice_exit = True
				
				if choice_exit == True:
			
					connection.send(b'\x13') #clear
					connection.send(b'\x93') #home
					connection.send(b'\x05') #white
					send_ln(connection, "Enter User's Number.\n\n")
					try:
						choice = int(input_line(connection))-1
						account_id = followers[choice]["id"]
						timeline = mastodon.account_statuses(account_id,exclude_reblogs=True,limit=1,max_id=datetime.now(timezone.utc))
						user_page(connection,timeline[0])
						return
					except:
						connection.send(b'\x13') #clear
						connection.send(b'\x93') #home
						connection.send(b'\x05') #white
						send_ln(connection, "Error.\nPress any key to Return.")
						get_char(connection)
						return
			
			except:
				return
		connection.send(b'\x13') #clear
		connection.send(b'\x93') #home
		connection.send(b'\x05') #white
		send_ln(connection, "End of list.\nPress any key to Return.")
		get_char(connection)
		return		



	if choice == "3":
		connection.send(b'\x13') #clear
		connection.send(b'\x93') #home
		send_cr(connection, secondary_menu_color)
		send_ln(connection, "Enter username. ")
		connection.send(b'\x05') #white
		send_ln(connection, "someone")
		send_cr(connection, "pink")
		send_ln(connection, "@someserver.com\n")
		send_cr(connection, secondary_menu_color)
		send_ln(connection, "Or just ")
		connection.send(b'\x05') #white
		send_ln(connection, "someone\n\n")
		connection.send(b'\x05') #white
		send_ln(connection, "Rembember user number!!\n")
		send_cr(connection, secondary_menu_color)
		send_ln(connection, "Enter (")
		connection.send(b'\x05') #white
		send_ln(connection, "x")
		send_cr(connection, secondary_menu_color)
		send_ln(connection, ") to exit.\n\n")
		while True:
			connection.send(b'\x05') #white
			choice = input_line(connection)
			if choice == "x":
				return
			else:
				user_id = mastodon.account_search(choice)
				if user_id:
					x=0
					y=0
					for s in user_id:
						print(str(x+1) + " " + user_id[x]["display_name"])
						connection.send(b'\x05') #white
						send_ln(connection, str(x+1) + " ")
						account_id = user_id[x]["id"]
						displayname= user_id[x]["display_name"]
						displayname = re.sub(r':.*:','',displayname)  
						displayname = deEmojify(connection ,displayname)
						displayname = anyascii(str(displayname))
						username = "@" + user_id[x]["acct"]
						send_cr(connection, "pink")
						send_ln(connection, displayname + " ")
						send_cr(connection, text_color)
						send_ln(connection, username + "\n")
			
						if y==10:
							connection.send(b'\x05') #white
							send_ln(connection, "\nPress any key..")
							send_cr(connection, "black")
							choice = get_char(connection)
							connection.send(b'\x13') #clear
							connection.send(b'\x93') #home
							if choice == "x":
								return
							if choice == "e":
								choice_exit = True
								break
							y=0
							x+=1
						else:
							x+=1
							y+=1
					if choice_exit == True:
						break		
				else:
					send_cr(connection, secondary_menu_color)
					send_ln(connection, "No user found.\n")
					connection.send(b'\x05') #white
					send_ln(connection, "Press any key to Return.")
					get_char(connection)
					return
							

		connection.send(b'\x13') #clear
		connection.send(b'\x93') #home
		connection.send(b'\x05') #white
		send_ln(connection, "Enter User's Number.\n\n")
		try:
			choice = int(input_line(connection))-1
			account_id = user_id[choice]["id"]
			timeline = mastodon.account_statuses(account_id,exclude_reblogs=True,limit=1,max_id=datetime.now(timezone.utc))			
			user_page(connection,timeline[0])
			return
		except:
			connection.send(b'\x13') #clear
			connection.send(b'\x93') #home
			connection.send(b'\x05') #white
			send_ln(connection, "Error.\nPress any key to Return.")
			get_char(connection)
			return
				

	


def time_posted(connection, view_time):
		global time_color		
		sec =  int(view_time.total_seconds())
		minute = int(sec / 60)
		hour = int(sec / (60 * 60))
		days= int(view_time.days)
		weeks = int(days / 7)
		months = int(weeks / 4)
		if sec < 60:
			Time = str(sec) + " Secs "
			print(Time)
			connection.send(b'\x05') #white
			send_ln(connection,"  " + str(sec))
			send_cr(connection, time_color)
			send_ln(connection, " Secs")
			return 
		if sec >= 60 and minute < 2:
			Time = "1 Min "
			print(Time)
			connection.send(b'\x05') #white
			send_ln(connection, "  1 ")
			send_cr(connection, time_color)
			send_ln(connection, " Min")
			return 
			
		if minute > 1 and minute < 60:
			Time = str(minute) + " Mins "
			print(Time)
			connection.send(b'\x05') #white
			send_ln(connection, "  " + str(minute))
			send_cr(connection, time_color)
			send_ln(connection,  " Mins")
			return #time
			
		if minute > 60 and minute < 120:
			Time = str(hour) + " Hour "
			print(Time)
			connection.send(b'\x05') #white
			send_ln(connection, "  " + str(hour))
			send_cr(connection, time_color)
			send_ln(connection,  " Hour")
			return 
			
		if hour > 1 and hour < 24:
			Time = str(hour) + " Hours "
			print(Time)
			connection.send(b'\x05') #white
			send_ln(connection,  "  " + str(hour))
			send_cr(connection, time_color)
			send_ln(connection, " Hours")
			return 
			
		if  days < 2 :
			Time = str(days) + " Day "
			print(Time)
			connection.send(b'\x05') #white
			send_ln(connection, "  1")
			send_cr(connection, time_color)
			send_ln(connection, " Day")	
			return 
				
		if  days < 7:
			Time = str(days) + " Days "
			print(Time)
			connection.send(b'\x05') #white
			send_ln(connection, "  " + str(days))
			send_cr(connection, time_color)
			send_ln(connection, " Days")
			return 
	
		if days < 14:
			Time = " 1 Week "
			print(Time)
			connection.send(b'\x05') #white
			send_ln(connection, "  1")
			send_cr(connection, time_color)
			send_ln(connection, " Week")
			return 
			
		if weeks < 5:
			Time = str(weeks) + " Weeks "
			print(Time)
			connection.send(b'\x05') #white
			send_ln(connection, "  " + str(weeks))
			send_cr(connection, time_color)
			send_ln(connection, " Weeks")
			return 
		
		if weeks <9:
			Time = "1 Month "
			print(Time)
			connection.send(b'\x05') #white
			send_ln(connection,  "  1 ")
			send_cr(connection, time_color)
			send_ln(connection, "Month")
			return 
		
		if months < 12:
			Time = str(months) + " Months "
			print(Time)
			connection.send(b'\x05') #white
			send_ln(connection, "  " + str(months))
			send_cr(connection, time_color)
			send_ln(connection, " Months")
			return 
			
		if months >= 12 and months < 24:
			Time = "1 Year "
			print(Time)
			connection.send(b'\x05') #white
			send_ln(connection, "  1")
			send_cr(connection, time_color)
			send_ln(connection, " Year")
			return 
			
		if months >24:
			year = int(days/365)
			Time = str(year) + " Years "
			print(Time)
			connection.send(b'\x05') #white
			send_ln(connection, "  " + str(year))
			send_cr(connection, time_color)
			send_ln(connection, " Years")
			return 	


def parse_contentNotifications(connection, notify):
	content = notify['status']["content"]
	content = re.sub(r'<br>', '\n', content)
	content = re.sub(r'<br />', '\n', content)
	content = re.sub(r'<p>', '\n', content)
	content = re.sub(r"£","lll" ,content)
	content = re.sub(r"lll","£" ,content)
	content = strip_tags(connection, content)
	content = deEmojify(connection, content)
	content = anyascii(str(content))
	favourites = notify["status"]["favourites_count"]
	replies = notify["status"]["replies_count"]
	boosts = notify["status"]["reblogs_count"]
	
	if notify["status"]["media_attachments"]:
		media = notify["status"]["media_attachments"]
		alt_text = media[0]["description"]
		media_type = media[0]["type"]
		if media_type == "image":
			media_type = "\nPosted a Picture\n"
		if media_type == "video":
			media_type = "\nPosted a Video\n"
		if media_type == "gifv":
			media_type = "\nPosted a GIF\n"
		if media_type == "audio":
			media_type = "\nPosted Audio\n"
		if media_type == "unknown":
			media_type = "\nPosted Unknown\n"
		if alt_text == None:
			pass
		else:	
			alt_text = "Alt Text - \n" + alt_text
			alt_text = strip_tags(connection, alt_text)
			alt_text = deEmojify(connection, alt_text)
			alt_text = anyascii(str(alt_text)) 
	else:
		media_type = None
		alt_text = None

	if media_type:
		if content == None:
			content = media_type
		else:
			content = content + "\n" + media_type 
		
	if alt_text:
		content = content +  alt_text
							
	return content, favourites, replies, boosts, media_type

def parse_content(connection, text):
	content = re.sub(r'<br>', '\n', text)
	content = re.sub(r'<br />', '\n', content)
	content = re.sub(r'<p>', '\n', content)
	content = re.sub(r"£","lll" ,content)
	content = re.sub(r"lll","£" ,content)
	content = strip_tags(connection, content)
	content = deEmojify(connection, content)
	content = anyascii(str(content))	
	return content		
			
def new_notifications(connection):
	global notify_id
	global notification_color
	notify = mastodon.notifications(limit = 1)			
	last_notify = notify[0]['created_at']
	if  last_notify > notify_id:
		print("New notification !!!                  ")
		connection.send(b'\x07') 
		send_cr(connection, notification_color)
		cursorxy(connection,1,21)
		new_notification = "         New Notification !!!         "
		send_cr(connection, "revon")
		send_ln(connection, new_notification)
		send_cr(connection, "revoff")
		send_cr(connection, "black")
	
			
def notifications(connection):
	global notify_id
	global displayname_color
	global text_color
	global secondary_menu_color
	global other_page
	global tl
	global return_page_tl
	time_now = datetime.now(timezone.utc)
	notify_id = time_now #Clears the new notification alert
	notify = mastodon.notifications(limit = 40)
	length = len(notify)
	y = 0
	exit_from = False	
	while True:
		if y == length:
			break
		notify_time = notify[y]['created_at']
		view_time = time_now - notify_time
		account_id = notify[y]["account"]["id"]
		displayname = notify[y]['account']['display_name']
		displayname = re.sub(r':.*:','',displayname)
		displayname = deEmojify(connection, displayname)
		displayname = anyascii(str(displayname))
		username = "@" + notify[y]['account']['acct']
		if len(displayname) == 1 or len(displayname) == 0 :
			displayname = timeline["account"]["username"]
				
		
		if notify[y]['type'] == 'favourite':
			print("----------------------------------------------------\n")
			print(displayname + " Favourited  " )		
			content,favourites,replies, boosts, media_type = parse_contentNotifications(connection, notify[y]) 
			is_boosted=False
			connection.send(b'\x13') #clear
			connection.send(b'\x93') #home
			send_cr(connection, displayname_color)
			send_ln(connection, displayname)
			time_posted(connection, view_time)
			send_cr(connection, displayname_color)
			send_ln(connection, "\n" + username)
			send_cr(connection, "white")
			send_ln(connection, "\n\nFavourited your Toot\n\n")
			send_cr(connection, text_color)
			do_print(connection,content,is_boosted)
			interaction = interactions(connection, favourites,replies,boosts)	
			cursorxy(connection,1,23)
			send_cr(connection, secondary_menu_color)
			send_ln(connection, "              (")
			send_cr(connection, "white")
			send_ln(connection, "i")
			send_cr(connection, secondary_menu_color)
			send_ln(connection, ")nteract")
			send_cr(connection, "black")
			
			
		if notify[y]['type'] == 'mention':
			print(displayname + " Mentioned " )			
			content,favourites,replies, boosts, media_type = parse_contentNotifications(connection, notify[y])					
			is_boosted=False		
			connection.send(b'\x13') #clear
			connection.send(b'\x93') #home
			send_cr(connection, displayname_color)
			send_ln(connection, displayname)			
			time_posted(connection, view_time)
			send_cr(connection, displayname_color)
			send_ln(connection, "\n" + username)			
			send_cr(connection, "white")
			send_ln(connection, "\n\nMentioned you\n\n")
			send_cr(connection, text_color)
			do_print(connection, content,is_boosted)			
			interaction = interactions(connection, favourites,replies,boosts)					
			send_cr(connection, secondary_menu_color)
			cursorxy(connection,1,23)
			send_ln(connection, "      Fa(")
			connection.send(b'\x05') #white
			send_ln(connection, "v")
			send_cr(connection, secondary_menu_color)
			send_ln(connection, ") (")
			connection.send(b'\x05') #white
			send_ln(connection, "r")
			send_cr(connection, secondary_menu_color)
			send_ln(connection, ")eply (")
			connection.send(b'\x05') #white
			send_ln(connection,"i")
			send_cr(connection, secondary_menu_color)
			send_ln(connection, ")nteract")
			send_cr(connection, "black")
			
		if notify[y]['type'] == 'reblog':
			print(displayname + " Boosted " )					
			content,favourites,replies, boosts, media_type = parse_contentNotifications(connection, notify[y])			
			connection.send(b'\x13') #clear
			connection.send(b'\x93') #home
			send_cr(connection, displayname_color)
			send_ln(connection, displayname)			
			time_posted(connection, view_time)
			send_cr(connection, displayname_color)
			send_ln(connection, "\n" + username)			
			send_cr(connection, "white")
			send_ln(connection, "\n\nBoosted your Toot\n\n")
			send_cr(connection, text_color)					
			do_print(connection, content,is_boosted=False)
			interaction = interactions(connection, favourites,replies,boosts)
			cursorxy(connection,1,23)
			send_cr(connection, secondary_menu_color)
			send_ln(connection, "              (")
			send_cr(connection, "white")
			send_ln(connection, "i")
			send_cr(connection, secondary_menu_color)
			send_ln(connection, ")nteract")
			send_cr(connection, "black")
			
		if notify[y]['type'] == 'follow':
			print(displayname + " Followed you")
			connection.send(b'\x13') #clear
			connection.send(b'\x93') #home
			send_cr(connection, displayname_color)
			send_ln(connection, displayname)		
			time_posted(connection, view_time)
			send_cr(connection, displayname_color)
			send_ln(connection, "\n" + username)			
			send_cr(connection, "white")
			send_ln(connection, "\n\nFollowed You")
			cursorxy(connection,1,23)
			send_cr(connection, secondary_menu_color)
			send_ln(connection, "              (")
			send_cr(connection, "white")
			send_ln(connection, "i")
			send_cr(connection, secondary_menu_color)
			send_ln(connection, ")nteract")
			send_cr(connection, "black")
			
		if notify[y]['type'] == 'follow_request':
			print(displayname + " Wants to follow you ")
			connection.send(b'\x13') #clear
			connection.send(b'\x93') #home	
			send_cr(connection, displayname_color)
			send_ln(connection, displayname)			
			time_posted(connection, view_time)
			send_cr(connection, displayname_color)
			send_ln(connection, "\n" + username)			
			send_cr(connection, "white")
			send_ln(connection, "\n\nWant's to Follow you.")	
			cursorxy(connection,1,23)
			send_cr(connection, secondary_menu_color)
			send_ln(connection, "   (")
			send_cr(connection, "white")
			send_ln(connection, "i")
			send_cr(connection, secondary_menu_color)
			send_ln(connection, ")nteract (")
			send_cr(connection, "white")
			send_ln(connection, "a")
			send_cr(connection, secondary_menu_color)
			send_ln(connection, ")uthorize request")
			send_cr(connection, "black")
				
		send_cr(connection, secondary_menu_color)
		cursorxy(connection,1,24)
		connection.send(b'\x05') #white
		send_ln(connection, "     Space ")
		send_cr(connection, secondary_menu_color)
		send_ln(connection, "for next notification.\n")
		send_ln(connection, "    (")
		connection.send(b'\x05') #white
		send_ln(connection, "x")
		send_cr(connection, secondary_menu_color)
		send_ln(connection, ") to exit back to timeline.")
		send_cr(connection, "black")
		
		while True:
					
			choice = get_char(connection)
			if choice == "a" and notify[y]['type'] == 'follow_request':
				try:
					mastodon.follow_request_authorize(account_id)
					cursorxy(connection,1,22)
					connection.send(b'\x05') #white
					send_ln(connection, "Follow request approved...")
					send_cr(connection, "black")
					connection.send(b'\x07')
				except:
					pass
				
			if choice == "i":
				if other_page == False:
					return_page_tl = tl
				
				timeline = mastodon.account_statuses(account_id,exclude_reblogs=True,limit=1,max_id=datetime.now(timezone.utc))				
				user_page(connection,timeline[0]) 
				if other_page == True:
					return
				else:
					y-=1
					break
					
			if choice == "x":
				exit_from = True
				break
			
			if choice == "v" and notify[y]['type'] == 'mention':
				try:
					mastodon.status_favourite(notify[y]["status"]["id"])
					cursorxy(connection,1,22)
					connection.send(b'\x05') #white
					send_ln(connection, "You Favourited this Toot !           ")
					send_cr(connection, "black")
					connection.send(b'\x07')
				except:
					pass
					
			if choice == "r" and notify[y]['type'] == 'mention':
				connection.send(b'\x13') #home
				connection.send(b'\x93') #clear
				connection.send(b'\x05') #white
				send_ln(connection, "Usernames are automatically added to\n")
				send_ln(connection,  "reply..\n\n")
				send_ln(connection, "Enter Reply...\n")
				send_cr(connection, text_color)
				reply = input_line(connection)
				try:
					mastodon.status_reply(notify[y]["status"],reply,in_reply_to_id=notify[y]["status"]["id"])
				except:
					pass
				y-=1
				break
			if choice == " ":			
				break
		if exit_from == True:
			return
		else:		
			y+=1
			
	
	connection.send(b'\x13') #clear
	connection.send(b'\x93') #home
	send_cr(connection, "white")
	send_ln(connection, "   End of retrieved Notifications.\n")
	send_ln(connection, " Press any key to return to timeline.")
	send_cr(connection, "black")
	get_char(connection)
	print("\n\n---------------------------------------------------------")
	return


def interactions(connection, favourites,replies,boosts):
	global interaction_color
	if interactions:
		send_ln(connection, "\n")
	if favourites == 0:
		favourites_out = ""
	elif favourites == 1:
		favourites_out = "1 Favourite "
		send_cr(connection, "white")
		send_ln(connection, "1 ")
		send_cr(connection, interaction_color)
		send_ln(connection, "Favourite ")
	else:
		favourites_out = str(favourites) + " Favourites "
		send_cr(connection, "white")
		send_ln(connection, str(favourites))
		send_cr(connection, interaction_color)
		send_ln(connection, " Favourites ")
		
	if replies == 0:
		replies_out = ""
	elif replies == 1:
		replies_out = "1 Reply "
		send_cr(connection, "white")
		send_ln(connection, "1 ")
		send_cr(connection, interaction_color)
		send_ln(connection, "Reply ")	
	else:
		print(str(replies) + "  Replies ")
		replies_out = str(replies) + " Replies "
		send_cr(connection, "white")
		send_ln(connection, str(replies))
		send_cr(connection, interaction_color)
		send_ln(connection, " Replies ")

	if boosts == 0:
		boosts_out = ""
	elif boosts == 1:
		boosts_out = "1 Boost"
		send_cr(connection, "white")
		send_ln(connection, "1 ")
		send_cr(connection, interaction_color)
		send_ln(connection, "Boost ")
		
	else:
		boosts_out = str(boosts) + " Boosts"
		send_cr(connection, "white")
		send_ln(connection, str(boosts))
		send_cr(connection, interaction_color)
		send_ln(connection, " Boosts ")
	
	
def get_content(connection, timeline):
	time_now = datetime.now(timezone.utc)
	created_at= timeline["created_at"]
	view_time = time_now - created_at		
	displayname = timeline["account"]["display_name"]
	displayname = re.sub(r':.*:','',displayname)  
	displayname = deEmojify(connection, displayname)
	displayname = anyascii(str(displayname))
	username = "@" + timeline["account"]["acct"]
	if len(displayname) == 1 or len(displayname) == 0 :
		displayname = timeline["account"]["username"]

	favourites = timeline["favourites_count"]
	replies = timeline["replies_count"]
	boosts = timeline["reblogs_count"]		
	content = timeline["content"]
	content = re.sub(r'<br>', '\n', content)
	content = re.sub(r'<br />', '\n', content)
	content = re.sub(r'</p>', '\n', content)
	content = re.sub(r"£","lll" ,content)
	content = strip_tags(connection, content)
	content = deEmojify(connection, content)	
	content = anyascii(str(content))
	content = re.sub(r"lll","£" ,content)
	boosted = timeline["reblog"]	
			
	if timeline["media_attachments"]:
		media = timeline["media_attachments"]
		alt_text = media[0]["description"]
		media_type = media[0]["type"]
		if media_type == "image":
			media_type = "Posted a Picture"
		if media_type == "video":
			media_type = "Posted a Video"
		if media_type == "gifv":
			media_type = "Posted a GIF"
		if media_type == "audio":
			media_type = "Posted Audio"
		if media_type == "unknown":
			media_type = "Posted Unknown" 
						
		if alt_text == None:
			pass
		else:			
			alt_text = "Alt Text - \n" + alt_text
			alt_text = strip_tags(connection, alt_text)
			alt_text = deEmojify(connection, alt_text)
			alt_text = anyascii(str(alt_text))	

	else:
		alt_text = None
		media_type = None

	return view_time,displayname,username,favourites,replies,boosts,content,boosted,alt_text,media_type


def do_print(connection,content,is_boosted):
	global text_color
	global alt_text_color
	global pinned
	x=0
	if is_boosted == True:
		x = 3
	elif pinned == True:
		x+=2

	alt=False
	lines = content.split("\n")
	lists = (textwrap.TextWrapper(width=38).wrap(line) for line in lines)
	body = "\n".join("\n".join(list) for list in lists)
	print(body)
	lines = body.splitlines()
	for line in lines:
		if line.startswith("Posted a Picture") or line.startswith("Posted a Video") or line.startswith("Posted a GIF") or line.startswith("Posted Unknown"):
			send_cr(connection, "cyan")
			x+=2
			length = len(line)
			for loop in range(1):
				for i in range(length):
					send_ln(connection, line[i])
				send_ln(connection, "\n")
				
		elif line.startswith("Alt Text -"):
			x+=2
			alt= True
			send_ln(connection, "\n")
			send_cr(connection, "yellow")
			for loop in range(1):
				send_ln(connection, line + "\n")
							
			send_ln(connection, "\n")
			send_cr(connection, alt_text_color)

		else:
			words = line.split(" ")
			for word in words:
				if re.findall(r'^#', word) or re.findall(r'^@', word):
					send_cr(connection, "red")
					send_ln(connection, word + " ")
					
				else:
					if alt==False:
						send_cr(connection, text_color)
						send_ln(connection, word + " ")
					else:
						send_cr(connection, alt_text_color)
						send_ln(connection, word + " ")
						
			send_ln(connection, "\n")
		
		if x >= 17:
			send_cr(connection, "white")
			send_ln(connection, "\nPress any key for next page")
			send_cr(connection, "black")
			get_char(connection)
			if alt==True:
				send_cr(connection, alt_text_color)
			else:
				send_cr(connection, text_color)
			
			connection.send(b'\x13') #clear
			connection.send(b'\x93') #home
			x=0
		x+=1


def messages(connection):
	global notification_color
	global text_color
	global displayname_color
	global text_color
	global main_menu_color
	global secondary_menu_color
	global other_page
	global tl
	global return_page_tl
	time_now =  datetime.now(timezone.utc)
	conv = mastodon.conversations(limit=40)
	length = len(conv)
	y=0 
	z=1 
	favourited = False
	replied = False
	while True:
		if y == length:
			break
		id = conv[y]["last_status"]["id"] #id of message 
		connection.send(b'\x13') #clear
		connection.send(b'\x93') #home
		message_num = str(z)
		conv_id = conv[y]["id"]
		unread = conv[y]["unread"]
		if unread == True:
			print("Unread Message")
			send_cr(connection, notification_color)
			send_cr(connection, "revon")
			send_ln(connection, "Unread Message\n")
			send_cr(connection, "revoff")
			mastodon.conversations_read(conv_id)
		
		accounts = conv[y]["last_status"]["account"] #id of message sender
		accounts_id = conv[y]["last_status"]
		account_id = conv[y]["accounts"][0]["id"] #id of people in the message?
		displayname = accounts["display_name"]
		username = "@" + accounts["acct"]
		
		if len(displayname) == 1 or len(displayname) == 0 :
			displayname = timeline["account"]["username"]
		
		print("---------------------------------------------------------\n")
		print(displayname)
		print(username)
		displayname = re.sub(r':.*:','',displayname)  
		displayname = deEmojify(connection, displayname)
		displayname = anyascii(str(displayname))
		created_at = conv[y]["last_status"]["created_at"]
		view_time = time_now - created_at
		last_status= conv[y]["last_status"]
		content = last_status["content"]
		content = parse_content(connection,content)
		send_cr(connection, displayname_color)
		send_ln(connection, displayname)
		time_posted(connection,view_time )
		send_cr(connection, displayname_color)
		send_ln(connection, "\n" + username)
		send_ln(connection, "\n\n")
		send_cr(connection, text_color)
		do_print(connection, content,is_boosted=False)
		
		if favourited == True:
			cursorxy(connection,1,20)
			send_cr(connection, notification_color)
			send_ln(connection, "You Favourited this Message!")
			favourited = False
			connection.send(b'\x07')
			
		if replied == True:
			cursorxy(connection,1,20)
			send_cr(connection, notification_color)
			send_ln(connection, "You replied to this Message!")
			replied = False
			connection.send(b'\x07')
			
		cursorxy(connection,1,21)
		send_cr(connection, notification_color)
		send_ln(connection, "Message ")
		connection.send(b'\x05') #white
		send_ln(connection, message_num)
		send_ln(connection,"\n")
		send_cr(connection, secondary_menu_color)
		send_ln(connection, "(")
		connection.send(b'\x05') #white
		send_ln(connection, "r")
		send_cr(connection, secondary_menu_color)
		send_ln(connection, ")eply to message fa(")
		connection.send(b'\x05') #white
		send_ln(connection, "v")
		send_cr(connection, secondary_menu_color)
		send_ln(connection, ")ourite message\n") 		
		send_ln(connection, "(")
		connection.send(b'\x05') #white
		send_ln(connection, "s")
		send_cr(connection, secondary_menu_color)
		send_ln(connection, ")how previous replies (")
		connection.send(b'\x05') #white
		send_ln(connection, "i")
		send_cr(connection, secondary_menu_color)
		send_ln(connection, ")nteract\n")
		send_ln(connection, "(")
		connection.send(b'\x05') #white
		send_ln(connection, "x")
		send_cr(connection, secondary_menu_color)
		send_ln(connection, ") to exit back to Timeline\n")
		send_ln(connection, "      Press ")
		connection.send(b'\x05') #white
		send_ln(connection, "Space ")
		send_cr(connection, secondary_menu_color)
		send_ln(connection, "for next Message")		
		send_cr(connection, "black")

		choice = get_char(connection)
		if choice == "i":
			if other_page == False:
				return_page_tl = tl 

			timeline = mastodon.account_statuses(account_id,exclude_reblogs=True,limit=1,max_id=datetime.now(timezone.utc))
			user_page(connection,timeline[0]) 
			if other_page == True:
				return
			else:
				y-=1
				z-=1
		
		if choice == "x":
			return
		
		if choice == "v":
			try:
				mastodon.status_favourite(id)
				y-=1
				z-=1	
				favourited = True
			except:
				y-=1
				z-=1	
					
		if choice == "r":
			connection.send(b'\x13') #clear
			connection.send(b'\x93') #home
			send_cr(connection, "white")
			send_ln(connection, "Usernames are automatically added to\n")
			send_ln(connection, "reply..\n\n")
			send_ln(connection, "Enter Reply\n\n")
			send_cr(connection, text_color)
			reply = input_line(connection)
			try:
				mastodon.status_reply(to_status=accounts_id, status=reply, in_reply_to_id=conv_id) #replies are direct by default
				replied = True
			except:
				pass
			y-=1
			z-=1
			#replied = True
		if choice == "s":
			replies = mastodon.status_context(accounts_id)
			past = replies["ancestors"]
			lengthl = len(past)
			l = 0
			for l in range(lengthl):
				time_now = datetime.now(timezone.utc)
				send_cr(connection, displayname_color)
				accounts = past[l]
				created_at = past[l]["created_at"]
				view_time = time_now - created_at	
				displayname = accounts["account"]["display_name"]
				print(displayname)
				content = past[l]["content"]
				content = parse_content(connection, content)
				connection.send(b'\x13') #clear
				connection.send(b'\x93') #home
				send_cr(connection, displayname_color)
				send_ln(connection, displayname)
				time_posted(connection,view_time)
				send_ln(connection, "\n\n")
				send_cr(connection, text_color)
				do_print(connection, content,is_boosted = False)				
				send_cr(connection, main_menu_color)
				cursorxy(connection,1,23)
				send_ln(connection, "      Press ")
				send_cr(connection, "white")
				send_ln(connection, "space ")
				send_cr(connection, main_menu_color)
				send_ln(connection, "for next reply\n")
				send_ln(connection, "    Press (")
				send_cr(connection, "white")
				send_ln(connection, "x") 
				send_cr(connection, main_menu_color)
				send_ln(connection, ") to return to Message.")
				send_cr(connection, "black")
				choice = get_char(connection)
				if choice == "x":
					break
				else:
					l+=1

			connection.send(b'\x13') #clear
			connection.send(b'\x93') #home
			send_cr(connection, "white")
			send_ln(connection, "        End of replies.\n")
			send_ln(connection, "Press any key to return to message.")
			send_cr(connection, "black")
			get_char(connection)
		
			y-=1 
			z-=1
				
		
		y+=1
		z+=1
	print("\n\n")
		
	connection.send(b'\x13') #clear
	connection.send(b'\x93') #home
	send_cr(connection, "white")
	send_ln(connection, "       End of retrieved Messages.\n")
	send_ln(connection, "  Press any key to return to timeline.")
	send_cr(connection, "black")
	get_char(connection)
	return



def user_page(connection,timeline): #currently uses a users post, reply, etc to get Account ID and other info. Should pass in the Account ID instead of Post in case the user has never posted to their timeline. 
	global tl
	global other_page
	global account_id
	global displayname_color
	global text_color
	global secondary_menu_color
	global notification_color
	global other_x
	other_x = 0
	account_id_temp = timeline["account"]["id"]
	print("account id " + str(account_id_temp))
	following_check = mastodon.account_relationships(account_id_temp)
	following_user = following_check[0]["following"]
	followed_by = following_check[0]["followed_by"]
	displayname = timeline["account"]["display_name"]
	displayname = re.sub(r':.*:','',displayname)  
	displayname = deEmojify(connection ,displayname)
	displayname = anyascii(str(displayname))	
	username = "@" + timeline["account"]["acct"]
	if len(displayname) == 1 or len(displayname) == 0 :
		displayname = timeline["account"]["username"]
	
	note = timeline["account"]["note"]
	note = re.sub(r'<br>', '\n', note)
	note = re.sub(r'<br />', '\n', note)
	note = re.sub(r'</p>', '\n', note)
	note = re.sub(r"£","lll" ,note)
	note = strip_tags(connection, note)
	note = deEmojify(connection, note)	
	note = anyascii(str(note))
	content = note + "\n\n"
	following = timeline["account"]["following_count"]
	followers = timeline["account"]["followers_count"]
	print(displayname)
	print(username)
	connection.send(b'\x13') #home
	connection.send(b'\x93') #clear
	send_cr(connection, displayname_color)
	send_ln(connection, displayname+"\n")
	send_ln(connection, username+"\n\n")
	do_print(connection,note,is_boosted=False)
	send_ln(connection, "\n")
	connection.send(b'\x05') #white
	send_ln(connection, "Press any key")
	send_cr(connection, "black")
	get_char(connection)
	connection.send(b'\x13') #home
	connection.send(b'\x93') #clear
	print()
	fields = timeline["account"]["fields"]
	x=0
	for field in fields:
		name = field["name"]
		print(name)
		send_cr(connection,"white")
		send_ln(connection, name+"\n")	
		value = field["value"]
		value = strip_tags(connection,value)
		value = deEmojify(connection,value)	
		value = anyascii(str(value))
		send_cr(connection,text_color)
		do_print(connection,value,is_boosted=False)
		content = content + value
		send_ln(connection, "\n")
		x+=1
	print()
	print("Following- " + str(following) + " Followers- " + str(followers))
	print()
	send_cr(connection, notification_color)
	send_ln(connection, "Following- ")
	connection.send(b'\x05') #white
	send_ln(connection, str(following))
	send_cr(connection, notification_color)
	send_ln(connection, "    Followers- ")
	connection.send(b'\x05') #white
	send_ln(connection, str(followers))
	send_ln(connection, "\n\n")
	
	
	if following_user == True and followed_by == False:
		send_ln(connection, "You follow them.")
		print("You follow them.")
		
	if following_user == False and followed_by == True:
		send_ln(connection, "They follow you.")
		print("They follow you.")
		
	if following_user == True and followed_by == True:
		send_ln(connection, "You follow each other.")
		print("You follow each other.")
		
	if following_user == False and followed_by == False:
		send_ln(connection, "You don't follow them.")
		print("You don't follow them.")
			
	cursorxy(connection,1,23)
	send_cr(connection, secondary_menu_color)
	send_ln(connection, "     (")
	connection.send(b'\x05') #white
	send_ln(connection, "f")
	send_cr(connection, secondary_menu_color)
	send_ln(connection, ")ollow (")
	connection.send(b'\x05') #white
	send_ln(connection, "u")
	send_cr(connection, secondary_menu_color)
	send_ln(connection, ")nfollow (")
	connection.send(b'\x05') #white
	send_ln(connection, "n")
	send_cr(connection, secondary_menu_color)
	send_ln(connection, ")otify\n")
	send_ln(connection, "     (")
	connection.send(b'\x05') #white
	send_ln(connection, "d")
	send_cr(connection, secondary_menu_color)
	send_ln(connection, ")irect message (")
	connection.send(b'\x05') #white
	send_ln(connection, "x")
	send_cr(connection, secondary_menu_color)
	send_ln(connection, ") return\n")
	connection.send(b'\x05') #white
	send_ln(connection, "        Space ")
	send_cr(connection, secondary_menu_color)
	send_ln(connection, "to view posts")
	send_cr(connection, "black")
	
	while True:
		print("in the while true")
		choice = get_char(connection)
		if choice == "f":
			try:
				mastodon.account_follow(account_id_temp,reblogs=True,notify=False)
				cursorxy(connection,1,22)
				send_cr(connection, "white")
				send_ln(connection, "You Followed them!")
				send_cr(connection, "black")
				connection.send(b'\x07')
			except:
				pass
			
		if choice == "u":
			try:
				mastodon.account_unfollow(account_id_temp)
				cursorxy(connection,1,22)
				send_cr(connection, "white")
				send_ln(connection, "You Unfollowed them!")
				send_cr(connection, "black")
				connection.send(b'\x07')
			except:
				pass
			
		if choice == "n":
			try:
				mastodon.account_follow(account_id_temp,reblogs=True,notify=True)
				cursorxy(connection,1,22)
				send_cr(connection, "white")
				send_ln(connection, "You will recieve notifications.")
				send_cr(connection, "black")
				connection.send(b'\x07')
			except:
				pass
			
		if choice == "d":
			connection.send(b'\x13') #home
			connection.send(b'\x93') #clear
			connection.send(b'\x05') #white
			send_ln(connection,"Username automatically added\n")
			send_ln(connection,"Enter Direct Message..\n\n")
			send_cr(connection, text_color)
			message = input_line(connection)
			message= username+ " " + message
			try:
				mastodon.status_post(message,visibility="direct")
			except:
				pass
			connection.send(b'\x13') #home
			connection.send(b'\x93') #clear
			cursorxy(connection,1,22)
			send_cr(connection, "white")
			send_ln(connection, "You messaged them!\n")
			connection.send(b'\x07')
			send_cr(connection, secondary_menu_color)
			send_ln(connection, "     (")
			connection.send(b'\x05') #white
			send_ln(connection, "f")
			send_cr(connection, secondary_menu_color)
			send_ln(connection, ")ollow (")
			connection.send(b'\x05') #white
			send_ln(connection, "u")
			send_cr(connection, secondary_menu_color)
			send_ln(connection, ")nfollow (")
			connection.send(b'\x05') #white
			send_ln(connection, "n")
			send_cr(connection, secondary_menu_color)
			send_ln(connection, ")otify\n")
			send_ln(connection, "     (")
			connection.send(b'\x05') #white
			send_ln(connection, "d")
			send_cr(connection, secondary_menu_color)
			send_ln(connection, ")irect message (")
			connection.send(b'\x05') #white
			send_ln(connection, "x")
			send_cr(connection, secondary_menu_color)
			send_ln(connection, ") return\n")
			connection.send(b'\x05') #white
			send_ln(connection, "        Space ")
			send_cr(connection, secondary_menu_color)
			send_ln(connection, "to view posts")
			send_cr(connection, "black")

		if choice == "x":
			if other_page == True:
				return
			else:
				other_tl = "" #resets other tl
			return
		if choice == " ":
			tl = "o"					
			account_id = account_id_temp #only sets account_id if you view the users posts.
			other_page = True
			return


		
def timeline(connection):
	global tl
	global account_id
	global displayname_color
	global text_color
	global main_menu_color
	global secondary_menu_color
	global home_tl
	global local_tl
	global federated_tl
	global user_tl
	global other_tl 
	global other_page
	global home_x
	global local_x
	global federated_x
	global user_x
	global other_x 
	global previous_home_tl_old
	global previous_home_tl_temp
	global previous_home_x	
	global previous_local_tl_old
	global previous_local_tl_temp
	global previous_local_x	
	global previous_federated_tl_old
	global previous_federated_tl_temp
	global previous_federated_x	
	global previous_user_tl_old
	global previous_user_tl_temp
	global previous_user_x	
	global previous_other_tl_old 
	global previous_other_tl_temp
	global previous_other_x	
	global notify_id
	global pinned
	global return_page_tl
	global notification_loop	
	global timeline_h 
	global timeline_l
	global timeline_f
	global timeline_y
	
	home_length=0
	local_length=0
	federated_length=0
	user_length=0
	other_length = 0 
	time_now = datetime.now(timezone.utc)
	pinned = False
	
	if tl == "h":
		if home_tl == "":	#first time loading the timeline	
			home_tl = time_now
			timeline_h = mastodon.timeline_home(limit=40, max_id=home_tl)
			x=0
		else: # loads the next page of posts.. timeline is first loaded at the end of the first page below..
			x=home_x #sets the proper post location
		timeline = timeline_h	#pulls timeline from memory rather than pulling from API
		home_length = len(timeline)-1

	
	if tl == "l":
		if local_tl == "":
			local_tl = time_now
			timeline_l = mastodon.timeline_local(limit=40, max_id=local_tl)
			x=0
		else:
			x=local_x
		timeline = timeline_l
		local_length = len(timeline)-1
		print()
	
	
	if tl == "f":
		if federated_tl == "":
			federated_tl = time_now
			timeline_f = mastodon.timeline_public(limit=40, max_id=federated_tl)
			x=0
		else:
			x=federated_x
		timeline = timeline_f
		federated_length = len(timeline)-1
		print()
	
	
	if tl == "y":
		if user_tl == "":
			user_tl = datetime.now(timezone.utc)#"" #first time loading homepage.
			x=user_x
			timeline_y = mastodon.account_statuses(user_id, pinned=True)
			if len(timeline_y) == 0:
				user_tl = datetime.now(timezone.utc)
				timeline_y = mastodon.account_statuses(user_id,limit=40, max_id=user_tl)
		else: # if no pinned toots or after showing all pinned toots or loading the next page of posts...
			x=user_x
		timeline = timeline_y
		user_length = len(timeline)-1

		
	if tl == "o":
		if other_tl == "": #try loading the pinned toots first.
			other_tl = time_now
			x=other_x	
			pinned = True
			timeline = mastodon.account_statuses(account_id,limit=40,pinned=True)
						
		else: #if no pinned toots or after showing the first page of posts. Doesn't save the timeline because it is changes with every use..
			x=other_x 
			pinned = False
			timeline = mastodon.account_statuses(account_id,limit=40, max_id=other_tl)
		other_length = len(timeline)-1
	
				
#################################################################################################################
	new_timeline = False 
	for i in timeline: #synchronizes the x for each timeline for loop.
		if tl == "h":
			home_x = x
		if tl == "l":
			local_x = x
		if tl == "f":
			federated_x =x
		if tl == "y":
			user_x = x
		if tl == "o":
			other_x = x
		print(x)
		
		connection.send(b'\x13') #home
		connection.send(b'\x93') #clear
		view_time,displayname,username,favourites,replies,boosts,content,boosted,alt_text,media_type = get_content(connection, timeline[x])
		id = timeline[x]["id"]		
		if boosted: 
			is_boosted = True
			print(displayname + "  BOOSTED")			
			send_cr(connection, "revon")
			send_cr(connection, boosted_displayname_color)
			send_ln(connection, displayname + " Boosted")
			send_cr(connection, "revoff")			
			time_posted(connection, view_time)
					
		else:
			is_boosted = False
			print(displayname)
			print(username)
			send_cr(connection, displayname_color)
			send_ln(connection, displayname)
			time_posted(connection, view_time)	
			send_cr(connection, displayname_color)
			send_ln(connection, "\n")
			send_ln(connection, username)
			send_ln(connection, "\n\n")

		try:
			pinned = timeline[x]["pinned"]
		except:
			pass
		if pinned == True:
			send_cr(connection, "white")
			send_ln(connection, "Pinned Toot !\n\n")
			print("pinned Toot !\n")
		
		if media_type:
			content = content + "\n" + media_type + "\n"	
		
		if alt_text:
			content = content +  alt_text
							
		else:
			alt_text == None

		do_print(connection,content,is_boosted)
		interaction = interactions(connection, favourites,replies,boosts)
			
		if boosted:
			boosted_id = boosted["id"]
			boosted_status=mastodon.status(boosted_id)
			boosted_time,boosted_displayname,boosted_username,boosted_favourites,boosted_replies,boosted_boosts,boosted_content,boosted,alt_text,media_type = get_content(connection, boosted_status)
			print(boosted_displayname)	
			send_cr(connection, displayname_color)
			send_ln(connection, "\n")		
			send_ln(connection, boosted_displayname)
			time_posted(connection, boosted_time)
			send_cr(connection, displayname_color)
			send_ln(connection, "\n")
			send_ln(connection, boosted_username)
			send_cr(connection, text_color)
			send_ln(connection, "\n\n")
			
			if media_type:
				boosted_content = boosted_content +  "\n" + media_type + "\n"
			
			if alt_text:
				boosted_content = boosted_content  + alt_text
					
			else:
				alt_text = None
										
			do_print(connection,boosted_content,is_boosted)	
			interaction = interactions(connection, boosted_favourites,boosted_replies,boosted_boosts)
			print(interaction)
		print("--------------------------------------")
		
		if other_page ==False and username != yourname: #menu for the 3 main timelines. Home, Local, Federated Normal Menu and it's not your post.
			send_cr(connection, "black")
			cursorxy(connection,1,22)
			send_cr(connection, main_menu_color)
			send_ln(connection, "fa(")
			connection.send(b'\x05') #white
			send_ln(connection, "v")
			send_cr(connection, main_menu_color)
			send_ln(connection, ") (")
			connection.send(b'\x05') #white
			send_ln(connection, "b")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")oost (")
			connection.send(b'\x05') #white
			send_ln(connection, "r")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")eply (")
			connection.send(b'\x05') #white
			send_ln(connection, "p")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")rivate reply\n")
			send_ln(connection, "(")
			connection.send(b'\x05') #white
			send_ln(connection, "s")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")how replies (")
			connection.send(b'\x05') #white
			send_ln(connection, "z")
			send_cr(connection, main_menu_color)
			send_ln(connection, ") Reload (")
			connection.send(b'\x05') #white
			send_ln(connection,"i")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")nteract\n")
			send_ln(connection, "(")
			connection.send(b'\x05') #white
			send_ln(connection, "h")
			send_cr(connection, main_menu_color)
			send_ln(connection, ") (")
			connection.send(b'\x05') #white
			send_ln(connection, "l")
			send_cr(connection, main_menu_color)
			send_ln(connection, ") (")
			connection.send(b'\x05') #white
			send_ln(connection, "f")
			send_cr(connection, main_menu_color)
			send_ln(connection, ") (")
			connection.send(b'\x05') #white
			send_ln(connection, "y")
			send_cr(connection, main_menu_color)
			send_ln(connection, ") (")
			connection.send(b'\x05') #white
			send_ln(connection, "t")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")oot (")
			connection.send(b'\x05') #white
			send_ln(connection, "n")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")otif (")
			connection.send(b'\x05') #white
			send_ln(connection, "m")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")ess\n")
			send_ln(connection, " sear(")
			connection.send(b'\x05') #white
			send_ln(connection, "c")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")h ")
			connection.send(b'\x05') #white
			send_ln(connection, "Space ")
			send_cr(connection, main_menu_color)
			send_ln(connection, "next Toot (")
			connection.send(b'\x05') #white
			send_ln(connection, "g")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")o Back")
			send_cr(connection, "black")
		
		if other_page ==False and tl != "y" and username == yourname: #menu for the 3 main timelines. Home, Local, Federated with your post.
			send_cr(connection, "black")
			cursorxy(connection,1,22)
			send_cr(connection, main_menu_color)
			send_ln(connection, "fa(")
			connection.send(b'\x05') #white
			send_ln(connection, "v")
			send_cr(connection, main_menu_color)
			send_ln(connection, ") (")
			connection.send(b'\x05') #white
			send_ln(connection, "b")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")oost (")
			connection.send(b'\x05') #white
			send_ln(connection, "r")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")eply (")
			connection.send(b'\x05') #white
			send_ln(connection, "p")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")in (")
			connection.send(b'\x05') #white
			send_ln(connection, "u")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")npin\n")
			send_ln(connection, "(")
			connection.send(b'\x05') #white
			send_ln(connection, "s")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")how replies (")
			connection.send(b'\x05') #white
			send_ln(connection, "z")
			send_cr(connection, main_menu_color)
			send_ln(connection, ") Reload (")
			connection.send(b'\x05') #white
			send_ln(connection,"i")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")nteract\n")
			send_ln(connection, "(")
			connection.send(b'\x05') #white
			send_ln(connection, "h")
			send_cr(connection, main_menu_color)
			send_ln(connection, ") (")
			connection.send(b'\x05') #white
			send_ln(connection, "l")
			send_cr(connection, main_menu_color)
			send_ln(connection, ") (")
			connection.send(b'\x05') #white
			send_ln(connection, "f")
			send_cr(connection, main_menu_color)
			send_ln(connection, ") (")
			connection.send(b'\x05') #white
			send_ln(connection, "y")
			send_cr(connection, main_menu_color)
			send_ln(connection, ") (")
			connection.send(b'\x05') #white
			send_ln(connection, "t")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")oot (")
			connection.send(b'\x05') #white
			send_ln(connection, "n")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")otif (")
			connection.send(b'\x05') #white
			send_ln(connection, "m")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")ess\n")
			send_ln(connection, " sear(")
			connection.send(b'\x05') #white
			send_ln(connection, "c")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")h ")
			connection.send(b'\x05') #white
			send_ln(connection, "Space ")
			send_cr(connection, main_menu_color)
			send_ln(connection, "next Toot (")
			connection.send(b'\x05') #white
			send_ln(connection, "g")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")o Back")
			send_cr(connection, "black")
		
		if other_page == True and yourname != username:
			send_cr(connection, "black")
			cursorxy(connection,1,22)
			send_cr(connection, secondary_menu_color)
			send_ln(connection, "fa(")
			connection.send(b'\x05') #white
			send_ln(connection, "v")
			send_cr(connection, secondary_menu_color)
			send_ln(connection, ") (")
			connection.send(b'\x05') #white
			send_ln(connection, "b")
			send_cr(connection, secondary_menu_color)
			send_ln(connection, ")oost (")
			connection.send(b'\x05') #white
			send_ln(connection, "r")
			send_cr(connection, secondary_menu_color)
			send_ln(connection, ")eply (")
			connection.send(b'\x05') #white
			send_ln(connection, "p")
			send_cr(connection, secondary_menu_color)
			send_ln(connection, ")rivate (")
			connection.send(b'\x05') #white
			send_ln(connection, "n")
			send_cr(connection, secondary_menu_color)
			send_ln(connection, ")otif\n")
			send_ln(connection, "(")
			connection.send(b'\x05') #white
			send_ln(connection, "s")
			send_cr(connection, secondary_menu_color)
			send_ln(connection, ")how replies (")
			connection.send(b'\x05') #white
			send_ln(connection, "i")
			send_cr(connection, secondary_menu_color)
			send_ln(connection, ")nteract (")			
			connection.send(b'\x05') #white
			send_ln(connection, "z")
			send_cr(connection, secondary_menu_color)
			send_ln(connection, ") Reload   \n")
			send_cr(connection, secondary_menu_color)
			send_ln(connection, " Press ")
			connection.send(b'\x05') #white
			send_ln(connection, "Space ")
			send_cr(connection, secondary_menu_color)
			send_ln(connection, "for next Toot. (")
			connection.send(b'\x05') #white
			send_ln(connection, "g")
			send_cr(connection, secondary_menu_color)
			send_ln(connection, ")o Back  \n")
			send_ln(connection, "     (")
			connection.send(b'\x05') #white
			send_ln(connection, "x")
			send_cr(connection, secondary_menu_color)
			send_ln(connection, ") to return to timeline.       ")
			send_cr(connection, "black")
		
		if tl == "y"  and is_boosted == False and username == yourname: # when viewing your own timeline and your own posts.
			send_cr(connection, "black")
			cursorxy(connection,1,22)
			send_cr(connection, main_menu_color)
			send_ln(connection, "  fa(")
			connection.send(b'\x05') #white
			send_ln(connection, "v")
			send_cr(connection, main_menu_color)
			send_ln(connection, ") (")
			connection.send(b'\x05') #white
			send_ln(connection, "b")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")oost (")
			connection.send(b'\x05') #white
			send_ln(connection, "r")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")eply (")
			connection.send(b'\x05') #white
			send_ln(connection, "p")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")in (")
			connection.send(b'\x05') #white
			send_ln(connection, "u")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")npin \n")		
			send_ln(connection, "  (")
			connection.send(b'\x05') #white
			send_ln(connection, "s")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")how replies (")
			connection.send(b'\x05') #white
			send_ln(connection, "z")
			send_cr(connection, main_menu_color)
			send_ln(connection, ") Reload")
			send_ln(connection, " sear(")
			connection.send(b'\x05') #white
			send_ln(connection, "c")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")h \n")
			send_ln(connection, "  (")
			connection.send(b'\x05') #white
			send_ln(connection, "h")
			send_cr(connection, main_menu_color)
			send_ln(connection, ") (")
			connection.send(b'\x05') #white
			send_ln(connection, "l")
			send_cr(connection, main_menu_color)
			send_ln(connection, ") (")
			connection.send(b'\x05') #white
			send_ln(connection, "f")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")")
			send_ln(connection, " (")
			connection.send(b'\x05') #white
			send_ln(connection, "t")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")oot (")
			connection.send(b'\x05') #white
			send_ln(connection, "n")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")otif (")
			connection.send(b'\x05') #white
			send_ln(connection, "m")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")ess\n")
			connection.send(b'\x05') #white
			send_ln(connection, "   Space ")
			send_cr(connection, main_menu_color)
			send_ln(connection, "next Toot (")
			connection.send(b'\x05') #white
			send_ln(connection, "g")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")o Back (")
			connection.send(b'\x05') #white
			send_ln(connection, "x")
			send_cr(connection, main_menu_color)
			send_ln(connection, ") Exit")
			send_cr(connection, "black")
			
		if tl == "y"  and is_boosted == True: # when viewing your own timeline with a boosted post.
			send_cr(connection, "black")
			cursorxy(connection,1,22)
			send_cr(connection, main_menu_color)
			send_ln(connection, "  fa(")
			connection.send(b'\x05') #white
			send_ln(connection, "v")
			send_cr(connection, main_menu_color)
			send_ln(connection, ") (")
			connection.send(b'\x05') #white
			send_ln(connection, "b")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")oost (")
			connection.send(b'\x05') #white
			send_ln(connection, "r")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")eply (")
			connection.send(b'\x05') #white
			send_ln(connection, "p")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")rivate reply")		
			send_ln(connection, "  (")
			connection.send(b'\x05') #white
			send_ln(connection, "s")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")how replies (")
			connection.send(b'\x05') #white
			send_ln(connection, "z")
			send_cr(connection, main_menu_color)
			send_ln(connection, ") Reload")
			send_ln(connection, " sear(")
			connection.send(b'\x05') #white
			send_ln(connection, "c")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")h \n")
			send_ln(connection, "(")
			connection.send(b'\x05') #white
			send_ln(connection, "h")
			send_cr(connection, main_menu_color)
			send_ln(connection, ") (")
			connection.send(b'\x05') #white
			send_ln(connection, "l")
			send_cr(connection, main_menu_color)
			send_ln(connection, ") (")
			connection.send(b'\x05') #white
			send_ln(connection, "f")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")")
			send_ln(connection, " (")
			connection.send(b'\x05') #white
			send_ln(connection, "t")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")oot (")
			connection.send(b'\x05') #white
			send_ln(connection, "n")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")otif (")
			connection.send(b'\x05') #white
			send_ln(connection, "m")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")ess (")
			connection.send(b'\x05') #white
			send_ln(connection, "i")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")nt\n")
			connection.send(b'\x05') #white
			send_ln(connection, "   Space ")
			send_cr(connection, main_menu_color)
			send_ln(connection, "next Toot (")
			connection.send(b'\x05') #white
			send_ln(connection, "g")
			send_cr(connection, main_menu_color)
			send_ln(connection, ")o Back (")
			connection.send(b'\x05') #white
			send_ln(connection, "x")
			send_cr(connection, main_menu_color)
			send_ln(connection, ") Exit")
			send_cr(connection, "black")

		
		if notification_loop == 3: #prevents querying the API every screen refresh.Cuts down on rate limiting. You can change to 1 to check for notifications every page reload.
			new_notifications(connection)	#checks for new notifications
			notification_loop = 0

		while True:	#scans the keyboard waiting for input.
			choice = get_char(connection)
			send_cr(connection, "black")
									
			if choice == "z": #Refreshes the current timeline.
				if tl=="h":
					home_tl=""
					home_x = 0
					new_timeline = True
					break
				if tl == "l":
					local_tl="" 
					local_x = 0
					new_timeline = True
					break
				if tl == "f":
					federated_tl=""
					federated_x = 0
					new_timeline = True
					break
				if tl== "y":
					user_tl=""
					user_x = 0
					new_timeline = True
					break
				if tl== "o":
					other_tl=""
					other_x = 0
					new_timeline = True
					break
				
			if choice == "c":
				if other_page == True: 
					pass
				else:
					search(connection)
					new_timeline = True
					break
				
			if choice == "t":
				toot(connection)
				break
				
			if choice == "m":				
				messages(connection)
				if other_page == True:
					new_timeline = True
					break
				else:				
					break
				
			if choice == "h":
				if other_page == True: #removes timeline switching from other peoples pages. uses x to return.
					pass
				else:
					tl = "h"
					new_timeline = True
					print()
					break
			
			if choice == "l":
				if other_page == True:
					pass
				else:
					tl = "l"
					new_timeline = True			
					print()
					break
			
			if choice == "f":
				if other_page == True:
					pass
				else:
					tl = "f"
					new_timeline = True
					print()
					break	
				
			if choice == "y": 	
				if other_page == True:
					pass
				else:
					return_page_tl = tl
					tl = "y"
					new_timeline = True
					print()
					break
			
			if choice == "i":
				if other_page == True and is_boosted == False: #doesn't set returning timeline when already interacting from an interaction. So it can return to the original location.
					user_page(connection, timeline[x])
					new_timeline = True
					break
				if other_page == True and is_boosted == True: #doesn't set returning timeline when already interacting from an interaction. So it can return to the original location.
					user_page(connection, boosted_status)
					new_timeline = True
					break
				
				if tl == "y" and is_boosted == True: # interact with people from your homepage but not yourself.
					return_page_tl = tl
					user_page(connection, boosted_status)
					new_timeline = True
					break
				if username == yourname and tl == "y" : #Don't interact with your posts while on your homepage.
					pass
				if username == yourname and tl != "y": # interact with yourself from regular timeline. Skips normal user_page function.
					return_page_tl = tl
					tl = "y"
					
					new_timeline = True
					break
					
				if other_page == False and is_boosted == False and username != yourname: #normal interaction from a main timeline.
					return_page_tl = tl 
					user_page(connection, timeline[x])
					new_timeline = True
					break
				if other_page == False and is_boosted == True and username != yourname: #normal interaction from a main timeline.
					return_page_tl = tl 
					user_page(connection, boosted_status)
					new_timeline = True
					break
				
			if choice == "n":
				notifications(connection)
				if other_page == True:
					new_timeline = True
					break
				else:					
					break
							
			
			if choice == "v":	
				try:
					mastodon.status_favourite(id)
					cursorxy(connection,1,21)
					send_cr(connection, "red")
					send_ln(connection, "You Favourited this Toot !           ")
					send_cr(connection, "black")
					connection.send(b'\x07')
				except:
					pass
			
			if choice == "b":
				try:
					mastodon.status_reblog(id)
					cursorxy(connection,1,21)
					send_cr(connection, "red")
					send_ln(connection, "You Boosted this Toot !             ")
					send_cr(connection, "black")
					connection.send(b'\x07')
				except:
					pass
			
			if choice == "r":
				if is_boosted == True:
					connection.send(b'\x13') #home
					connection.send(b'\x93') #clear
					connection.send(b'\x05') #white
					send_ln(connection, "Usernames are automatically added to\n")
					send_ln(connection, "reply..\nAll users who are tagged in the reply\nwill be added.\n")
					send_ln(connection, "Enter Reply...\n\n")
					send_cr(connection, text_color)
					reply = input_line(connection)
					try:
						mastodon.status_reply(boosted_status,reply,in_reply_to_id=boosted_id)
					except:
						pass
					break
				else:
					connection.send(b'\x13') #home
					connection.send(b'\x93') #clear
					connection.send(b'\x05') #white
					send_ln(connection, "Usernames are automatically added to\n")
					send_ln(connection, "reply..\nAll users who are tagged in the reply\nwill be added.\n")
					send_ln(connection, "Enter Reply...\n\n")
					send_cr(connection, text_color)
					reply = input_line(connection)
					try:
						mastodon.status_reply(timeline[x],reply,in_reply_to_id=id)
					except:
						pass
					break
			
			if choice == "u":
				if is_boosted == False and username == yourname:
					mastodon.status_unpin(id)
					cursorxy(connection,1,21)
					connection.send(b'\x05') #white
					send_ln(connection, "You Unpinned this Toot !              ")
					send_cr(connection, "black")
					connection.send(b'\x07')
			
			if choice == "p":
				if is_boosted == False and username == yourname:	
					mastodon.status_pin(id)
					cursorxy(connection,1,21)
					connection.send(b'\x05') #white
					send_ln(connection, "You Pinned this Toot !              ")
					send_cr(connection, "black")
					connection.send(b'\x07')
					
				if is_boosted == True:
					connection.send(b'\x13') #home
					connection.send(b'\x93') #clear
					connection.send(b'\x05') #white
					send_ln(connection, "Usernames are automatically added to\n")
					send_ln(connection, "reply..\nAll users who are tagged in the reply\nwill be added.\n")
					send_ln(connection, "Enter Reply...\n")
					send_cr(connection, text_color)
					reply = input_line(connection)
					try:
						mastodon.status_reply(boosted_status,reply,in_reply_to_id=boosted_id,visibility="direct")
					except:
						pass
					break
				else:
					connection.send(b'\x13') #home
					connection.send(b'\x93') #clear
					connection.send(b'\x05') #white
					send_ln(connection, "Usernames are automatically added to\n")
					send_ln(connection, "reply..\nAll users who are tagged in the reply\nwill be added.\n")
					send_ln(connection, "Enter Reply...\n")
					send_cr(connection, text_color)
					reply = input_line(connection)
					try:
						mastodon.status_reply(timeline[x],reply,in_reply_to_id=id,visibility="direct")
					except:
						pass
					break	
			
			if choice == "s":	#show replies..
				
				if is_boosted:
					id = boosted_id
				replies = mastodon.status_context(id)
				since = replies["descendants"]
				reply_return = False	
				length2 = len(since)
				is_boosted = False
				for s in range(length2):
					reply_id = since[s]["id"]
					to_status_id = mastodon.status(since[s]["id"])
					view_time,displayname,username,favourites,replies,boosts,content,boosted,alt_text,media_type = get_content(connection,since[s])
					print(displayname)
					print("\n\n")
					connection.send(b'\x13') #home
					connection.send(b'\x93') #clear
					send_cr(connection, displayname_color)
					send_ln(connection, displayname+"\n")
					send_ln(connection, username)
					time_posted(connection, view_time)	
					send_ln(connection, "\n\n")
					send_cr(connection, text_color)
			
					if media_type:
						content = content + "\n" + media_type + "\n"
					do_print(connection,content,is_boosted)
					interaction = interactions(connection, favourites,replies,boosts)
					cursorxy(connection,1,22)
					reply_num = s + 1
					send_cr(connection, "cyan")
					send_ln(connection, "Reply # ")
					connection.send(b'\x05') #white
					send_ln(connection, str(reply_num) + "\n")			
					send_cr(connection, secondary_menu_color)
					send_ln(connection, "Fa(")
					connection.send(b'\x05') #white
					send_ln(connection, "v")
					send_cr(connection, secondary_menu_color)
					send_ln(connection, ")ourite (")
					connection.send(b'\x05') #white
					send_ln(connection, "b")
					send_cr(connection, secondary_menu_color)
					send_ln(connection, ")oost (")
					connection.send(b'\x05') #white
					send_ln(connection, "r")
					send_cr(connection, secondary_menu_color)
					send_ln(connection, ")eply \n(")
					connection.send(b'\x05') #white
					send_ln(connection, "p")
					send_cr(connection, secondary_menu_color)
					send_ln(connection, ")rivate reply (")
					connection.send(b'\x05') #white
					send_ln(connection, "i")
					send_cr(connection, secondary_menu_color)
					send_ln(connection, ")nteract with user \n(")				
					connection.send(b'\x05') #white
					send_ln(connection, "x")
					send_cr(connection, secondary_menu_color)
					send_ln(connection, ") to exit")					
					connection.send(b'\x05') #white
					send_ln(connection, " Space ")
					send_cr(connection, secondary_menu_color)
					send_ln(connection, "for next reply.")
					send_cr(connection, "black")
					
									
					while True:
						choice = get_char(connection)
						if choice == "x":
							reply_return = True
							break

						if choice == "v":
							try:
								mastodon.status_favourite(reply_id)
								cursorxy(connection,1,21)
								send_cr(connection, "red")
								send_ln(connection, "You Favourited this Reply !")
								send_cr(connection, "black")
								connection.send(b'\x07')
							except:
								pass
							
						if choice == "b":
							try:
								mastodon.status_reblog(reply_id)
								cursorxy(connection,1,21)
								send_cr(connection, "red")
								send_ln(connection, "You Boosted this Reply !   ")
								send_cr(connection, "black")
								connection.send(b'\x07')
							except:
								pass
	
						if choice == "r":
							connection.send(b'\x13') #home
							connection.send(b'\x93') #clear
							connection.send(b'\x05') #white
							send_ln(connection, "Usernames are automatically added to\n")
							send_ln(connection, "reply..\nAll users who are tagged in the reply\nwill be added.\n\n")
							send_cr(connection, notification_color)
							send_ln(connection, "Enter Reply...\n")
							send_cr(connection, text_color)
							reply = input_line(connection)
							try:
								mastodon.status_reply(to_status= to_status_id , status=reply , in_reply_to_id=reply_id)
							except:
								pass
							send_cr(connection, "black")
							break
							
						if choice == "p":
							connection.send(b'\x13') #home
							connection.send(b'\x93') #clear
							connection.send(b'\x05') #white
							send_ln(connection, "Usernames are automatically added to\n")
							send_ln(connection, "reply..\nAll users who are tagged in the reply\nwill be added.\n")
							send_cr(connection, notification_color)
							send_ln(connection, "Enter Reply...\n")
							send_cr(connection, text_color)
							reply = input_line(connection)
							try:
								mastodon.status_reply(to_status= to_status_id , status=reply , in_reply_to_id=reply_id,visibility = "direct")
							except:
								pass
							send_cr(connection, "black")
							break 
						
						if choice == "i":	
							if other_page == True:
								user_page(connection, since[s])
								new_timeline = True
								break
							else:
					
								return_page_tl = tl
								user_page(connection, since[s])
								new_timeline = True
								reply_return = True
								break						
						
						if choice == " ":
							break						
	
					if reply_return == True:
						break
				if new_timeline ==True:
					break
				
				connection.send(b'\x13') #home
				connection.send(b'\x93') #clear
				send_cr(connection, "white")
				send_ln(connection, "         No more replies...\n")
				send_ln(connection, "Press any key to Return to Toot...")
				send_cr(connection, "black")
				get_char(connection)
				break
			
			if choice == "g":   #goes back to previous post.
				if x == 0: #used when reaching the very first post x=0 in a timeline and needs to load the previous timeline and last (x)post number.
					if tl=="h":
						home_tl=previous_home_tl_old 
						home_x=previous_home_x
						timeline_h = mastodon.timeline_home(limit=40, max_id=home_tl)
						new_timeline = True
						break
						
					if tl=="l":
						local_tl=previous_local_tl_old
						local_x=previous_local_x
						timeline_l = mastodon.timeline_local(limit=40, max_id=local_tl)
						new_timeline = True
						break
						
					if tl=="f":
						federated_tl=previous_federated_tl_old
						federated_x=previous_federated_x
						timeline_f = mastodon.timeline_public(limit=40, max_id=federated_tl)
						new_timeline = True
						break
						
					if tl=="y":
						user_tl=previous_user_tl_old
						user_x=previous_user_x
						timeline_y = mastodon.account_statuses(user_id,limit=40, max_id=user_tl) #probem here.
						new_timeline = True
						break
					
					if tl=="o": 
						other_tl=previous_other_tl_old
						other_x=previous_other_x
						new_timeline = True
						
						break
				else:
					x-=1
					break
											
			if choice == "x":# and other_page == True: #only used on others timelines in order to return to a main timeline.
				if other_page == True:
					other_tl="" #resets the timeline.	
					tl = return_page_tl #loads the timeline it was on before jumping to others timeline. 
					other_page = False
					new_timeline = True
					break
								
				if tl == "y":
					tl = return_page_tl #loads the timeline it was on before jumping to others timeline. 
					x=0
					new_timeline = True
					break
					
					
			if choice == " ": # when pressing space on a timeline.
				
				if tl == "h" and home_x == 0: #used to hold the current timeline when loading a new page.
					previous_home_tl_temp = home_tl
			
				if tl == "l" and local_x == 0:
					previous_local_tl_temp = local_tl
			
				if tl == "f" and federated_x == 0:
					previous_federated_tl_temp = federated_tl
				
				if tl == "y" and user_x == 0:
					if user_tl == "":
						previous_user_tl_temp = ""
					else:
						previous_user_tl_temp = user_tl
				
				if tl == "o" and other_x == 0:		
					if other_tl == "":
						previous_other_tl_temp = ""
					else:
						previous_other_tl_temp = other_tl
											
				
				if tl == "h" and home_length == x: #used to lock in the previous timeline when reaching the end of a timeline page. i.e. after viewing 40 comments and loading new ones.
					home_tl=timeline[x]["id"] 
					previous_home_tl_old = previous_home_tl_temp #locks in the previous temp page so it knows what to load if going back a previous timeline.
					previous_home_x = home_x 
					home_x = 0
					
					timeline_h = mastodon.timeline_home(limit=40, max_id=home_tl) #only pulls a new timeline from the API only after the end of the timeline is finished. Prevents querrying the API everytime you switch between timelines.
					new_timeline=True
					break
					
				if tl == "l" and local_length == x:
					local_tl=timeline[x]["id"]
					previous_local_tl_old = previous_local_tl_temp
					previous_local_x = local_x
					local_x = 0
					timeline_l = mastodon.timeline_local(limit=40, max_id=local_tl) 
					new_timeline=True
					break
					
				if tl == "f" and federated_length == x:
					federated_tl=timeline[x]["id"]
					previous_federated_tl_old = previous_federated_tl_temp
					previous_federated_x = federated_x
					federated_x = 0
					timeline_f = mastodon.timeline_public(limit=40, max_id=federated_tl) 
					new_timeline=True
					break

				
				if tl == "y" and user_length == x:
					if pinned == True:
						previous_user_x = user_x
						user_x = 0
						user_tl = datetime.now(timezone.utc)
						pinned = False
						timeline_y = mastodon.account_statuses(user_id,limit=40, max_id=user_tl)
						previous_user_tl_old = ""
						new_timeline=True
						break
					else:
						previous_user_x = user_x
						user_tl=timeline[x]["id"]
						user_x = 0
						timeline_y = mastodon.account_statuses(user_id,limit=40, max_id=user_tl)
						previous_user_tl_old = previous_user_tl_temp
						new_timeline=True
						break
				
				if tl == "o" and other_length == x: 
					if pinned == True:
						previous_other_x = other_x
						other_x = 0
						other_tl = datetime.now(timezone.utc)
						pinned = False
						previous_other_tl_old = ""
						new_timeline=True
						break
					else:
						previous_other_x = other_x
						other_tl=timeline[x]["id"]
						other_x = 0
						previous_other_tl_old = previous_other_tl_temp
						new_timeline=True
						break			
				
				else:
					x+=1 #advances the next timeline post.
					notification_loop+=1 
					break
			
		if new_timeline == True: #loads the new timeline you selected above. 
			break		
		print()
		
				
def run_once(connection):
	global tl
	global other_tl
	global text_color
	send_cr(connection,"clear") 
	send_cr(connection,"home")
	send_cr(connection, text_color)						   
	connection.send(b'\x05') #white
	send_ln(connection, "              MOS")
	send_cr(connection, "blue")
	send_ln(connection, "todon\n\n")	
	send_cr(connection, text_color)
	send_ln(connection, "Press ")
	send_cr(connection, text_color)
	send_ln(connection, "(")
	connection.send(b'\x05') #white
	send_ln(connection, "t")
	send_cr(connection, text_color)
	send_ln(connection, ") to post a Toot or send a\n")
	send_ln(connection, "Direct Message.\n\n")
	send_ln(connection, "Switch between timelines at anytime.\n")
	send_ln(connection, "(")
	connection.send(b'\x05') #white
	send_ln(connection, "h")
	send_cr(connection, text_color)
	send_ln(connection, ") for Home (")
	connection.send(b'\x05') #white
	send_ln(connection, "l")
	send_cr(connection, text_color)
	send_ln(connection, ") for Local\n")
	send_ln(connection, "(")
	connection.send(b'\x05') #white
	send_ln(connection, "f")
	send_cr(connection, text_color)
	send_ln(connection, ") for Federated (")
	connection.send(b'\x05') #white
	send_ln(connection, "y")
	send_cr(connection, text_color)
	send_ln(connection, ") for Your page.\n\n")
	connection.send(b'\x05') #white
	send_cr(connection, text_color)
	send_ln(connection, "Fa(")
	connection.send(b'\x05') #white
	send_ln(connection, "v")
	send_cr(connection, text_color)
	send_ln(connection, ")ourite, (")
	connection.send(b'\x05') #white
	send_ln(connection, "b")
	send_cr(connection, text_color)
	send_ln(connection, ")oost, or (")
	connection.send(b'\x05') #white
	send_ln(connection, "r")
	send_cr(connection, text_color)
	send_ln(connection, ")eply.\n")
	send_ln(connection, "You can also send (")
	connection.send(b'\x05') #white
	send_ln(connection, "p")
	send_cr(connection, text_color)
	send_ln(connection, ")rivate replies.\n(")
	connection.send(b'\x05') #white
	send_ln(connection, "s")
	send_cr(connection, text_color)
	send_ln(connection, ")how and interact with replies.\n\n")
	send_ln(connection, "(")
	connection.send(b'\x05') #white
	send_ln(connection, "g")
	send_cr(connection, text_color)
	send_ln(connection, ")o back to the previous toot.\n")
	send_ln(connection, "(")
	connection.send(b'\x05') #white
	send_ln(connection, "i")
	send_cr(connection, text_color)
	send_ln(connection, ")nteracts with the users homepage.\n(")
	connection.send(b'\x05') #white
	send_ln(connection, "z")
	send_cr(connection, text_color)
	send_ln(connection, ") reloads the timeline with\nthe newest toots.\n\n")
	send_ln(connection, "Sear(")
	connection.send(b'\x05') #white
	send_ln(connection, "c")
	send_cr(connection, text_color)
	send_ln(connection, ")h for other users.\n")  
	send_ln(connection, "(")
	connection.send(b'\x05') #white
	send_ln(connection, "n")
	send_cr(connection, text_color)
	send_ln(connection, ") will load notifications. This will\nalso clear the notification alert.\n")
	send_ln(connection, "(")
	connection.send(b'\x05') #white
	send_ln(connection, "m")
	send_cr(connection, text_color)
	send_ln(connection, ") to read your Messages.\n\n")
	connection.send(b'\x05') #white
	send_ln(connection, "Select Choice.")
	send_cr(connection, text_color)
	send_cr(connection, text_color)
	send_ln(connection, "(")
	connection.send(b'\x05') #white
	send_ln(connection, "h")
	send_cr(connection, text_color)
	send_ln(connection, ")(")
	connection.send(b'\x05') #white
	send_ln(connection, "l")
	send_cr(connection, text_color)
	send_ln(connection, ")(")
	connection.send(b'\x05') #white
	send_ln(connection, "f")
	send_cr(connection, text_color)
	send_ln(connection, ")(")
	connection.send(b'\x05') #white
	send_ln(connection, "y")
	send_cr(connection, text_color)
	send_ln(connection, ")(")
	connection.send(b'\x05') #white
	send_ln(connection, "t")
	send_cr(connection, text_color)
	send_ln(connection, ")(")
	connection.send(b'\x05') #white
	send_ln(connection, "c")
	send_cr(connection, text_color)
	send_ln(connection, ")(")
	connection.send(b'\x05') #white
	send_ln(connection, "n")
	send_cr(connection, text_color)
	send_ln(connection, ")(")
	connection.send(b'\x05') #white
	send_ln(connection, "m")
	send_cr(connection, text_color)
	send_ln(connection, ")\n")
	send_ln(connection, "or press")
	connection.send(b'\x05') #white
	send_ln(connection, " Space ")
	send_cr(connection, text_color)
	send_ln(connection, "for Home Timeline.")
	send_cr(connection, "black")
	choice = get_char(connection)
	send_ln(connection, "\n")
	print("choice selected " + choice)
	
	
	if choice == "t":
		toot(connection)
		
	if choice == "h":
		tl = "h"
		
	if choice == "l":
		tl = "l"
		
	if choice == "f":
		tl = "f"
		
	if choice == "y":
		tl = "y"
		
	if choice == "n":
		notifications(connection)

	if choice == "m":
		messages(connection)

	if choice == "c":
		search(connection)

def user_session(connection):
      send_cr(connection,"clear")
      send_cr(connection,"home")
      send_cr(connection, "blue")
      send_ln(connection, "Connected. Hit Return key...")
      bucl=input_line(connection)
      send_cr(connection,"clear")
      send_cr(connection,"home")
      send_seq(connection, "seq/MOStodon.seq")




def threaded_client(connection):
	global UsersCount
	try:
		connection.settimeout(1200) # 20 mins of inactivity will disconnect..
		user_session(connection)
		run_once(connection)
		while True:
			timeline(connection)

	except Exception:
		connection.send(b'\x13') #home
		connection.send(b'\x93') #clear
		send_cr(connection, "white")
		send_ln(connection, "Disconnected from MOStodon..\n\n")
		connection.close()
		print('Timeout occurred.  Closed connection',connection)
		UsersCount -= 1
		print("\nConnected users ", UsersCount)



def threaded_clientTesting(connection):
	global UsersCount
	############################### removed the try and except for testing!!!!!!!!!!!!!!!!!! Use to display the error messages...
	connection.settimeout(1200) # 20 minutes of inactivity will end session.
	user_session(connection)
	run_once(connection)
	while True:
		timeline(connection)


try:
    MOStodon.bind((host, port))
    MOStodon.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,False) 
    
except socket.error as e:
    print("Connection error detected ->", str(e))

print('SERVER > Waiting for a Connection..\r')

MOStodon.listen()

while True:
    Client, address = MOStodon.accept()
    print('New connection from: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    UsersCount += 1
    print('Connected Users: ' + str(UsersCount))
	
