from gophish import Gophish
from gophish.models import *


# These are hard-coded values that should not be changed without consulting John Marsden (jmm15f@acu.edu)
class GophishUtility:
    apiKey = "a13fe2c8d9b2fff652fed82530e4c6db5fe7acc0012808968a113d8cb724941a"
    baseUri = "https://www.acu-edu.info:3333"
    numGroups = 20
    groupNames = [
        'Email Set 1 - Expert Facts',
        'Email Set 1 - Expert Story',
        'Email Set 1 - Peer Facts',
        'Email Set 1 - Peer Story',
        'Email Set 1 - Control',
        'Email Set 2 - Expert Facts',
        'Email Set 2 - Expert Story',
        'Email Set 2 - Peer Facts',
        'Email Set 2 - Peer Story',
        'Email Set 2 - Control',
        'Email Set 3 - Expert Facts',
        'Email Set 3 - Expert Story',
        'Email Set 3 - Peer Facts',
        'Email Set 3 - Peer Story',
        'Email Set 3 - Control',
        'Email Set 4 - Expert Facts',
        'Email Set 4 - Expert Story',
        'Email Set 4 - Peer Facts',
        'Email Set 4 - Peer Story',
        'Email Set 4 - Control'
    ]

    @staticmethod
    def createGophishClient():
        # This client has all methods attached to it necessary to create, read, and run our campaigns.
        return Gophish(GophishUtility.apiKey, host=GophishUtility.baseUri, verify=False)

    @staticmethod
    def getEmailTemplateForDay(day, emailSet):
        if day == 0:
            if emailSet == "Email Set 1":
                return GophishUtility.getEmailTemplatePage(1)
            elif emailSet == "Email Set 2":
                return GophishUtility.getEmailTemplatePage(2)
            elif emailSet == "Email Set 3":
                return GophishUtility.getEmailTemplatePage(3)
            elif emailSet == "Email Set 4":
                return GophishUtility.getEmailTemplatePage(4)
        elif day == 2:
            if emailSet == "Email Set 1":
                return GophishUtility.getEmailTemplatePage(2)
            elif emailSet == "Email Set 2":
                return GophishUtility.getEmailTemplatePage(4)
            elif emailSet == "Email Set 3":
                return GophishUtility.getEmailTemplatePage(1)
            elif emailSet == "Email Set 4":
                return GophishUtility.getEmailTemplatePage(3)
        elif day == 7:
            if emailSet == "Email Set 1":
                return GophishUtility.getEmailTemplatePage(3)
            elif emailSet == "Email Set 2":
                return GophishUtility.getEmailTemplatePage(1)
            elif emailSet == "Email Set 3":
                return GophishUtility.getEmailTemplatePage(4)
            elif emailSet == "Email Set 4":
                return GophishUtility.getEmailTemplatePage(2)
        elif day == 30:
            if emailSet == "Email Set 1":
                return GophishUtility.getEmailTemplatePage(4)
            elif emailSet == "Email Set 2":
                return GophishUtility.getEmailTemplatePage(3)
            elif emailSet == "Email Set 3":
                return GophishUtility.getEmailTemplatePage(2)
            elif emailSet == "Email Set 4":
                return GophishUtility.getEmailTemplatePage(1)

    @staticmethod
    def getEmailTemplatePage(number):
        if number == 1:
            return Page(name="Email Update")
        elif number == 2:
            return Page(name="Full Mailbox")
        elif number == 3:
            return Page(name="Revalidate Mailbox")
        elif number == 4:
            return Page(name="Unusual Location")

    @staticmethod
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

    @staticmethod
    def writeCampaignResultsTo(filename, campaigns):
        with open(filename, "w") as resultsFile:
            resultsFile.write("First Name, Last Name, Email, Status, Group\n")
            for campaign in campaigns:
                for result in campaign.results:
                    resultsFile.write("{},{},{},{},{}\n".format(result.first_name, result.last_name, result.email, result.status, campaign.name))

            resultsFile.close()

    @staticmethod
    def getSMTPProfile():
        return SMTP(name="ACU IT SendGrid")

    @staticmethod
    def markListCampaignsComplete(campaigns):
        gophishClient = GophishUtility.createGophishClient()
        for campaign in campaigns:
            gophishClient.campaigns.complete(campaign.id)

    # Gets all campaigns that are currently In Progress and are named something that can be found in the GophishUtility.groupNames list
    @staticmethod
    def getOurCampaigns():
        gophishClient = GophishUtility.createGophishClient()
        campaigns = [campaign for campaign in gophishClient.campaigns.get() if campaign.name in GophishUtility.groupNames and campaign.status != "Completed"]
        return campaigns
