import requests
from bs4 import BeautifulSoup

import discord,asyncio,os
from discord.ext import commands, tasks
from discord.ext.commands import Bot

###client = discord.Client()
DISCORD_TOKEN="ODA1MTQ3NzAxNjc1MTYzNjg4.YBWqOw.JO5KvQcXn5oht5CCG8eAgNeF-aU"
#client.run(DISCORD_TOKEN)
bot = Bot(command_prefix="$")


class url_info:
    def __init__(self, text, url):
        self.text = text
        self.url = url

def Controller():
    return_list = Scrape_Mega() + Scrape_Daesong()
    return return_list

def Scrape_Mega():
    url_list = []
    Url = "https://www.megastudy.net/inside/event/event_list.asp?tab=0&page={}"
    for n in range(1, 6):
        page = requests.get(Url.format(n))
        page.encoding='euc-kr'

        soup = BeautifulSoup(page.text, 'html.parser')

        list1 = soup.find_all(class_="txt")
        for item in list1:
            if "선착순" in item.text:
                info = url_info(item.text, item.find('a')['href'])
                url_list.append(info)
            if "광클" in item.text:
                info = url_info(item.text, item.find('a')['href'])
                url_list.append(info)
    return url_list
def Scrape_Daesong():
    url_list = []
    Urls = ["http://www.mimacstudy.com/event/eventIngList.ds?searchType=evtName&searchText=%B1%A4%C5%AC","http://www.mimacstudy.com/event/eventIngList.ds?searchType=evtName&searchText=%BC%B1%C2%F8%BC%F8"]
    # TEST ONLY == > Urls = ["http://www.mimacstudy.com/event/eventIngList.ds?requestMenuId=M000000045"]
    for url in Urls:
        page = requests.get(url)
        page.encoding = 'euc-kr'
        soup = BeautifulSoup(page.text, 'html.parser')

        list2 = soup.find(class_ = "contentsarea").find_all('li')
        for item in list2:
            img_class = item.find(class_="img")
            if img_class is not None:
                extract_url = img_class.find('img')['src']
                info = url_info(img_class.find('img')['alt'], extract_url)
                url_list.append(info)
    return url_list

@bot.event
async def on_ready():
    infinite_loop.start()
    print(f'Bot connected as {bot.user}')
    


@tasks.loop(seconds=86400)
async def infinite_loop():
    channel = bot.get_channel(805147898638499884)
    info_list = Controller()
    OutputString = ""
    index = 1
    embedVar = discord.Embed(title="이벤트 목록")
    for info in info_list:
        embedVar.add_field(name=info.text, value = info.url)
        
    await channel.send(embed=embedVar)
    

bot.run(DISCORD_TOKEN)