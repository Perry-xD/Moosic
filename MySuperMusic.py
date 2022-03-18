import json
import os
try:
  import telebot
else:
  os.system("pip install pytelegrambotapi")
from telebot import TeleBot
import time
import urllib
import urllib2

try:
  from bs4 import BeautifulSoup
else:
  os.system("pip install beautifulsoup4")
from bs4 import BeautifulSoup

try:
  from slugify import slugify
else:
  os.system("pip install slugify")

TOKEN = os.environ.get("BOT_TOKEN")
WelcomeGreeting = '**Welcome! Just send me the name of the song that you want to download.**'
base_url = 'http://www.youtubeinmp3.com/fetch/?format=JSON&video='

bot = TeleBot(TOKEN)
path = './Downloads/'

@bot.message_handler(commands=["start"])
def starting(message):
  bot.send_message(message.chat.id, WelcomeGreeting)

@bot.message_handler()
def sonmg(message):
  song_name = message.text
    bot.send_message(message.chat.id, f"Hi there, the song {song_name} is on its way...")

    query = urllib.quote(song_name+ "song")
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib2.urlopen(url)

    soup = BeautifulSoup(response.read(), "html.parser")
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        video_url = 'https://www.youtube.com' + vid['href']
        json_url = base_url + video_url

        response = urllib.urlopen(json_url)

        try:
            data = json.loads(response.read())
            if 'length' not in data:
                raise ValueError("No length present.")
                break
            if 'link' not in data:
                raise ValueError("No link present.")
                break
            if 'title' not in data:
                raise ValueError("No title present.")
                break

            length = data['length']
            downLoad_url = data['link']
            title = data['title']

            upload_file = path + slugify(title).lower() + '.mp3'

            if not (os.path.exists(upload_file)):
                bot.send_message(message.chat.id, '**Download for your song has started..**')

                downloadSong(downLoad_url, upload_file)
                bot.send_message(message.chat.id, '**Download is complete. Song is being sent to you. Please wait.**')

                bot.send_audio(message.chat.id, open(upload_file , 'rb'), length , '', title)

        except ValueError as e:
            print 'No song found', e
            bot.send_message(message.chat.id, '**No song found. Please try again with a different keyword.**')

        break

def downloadSong(url, fileLoc):
    f = open(fileLoc, 'wb')
    usock = urllib2.urlopen(url)
    try :
      file_size = int(usock.info().getheaders("Content-Length")[0])
    except IndexError:
      print ('Unknown file size: index error')

    block_size = 8192
    while True:
        buff = usock.read(block_size)
        if not buff:
            break
        f.write(buff)
    f.close()

    print("done")


# Keep the program running
if __name__ == "__main__":
  bot.polling()
