from gophishUtility import *
from gophish.models import *
from math import ceil
import os

# This client has all methods attached to it necessary to create, read, and run our campaigns.
gophishClient = GophishUtility.createGophishClient()

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
    for group in [nonEmptyGroups for nonEmptyGroups in groups if nonEmptyGroups .targets]:
        response = gophishClient.groups.post(group)
        print(response.name)

    return [nonEmptyGroups for nonEmptyGroups in groups if nonEmptyGroups .targets]

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
            template=GophishUtility.getEmailTemplateForDay(30, emailSet),
            page=GophishUtility.chooseLandingPage(pageSet)
        )

        response = gophishClient.campaigns.post(campaign)
        print(response.name, "Campaign has been started")


campaigns = GophishUtility.getOurCampaigns()

# Need to change day0results.csv to match whatever day this query is for. For example, this query runs on day 2 so the results are for day 0.
# Day 7 should create day2results.csv and Day 30 should create day7results.csv. Finally we need a final query that will run say Day 40 and create
# day30results.csv.
GophishUtility.writeCampaignResultsTo('day7results.csv', campaigns)

groups = setUpNewGroups(campaigns)

GophishUtility.markListCampaignsComplete(campaigns)
startNewCampaigns(groups)
