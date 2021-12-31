import telebot
import bs4
import requests
import datetime
import os

API_KEY = os.getenv('API_KEY')

bot = telebot.TeleBot(API_KEY)


def check_if_date(string):
    elements = string.text.split('-')
    if len(elements) == 3:
        return True
    else:
        return False

def get_songs(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, features="html.parser")

    print(soup)

    songs_elements = soup.find_all('h3', class_='a-no-trucate')
    artists_elements = soup.find_all('span', class_='a-no-trucate')

    songs = [element.text.split('\n')[1] for element in songs_elements]
    artists = [element.text.strip() for element in artists_elements]

    songs_artists = {}

    for i in range(0, len(songs)):
        songs_artists[songs[i]] = artists[i]

    return songs_artists



@bot.message_handler(commands=['start', 'help', 'hi', 'hello'])
def greet(message):
    bot.reply_to(message, "Hey! How's it going!\n\nWelcome to the Musical Time Machine. This is a bot that allows you to enter any date in time and then gets the hot 100 songs for that day according to Billboard.\n\n\nEnter your date in this format: YYYY-MM-DD.\nFor Example, to get the Billboard top 100 songs for 3rd Ferbuary, 2021, you should input '2021-02-03'.")

@bot.message_handler(func=check_if_date)
def greet(message):
    bot.send_message(message.chat.id, "Processing....")
    date = message.text.split('-')
    year = date[0]
    month = date[1]
    day = date[2]

    try:
        formatted_date = datetime.datetime(int(year), int(month), int(day))
        formatted_month = formatted_date.strftime("%B")
        formatted_day = formatted_date.strftime("%A")
    except:
        bot.send_message(message.chat.id, "Invalid date, Please input date in the right format!")

    songs = get_songs(f"https://www.billboard.com/charts/hot-100/{year}-{month}-{day}/")
    try:
        if len(songs) > 0:
            songs_text = ""

            counter = 0
            for i in songs.items():
                counter += 1
                songs_text += str(counter) + ". " + i[0] + " by " + i[1] + "\n"

            print(songs_text)
            bot.send_message(message.chat.id, f"These are the hot 100 songs for {formatted_day}, day {day} of {formatted_month}, {year}:\n{songs_text}")
        else:
            bot.send_message(message.chat.id, "There are no songs for this date")
    except:
        bot.send_message(message.chat.id, "An error occured, please try again later.")


bot.polling()