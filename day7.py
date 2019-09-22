from gophishUtility import *
from gophish.models import *
from math import ceil
import os

# This client has all methods attached to it necessary to create, read, and run our campaigns.
gophishClient = GophishUtility.CreateGophishClient()

# Gets all campaigns that are currently In Progress and are named something that can be found in the GophishUtility.groupNames list
# in the gophishUtility.py file.
def getOurCampaigns():
    campaigns = [campaign for campaign in gophishClient.campaigns.get() if campaign.name in GophishUtility.groupNames and campaign.status != "Completed"]
    return campaigns

# Write Campaign Results out to the file that you name in the parameter
def writeResultsTo(filename):
    with open(filename, "w") as resultsFile:
        resultsFile.write("First Name, Last Name, Email, Status, Group\n")
        for campaign in campaigns:
            for result in campaign.results:
                resultsFile.write("{},{},{},{},{}\n".format(result.first_name, result.last_name, result.email, result.status, campaign.name))

        resultsFile.close()

# Sets up new groups and moves all persons who clicked the link into our control group for training.
# Then it deletes all the groups and then recreates them with their new audience.
def setUpNewGroups(campaigns):
    groups = []
    count = 0
    for i in range(20):
        newGroup = Group(name = GophishUtility.groupNames[i], targets=[])
        groups.append(newGroup)

    for campaign in campaigns:
        for result in campaign.results:
            newUser = User(first_name = result.first_name, last_name = result.last_name, email = result.email)
            groupName = campaign.name if result.status != "Clicked Link" else campaign.name[:14]+"Control"
            for group in groups:
                if groupName == group.name:
                    group.targets.append(newUser)
                    print(newUser.first_name, result.status)

    for group in gophishClient.groups.get():
        if group.name in GophishUtility.groupNames:
            gophishClient.groups.delete(group.id)


    # Load groups into Gophish
    for group in groups[:1]:
        response = gophishClient.groups.post(group)
        print(response.name)

    return groups

# Chooses the correct email template for the group. Needs to be manually changed at this point to match what the correct template should be for each day.
def chooseEmailTemplate(emailSet):
    if emailSet == "Email Set 4":
        return Page(name="Full Mailbox")
    elif emailSet == "Email Set 3":
        return Page(name="Unusual Location")
    elif emailSet == "Email Set 2":
        return Page(name="Email Update")
    elif emailSet == "Email Set 1":
        return Page(name="Revalidate Mailbox")

# Chooses the correct landing page for all users who have one of these possible groupings
def chooseLandingPage(pageSet):
    if pageSet == "Expert Story":
        return Template(name="Expert - Story")
    elif pageSet == "Expert Facts":
        return Template(name="Expert - Facts")
    elif pageSet == "Peer Story":
        return Template(name="Peer - Story")
    elif pageSet == "Peer Facts":
        return Template(name="Peer - Facts")
    elif pageSet == "Control":
        return Template(name="Control")

# Completes the old campaigns that are passed to it
def completeOldCampaigns(campaigns):
    for campaign in campaigns:
        gophishClient.campaigns.complete(campaign.id)

# Starts the new campaigns based on the groups that are passed to it.
def startNewCampaigns(groups):
    for group in groups:
        emailSet = group.name.split('-')[0].strip()
        pageSet = group.name.split('-')[1].strip()

        campaign = Campaign(
            name=group.name,
            groups=[group],
            url="http://acu-edu.info",
            smtp=SMTP(name="ACU IT SendGrid"),
            template=chooseEmailTemplate(emailSet),
            page=chooseLandingPage(pageSet)
        )

        gophishClient.campaigns.post(campaign)

campaigns = getOurCampaigns()

# Need to change day0results.csv to match whatever day this query is for. For example, this query runs on day 2 so the results are for day 0.
# Day 7 should create day2results.csv and Day 30 should create day7results.csv. Finally we need a final query that will run say Day 40 and create
# day30results.csv.
writeResultsTo('day2results.csv')

groups = setUpNewGroups(campaigns)

completeOldCampaigns(campaigns)
startCampaigns(groups, campaigns)
