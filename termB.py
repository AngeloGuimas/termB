import telebot
import requests
import subprocess
import os.path

#For security reasons store your bot token in enviroment variables
api_token = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(api_token)

#function to handler actions related to cmd commands on target system
@bot.message_handler(commands=['cmd'])
def cmd(message):
        command = ((message.text).replace('/cmd',''))
        if len(command)== 0:
                response= "Please insert a valid command. E.g.: \"cmd ps\" or \"get_file termB.py\"."
        else:
                #result = subprocess.run(command, shell=True, capture_output=True, text=True)
                result = subprocess.run([command], shell=True, capture_output=True, text=True)
                if(len(result.stderr)>0):
                        response = result.stderr
                elif(len(result.stdout)>0):
                        response = result.stdout
                else:
                        response = "command executed, but without response"
        bot.reply_to(message,response)

#function to handler actions related to getting files from a specific location in the system that is running the bot
@bot.message_handler(commands=['getFile'])
def getFile(message):
        command = ((message.text).replace('/getFile',''))
        if len(command)== 0:
                response= "Please, insert a valid command. E.g.: /cmd ps"
                bot.reply_to(message,response)
        else:
                command = command.split()
                if os.path.isfile(command[0]):
                        file = open(command[0], 'rb')
                        bot.reply_to(message,"Sending, please wait")
                        bot.send_document(message.chat.id, file)
                else:
                        bot.reply_to(message,"The required file doesn't exist!")
                        
#function to handler actions related to sending files to a specific location in system that is running the bot                        
@bot.message_handler(content_types=['document', 'photo', 'audio', 'video', 'voice'])
def putFile(message):
        file_info = bot.get_file(message.json[message.content_type][1]['file_id'])
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(api_token, file_info.file_path))
        #if /tmp not exist,create
        os.makedirs('/tmp', exist_ok=True)
        file_details = (file_info.file_path).split('/')
        with open('/tmp/'+file_details[1], 'wb') as file_local:
            file_local.write(file.content)
            bot.reply_to(message,"File successfully stored in: "+"/tmp/"+file_details[1])

#function to turn on a specific gpio, change the target gpio according with the possibilities of your hardware                        
@bot.message_handler(commands=['on'])
def gpio_on(message):
        subprocess.Popen('echo 255 > /sys/class/leds/blue:usb/brightness', shell=True,stdout=subprocess.PIPE)
        bot.reply_to(message,"Command received")

#function to turn off a specific gpio, change the target gpio according with the possibilities of your hardware     
@bot.message_handler(commands=['off'])
def gpio_off(message):
        subprocess.Popen('echo 0 > /sys/class/leds/blue:usb/brightness', shell=True,stdout=subprocess.PIPE)
        bot.reply_to(message,"Command received")

#function to present the bot options by /start command                                
@bot.message_handler(commands=['start'])
def start(message):
        start_message = "There are the followings commands to be used: \n\"/cmd\" is used to execute some line command in bot host system.\n\"/getFile <path_to_file>\" is used to get some file from bot host system.The path to file must be specified.\n\"/on\" is used to turn on the led \"blue:usb\".\n\"/off\" is used to turn off the led \"blue:usb\".\n\nPS1: Files sent to the bot will be stored in the /tmp path. Be careful, on unix distributions /tmp is a temporary folder, after reboot the files are deleted..\nPS2: Before uploading a file, make sure the destination system has enough space to store the file."
        bot.reply_to(message,start_message)
      
#function to answer a default message to non mapped commands                                
@bot.message_handler(func=lambda message: True)
def exception(message):
	bot.reply_to(message,"Command not recognized. Type \"/start\" to check available commands")

#bot looping to monitore all message handlers	
bot.infinity_polling()
