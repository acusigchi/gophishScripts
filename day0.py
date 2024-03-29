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
        for student in infoReader:
            newUser = User(first_name = student['firstName'], last_name = student['lastName'], email = student['email'])
            students.append(newUser)

    print("Students have been loaded into User objects")

    # Split the students into 20 groups of equal length. Each group will be adjusted later after seeing results.
    groups = []
    for i in range(GophishUtility.numGroups):
        targets = [students[j] for j in range(len(students)) if j % GophishUtility.numGroups == i]
        newGroup = Group(name = GophishUtility.groupNames[i], targets=targets)
        groups.append(newGroup)
        print(newGroup.name)

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

campaigns = GophishUtility.getOurCampaigns()
GophishUtility.markListCampaignsComplete(campaigns)
csvFilename = 'studentList.csv'
groups = setUpNewGroupsByCSV(csvFilename)
startNewCampaigns(groups)
