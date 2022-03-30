import codecs
import os
import shutil
import urllib.request
import time
import discord

from pathlib import Path
from instagram_private_api import Client
from collections import namedtuple
from xml.dom.minidom import parseString

TOKEN = 'OTQ1MjIyMjUwNjQ1MzAzMzM4.YhNA0Q.TRIs2HubonpyelfQc2wzCaccu8A'
INSTA_USERNAME = 'jkt48.zee'
INSTA_ID       = '9144760144'

def absPath(path):
    return str(Path(__file__).resolve().parent.joinpath(path))

def getStory(storyGET):
    with open(absPath('config/instaAPI.txt')) as instaData:
        kuki = codecs.decode(instaData.read().encode(), 'base64')
    dataGET = Client(INSTA_USERNAME,'', cookie=kuki)
    storyData = dataGET.user_reel_media(INSTA_ID)
    if storyData['items'] is not None:
        for i in storyData['items']:
            storyID = i['id']
            storyGET = absPath('assets/'+storyID+'.mp4')
            if i["media_type"] == 1:
                url = i['image_versions2']['candidates'][0]['url']
                end = storyGET
                urllib.request.urlretrieve(url, end)
            elif i["media_type"] == 2:
                url = i['video_versions'][0]['url']
                end = storyGET
                urllib.request.urlretrieve(url, end)

def ReadLastStory():
    if not os.path.exists(absPath('tempDiscord.txt')):
        return 0
    with open(absPath('tempDiscord.txt')) as file:
        read = file.read()
        timestamp = str(read)
    return timestamp

def deleteStory():
    shutil.rmtree(absPath('assets/'))
    os.makedirs(absPath('assets/'))
    with open('assets/story','w') as file:
        file.write('')

client = discord.Client()
@client.event
async def on_ready():
    print('si gadis tomboy yang semangatnya meletup-letup, halo aku {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('halo'):
        while True:
            if __name__ == '__main__':
                with open(absPath('config/instaAPI.txt')) as instaData:
                    kuki = codecs.decode(instaData.read().encode(), 'base64')
                dataGET = Client(INSTA_USERNAME,'', cookie=kuki)
                storyData = dataGET.user_reel_media(INSTA_ID)
                if storyData['items'] is not None:
                    for i in storyData['items']:
                        storyID = i['id']
                        lastStory = ReadLastStory()
                        if lastStory >= str(storyID):
                            print('STORY {} ALREADY SENT'.format(storyID))
                            continue
                        if i["media_type"] == 1:
                            storyGET = absPath('assets/'+storyID+'.jpg')
                            time.sleep(5)
                            url = i['image_versions2']['candidates'][0]['url']
                            urllib.request.urlretrieve(url, storyGET)
                            print('UPLOADING {}...'.format(storyGET))
                            files = discord.File(storyGET)
                            await message.channel.send('aku update story nich @everyone', file=files)
                            print('SUCCESS!')
                            with open('tempDiscord.txt','w') as file:
                                write = str(storyID)+'\n'
                                file.write(write)
                        elif i["media_type"] == 2:
                            storyGET = absPath('assets/'+storyID+'.mp4')
                            time.sleep(5)
                            url = i['video_versions'][0]['url']
                            urllib.request.urlretrieve(url, storyGET)
                            print('UPLOADING {}...'.format(storyGET))
                            files = discord.File(storyGET)
                            await message.channel.send('aku update story nich @everyone', file=files)
                            print('SUCCESS!')
                            with open('tempDiscord.txt','w') as file:
                                write = str(storyID)+'\n'
                                file.write(write)
                    else:
                        print('NOT STORIES FOUND')
                    deleteStory()
                time.sleep(5)

client.run(TOKEN)