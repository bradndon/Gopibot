from __future__ import print_function

from django.shortcuts import render
from django.http import HttpResponse
import httplib2
import os
import time
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import requests


from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', developerKey='AIzaSyD_otvSldDNjFXyEd3W70CpQTDJkldNa2I')

    spreadsheetId = '1gVJNMbbD8Zkbm_sFljkGZLmWc9lNJrfTimrM8wfXwgY'
    rangeName = 'A1:F21'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])
    allResults = [];
    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        dates = ["","","","","",""]
        for row in values:
            if not row[0]:
                dates = row
            else :

                for index, v in enumerate(row):
                    if (time.strftime("%d") == dates[index]):
                        allResults.append([row[0]] + v.replace("\n", ", ").replace("-", "").strip().split(", "))
    while len(allResults) != 3 :
        allResults.append([])
    message="<table>"
    for i in range(0, max(len(allResults[0]), len(allResults[1]), len(allResults[2]))):
        message += "<tr>"
        for j in range(0,3):
            if i == 0:
                message+="<th>"
            else:
                message+="<td>"
            if len(allResults[j]) > i:
                message+=allResults[j][i]
            if i == 0:
                message+="</th>"
            else:
                message+="</td>"
        message += "</tr>"
    message+="</table><p>Warning: There is no guarantee these values are correct</p>"
    notification = {"color": "purple", "message": message, "notify":False}
    url = 'https://expedia.hipchat.com/v2/room/3060320/notification?auth_token=eqqE5K0HmvDAP0IJcroihbhtvpeX9EX5iYZtY2fI'
    r = requests.post(url, data={"color":"red","message":"(hungry)? Food Trucks for " + time.strftime("%B %d") +":\n","notify":False,"message_format":"text"})
    r = requests.post(url, data=notification)
    return render(request, 'index.html')

def recommend(request):
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', developerKey='AIzaSyD_otvSldDNjFXyEd3W70CpQTDJkldNa2I')

    spreadsheetId = '1gVJNMbbD8Zkbm_sFljkGZLmWc9lNJrfTimrM8wfXwgY'
    rangeName = 'A1:F21'
    # result = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()


    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])
    allResults = [];
    if not values:
        print('No data found.')
    else:
        dates = ["","","","","",""]
        for row in values:
            if not row[0]:
                dates = row
            else :
                for index, v in enumerate(row):
                    if time.strftime("%d") == dates[index]:
                        allResults.append([row[0]] + v.replace("\n", ", ").replace("-", "").strip().split(", "))
    while len(allResults) != 3 :
        allResults.append([])
    choices = []
    for i in range(0, max(len(allResults[0]), len(allResults[1]), len(allResults[2]))):
        for j in range(0,3):
            if len(allResults[j]) > i:
                message =  allResults[j][i]
                if "Bumbu" in message:
                    choices.append("Bumbu is at " + allResults[j][0] + " today. We should tell Agnes.")
                elif message == "The Box":
                    choices.append("The Box is at " + allResults[j][0] + " today. (mmhmm)")
                elif "Mangia" in message:
                    choices.append("Mangia Me is at " + allResults[j][0] + " today. I enjoy the pasta there.")
    randNum = random.randint(0,2)
    while len(allResults[randNum]) < 2:
        randNum = random.randint(0,2)
    note = ""
    if len(choices) == 0:
        note = "Let's check out " + allResults[randNum][0] +  " today."
    elif len(choices) == 1:
        note = choices[0]
    else:
        note = "There are a few good options today:\n" + "\n".join(choices)
    notification = {"color": "green", "message": note, "notify":False,"message_format":"text"}
    print(notification)
    url = 'https://expedia.hipchat.com/v2/room/3060320/notification?auth_token=eqqE5K0HmvDAP0IJcroihbhtvpeX9EX5iYZtY2fI'
    r = requests.post(url, data=notification)
    return render(request, 'index.html')

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})
