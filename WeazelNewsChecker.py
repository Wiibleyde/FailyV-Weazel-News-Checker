"""
Begining of config
"""
WEBHOOK_URL="URL_HERE"
UrlWN='http://panel.failyv.com/weazelnews/'
WikiFaily='https://failyv.fandom.com/fr/wiki/'
"""
End of config
"""

#=======================================================================================================================================================================================
# Don't modify after this line
#=======================================================================================================================================================================================

import bs4 as bs
import requests
from time import sleep
from discord_webhook import DiscordWebhook, DiscordEmbed
import random


def getLastArticle(url):
    """get last article title and content with a link (article are on a row)"""
    page=requests.get(url)
    soup=bs.BeautifulSoup(page.text, 'html.parser')
    article=soup.find('div', class_='col-md-6')
    title=article.find('h2').text
    author=article.find('span', class_='author mr-2').text
    img=article.find('img')['src']
    link=article.find('a')['href']
    return [title, author, link, img]

def noteLastArticle(title):
    """save last article title in a file"""
    with open('last_article.txt', 'w') as f:
        f.write(title)

def compareLastArticle(url):
    """compare last article title with last article title in file"""
    last_article=getLastArticle(url)[0]
    with open('last_article.txt', 'r') as f:
        last_article_file=f.read()
    if last_article==last_article_file:
        return False
    else:
        return True

def sendMessage(title, author, url, img):
    """send message to discord webhook"""
    webhook = DiscordWebhook(url=WEBHOOK_URL)
    embed=DiscordEmbed(title='Nouvel article Weazel News !', description=title, color=0xfc0000, url=url)
    authorName=author.replace(' ','_').replace("'","%27")
    authorUrl=f'{WikiFaily}{authorName}'
    embed.set_author(name=author, url=authorUrl)
    embed.set_image(url=img)
    webhook.add_embed(embed)
    response = webhook.execute()

if __name__ == '__main__':
    url=UrlWN
    noteLastArticle(str(getLastArticle(url)[0]))
    while True:
        lstInfo=getLastArticle(url)
        title=str(lstInfo[0])
        author=str(lstInfo[1])
        link=f'{UrlWN}{str(lstInfo[2])}'
        if str(lstInfo[3]).startswith('images/'):
            img=f'{UrlWN}{str(lstInfo[3])}'
        else:
            img=str(lstInfo[3])
        if compareLastArticle(url):
            print('New article')
            sendMessage(title, author, link, img)
            noteLastArticle(title)
        else:
            print('No new article')
        print('Program finished')
        randomSleep=random.randint(30,50)
        print(f'sleeping for {randomSleep} seconds')
        sleep(randomSleep)
        print('Program restarted')
