# Cisco Meraki ExCap Splash Page Server

Overview

This Node.JS applications provides an example of the ExCAP interface for delivering a custom Captive Portal / Splash Page for Cisco Meraki access points.

###Complete write-up: 
http://www.internetoflego.com/wifi-hotspot-cisco-meraki-excap-nodejs/

###Official ExCap API documentation: 
https://meraki.cisco.com/lib/pdf/meraki_whitepaper_captive_portal.pdf

#Usage

Configure the Wi-Fi SSID

Logon to the Meraki Dashboard

Dashboard --> Wireless --> Access Control: (select SSID name from list)

Configure an SSID with a Sign-on or Click-through splash page.

Scroll down the page and enable the "Walled Garden". Enter the IP address of your web server, to provide access to your splash page content prior to authentication. Enter any additional IP addresses for hosted content such as images, terms of service, etc in this section as well.

Configure the Splash Page

Dashboard --> Wireless --> Configure --> Splash Page Select: Use custom URL

Enter the URL for the splash page. This flow provides two options, Sign-on and Click-through.

#Sign-on

http://yourserver/signon


#Click-through

http://yourserver/click


#Install

### Install MongoDB
https://docs.mongodb.com/manual/installation/

### Clone the ExCap app into your intended directory 
```
mkdir excap
cd excap
git clone https://github.com/dexterlabora/excap.git
```

### Install any missing dependencies
`npm install`

### Run the app
`node app.js`       or as a service using PM2:  `pm2 start app.js --name excap`
   

#Report
You can see the session data by going to

http://yourserver/excapData/excap

#Enjoy!

Note: You should run this using SSL. The reports are not protected in anyway, so either sort that out or disable the mongodb REST route.


#Written by
Cory Guynn, 2015
www.InternetOfLego.com


