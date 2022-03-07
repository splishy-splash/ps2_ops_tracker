from __future__ import print_function
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from datetime import date
from shutil import copyfile
from os import remove
from discord.ext import commands
from discord import File
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
import datetime
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Initial Chrome selenium driver setup


client = commands.Bot(command_prefix='!')
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.minimize_window()
api_key = ''
gmail_calendar = ''
folder_path = ''
bot_token = ''




SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# , 'https://www.googleapis.com/auth/drive'

def query_cal():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId=gmail_calendar, timeMin=now,
                                        maxResults=1, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        print(start, event['summary'])
        print(end)



@client.event
async def on_ready():
    print("ops tracker bot! Beep Boop")




def initial_connect():
    """
    This function is to get through the first page of the TOPT tracker that is hosted locally.

    Users will need to change api_key to be their own.
    Users will need to change URL to point to their instance of TOPT if not on localhost.
    :return: None
    """
    # you can apply for an API key on DayBreak Game's website. Takes 2 minutes.
    outfit_tag = 'VKTZ'


    # this is the url. localhost or a hosted version
    driver.get('http://127.0.0.1:8082')

    # setting server to Emerald (server id is 17)
    srv_select = Select(driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[1]/select'))
    srv_select.select_by_value('17')

    # setting API key
    driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[3]/input').send_keys(api_key)

    # This is what clicks the button on the first page to connect
    driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/button[1]').click()


def second_page():
    # setting the outfit tag
    driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div/div[1]/div/input').send_keys('VKTZ')
    driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div/div[1]/div/div/button').click()
    sleep(15)

    # begin tracking
    driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div/div[5]/button').click()


def ops_start():

    # opens browser, automates first page, then waits 3 seconds before plugging in outfit tag and starting tracking

    driver.refresh()
    try:
        alert = driver.switch_to.alert
        alert.accept()
    except:
        pass
    initial_connect()
    sleep(5)
    second_page()
    return 'Starting meow!'


def ops_end():
    #set date for filename
    today = date.today()
    filename = folder_path + '\\ops '+ today.strftime('%Y-%m-%d') + '.json'
    # stop tracking ops
    driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div/div[4]/button').click()

    # download reports
    driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div/div[5]/div[2]/button[1]').click()
    sleep(1)
	
	#change these paths!! 
    copyfile('C:\\Users\\user\\Downloads\\data.json', filename)
    remove('C:\\Users\\user\\Downloads\\data.json')


    mydrive = MyDrive()
    mydrive.upload(filename)
    # to do: change this to return link to file in google drive
    return 'Done! o7'



@client.command()
async def startops(ctx):
    await ctx.send(ops_start())

@client.command()
async def endops(ctx):
    await ctx.send(ops_end())

sched = AsyncIOScheduler()
sched.start()

@sched.scheduled_job('interval', hours=24, start_date='2020-08-26 16:30:00')
async def period_job():
    query_cal()

query_cal()

while True:
    client.run(bot_token)
