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
    message+="</table>"
    notification = {"color": "purple", "message": message, "notify":False}
    url = 'https://expedia.hipchat.com/v2/room/3060320/notification?auth_token=eqqE5K0HmvDAP0IJcroihbhtvpeX9EX5iYZtY2fI'
    r = requests.post(url, data={"color":"red","message":"(hungry)? Food Trucks for " + time.strftime("%B %d") +":\n","notify":False,"message_format":"text"})
    r = requests.post(url, data=notification)
    return render(request, 'index.html')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})
