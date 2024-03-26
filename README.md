### **termB.py** is a python script that implements a parameterized Telegram bot to help the remote user with basic actions like command executions and file transfers in remote devices.

This script allows basic actions that are normally performed by SSH sessions with programs like Putty and Filezilla. The big problem here is when your remote device is on a CGNAT network which avoid the unique identification of a device. The natural solutions for these cases are to use reverse SSH tunnels, VPNs or third party services like ngrok and pagekite, all of these are complicated and paid options for simple users who just want basic access to the device.

Install python on your remote device (router, gateways, computers...) and test this script, you will definitely like it. Configure it to start with the system.


**termB.py works with the following commands sent to the bot's chat:**

  **/start**: bot responds with a brief description of available services
  
  **/cmd <*some command line*>**: By this command the user can execute a remote command on the bot's target system, e.g.: /cmd ps will execute the ps command, the bot will respond with the result of the command, in this example case, a list of all currently running processes.
  
  **/getFile <*path_to_file*>**: By this command the user can ask the bot to send a file located at <path_to_file>, e.g.: the bot will respond  the command /getFile /tmp/log.txt with the file log .txt (if the file exists, of course).
  
  **/on**: This command activates the gpio *blue:usb* logical state.Change the script according to the gpio available on your hardware.
  
  **/off**: This command turns off the logical state of the gpio *blue:usb*.Change the script according to the gpio available on your hardware.

  
**PS1:** When a file is sent to the bot in chat, the file will be stored in the **/tmp** path.

**PS2:** The following animation shows a basic use of this bot running on a router with an OpenWrt system installed.

**PS3 (Very important!):** Telegram bots can be found by other users. To avoid interactions with unauthorized users, I strongly recommend reading the following article, in which the author shows very good ways to guarantee the bot's privacy. In remote applications such as industrial gateways, device access control is essential.

https://sarafian.github.io/low-code/2020/03/24/create-private-telegram-chatbot.html

![](https://github.com/AngeloGuimas/termB/blob/master/real_use.gif)
