from gophishUtility import *
from gophish.models import *
import csv
from math import ceil
import os

# This client has all methods attached to it necessary to create, read, and run our campaigns.
gophishClient = GophishUtility.createGophishClient()

# Sets up new groups and moves all persons who clicked the link into our control group for training.
# Then it deletes all the groups and then recreates them with their new audience.
def setUpNewGroupsByCSV(csvFilename):
    students = [] # lists of users
    with open(csvFilename) as studentInfo:
        infoReader = csv.DictReader(studentInfo)
        count = 0
        index = 0
        for student in infoReader:
            newUser = User(first_name = student['firstName'], last_name = student['lastName'], email = student['email'])
            students.append(newUser)
            count = count + 1

    print("Students have been loaded into User objects")

    # Split the students into 20 groups of equal length. Each group will be adjusted later after seeing results.
    groups = []
    count = 0
    sizeOfGroups = ceil(len(students)/GophishUtility.numGroups)
    for i in range(0, len(students), sizeOfGroups):
        targets = students[i:i+sizeOfGroups]
        newGroup = Group(name = GophishUtility.groupNames[count], targets=targets)
        groups.append(newGroup)
        count = count + 1

    print("Users have been loaded into Group objects")

    for group in gophishClient.groups.get():
        if group.name in GophishUtility.groupNames:
            gophishClient.groups.delete(group.id)

    # Load groups into Gophish
    for group in groups:
        response = gophishClient.groups.post(group)
        print(response.name, "has been created on the server")

    return groups

# Starts the new campaigns based on the groups that are passed to it.
def startNewCampaigns(groups):
    for group in groups:
        emailSet = group.name.split('-')[0].strip()
        pageSet = group.name.split('-')[1].strip()

        campaign = Campaign(
            name=group.name,
            groups=[group],
            url="http://acu-edu.info",
            smtp=GophishUtility.getSMTPProfile(),
            template=GophishUtility.getEmailTemplateForDay(0, emailSet),
            page=GophishUtility.chooseLandingPage(pageSet)
        )

        response = gophishClient.campaigns.post(campaign)
        print(response.name, "Campaign has been started")

csvFilename = 'sigchiStudents.csv'
groups = setUpNewGroupsByCSV(csvFilename)
startNewCampaigns(groups)
