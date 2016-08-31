from __future__ import print_function
import os
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
import random
from django.views.decorators.csrf import csrf_exempt


def getValues():
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', developerKey=os.environ['DEVELOPER_KEY'])

    spreadsheetId = '1gVJNMbbD8Zkbm_sFljkGZLmWc9lNJrfTimrM8wfXwgY'
    result = service.spreadsheets().get(spreadsheetId=spreadsheetId, includeGridData=False).execute()
    sheetId = ""
    for sheet in result["sheets"] :
        if time.strftime("%B") in sheet["properties"]["title"]:
            sheetName = sheet["properties"]["title"]

    rangeName = sheetName + '!A1:F21'
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
    return allResults

@csrf_exempt
def index(request):
    allResults = getValues()
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
    url = os.environ["HIPCHAT_URL"]
    r = requests.post(url, data={"color":"red","message":"(hungry)? Food Trucks for " + time.strftime("%B %d") +":\n","notify":False,"message_format":"text"})
    r = requests.post(url, data=notification)
    return render(request, 'index.html')

@csrf_exempt
def recommend(request):
    allResults = getValues()
    choices = []
    for index, j in enumerate(allResults):
        for message in j:
            if "Bumbu" in message:
                choices.append("Bumbu is at " + allResults[index][0] + " today. We should tell Agnes.")
            elif message == "The Box":
                choices.append("The Box is at " + allResults[index][0] + " today. (mmhmm)")
            elif "Mangia" in message:
                choices.append("Mangia Me is at " + allResults[index][0] + " today. I enjoy the pasta there.")
            elif "Papa B" in message:
                choices.append("Papa Bois is at " + allResults[index][0] + " today. I would recommend it.")
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
    url = os.environ["HIPCHAT_URL"]
    r = requests.post(url, data=notification)
    return render(request, 'index.html')

@csrf_exempt
def about(request):
    notification = {"color": "gray", "message": "This bot is a tribute to the most stylish man in Seattle. It will help you decide on lunch for the day.", "notify":False,"message_format":"text"}
    url = os.environ["HIPCHAT_URL"]
    r = requests.post(url, data=notification)
    return render(request, 'index.html')
