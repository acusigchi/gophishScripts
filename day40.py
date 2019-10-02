from gophishUtility import *
from gophish.models import *
from math import ceil
import os

# This client has all methods attached to it necessary to create, read, and run our campaigns.
gophishClient = GophishUtility.createGophishClient()

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

campaigns = getOurCampaigns()

# Need to change day0results.csv to match whatever day this query is for. For example, this query runs on day 2 so the results are for day 0.
# Day 7 should create day2results.csv and Day 30 should create day7results.csv. Finally we need a final query that will run say Day 40 and create
# day30results.csv.
GophishUtility.writeResultsTo('day30results.csv', campaigns)
GophishUtility.markListCampaignsComplete(campaigns)
