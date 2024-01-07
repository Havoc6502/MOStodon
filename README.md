# MOStodon
![image](https://github.com/Havoc6502/MOStodon/assets/140346993/fb95578a-86e7-42ae-911c-7d1dcc4ff2bc)

A Commodore 64 Mastodon Client. A C64 compatible Modem is required.
![image](https://github.com/Havoc6502/MOStodon/assets/140346993/8d7667ef-3318-4465-b748-16ab38294f89)

![image](https://github.com/Havoc6502/MOStodon/assets/140346993/d2800796-d172-4e12-8fc7-b78a2046c10e)

Python 3.7 or newer is required!

Install-

pip install -r requirements.txt


or install manually.-

pip install Mastodon.py

pip install anyascii


Create your Mastodon app on your Mastodon Instance.-

Log into your Mastodon instance and navigate to your settings. Under the Development tab click New Application.
Add the application name MOStodon. Default application settings should already be Read,Write. Crypto should not be needed
because all data is sent over https requests.

Click on the newly created app. Copy "Your access token" secret.
Paste the token between the quotes in MOStodon.py after access_token = ""
Add the name of your Mastodon instance between the quotes in api_base_url = ""
e.g. api_base_url = "https://oldbytes.space"

Running the MOStodon.py Server.-

Simply type python MOStodon.py

Connecting to the Server.-

You will need a compatible Commodore 64 Modem. Any of the C64 WiFi modems, a 1541 Ultimate, or equivilent Modem will work.
You can even use Vice with TCPser.
The higher the Baud rate the better!

Once the Server is running you can log into the Server with any Commodore Modem software that works with your Modem. CCGMS, etc..
Because local IP addresses can change I prefer to connect by using AT commands instead of saving the Server IP. 
With CCGMS you can type atdt192.168.1.100:6502 to connect. Use the IP of your Local Machine running MOStodon.py

Changing the look of MOStodon.-

You can change the colors of almost every aspect of MOStodon. Simply edit the MOStodon.py color variables with the list of included colors.
Other hard coded colors can be changed by finding them in the code and replacing the "color".
