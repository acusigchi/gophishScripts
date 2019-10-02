from gophishUtility import *
from gophish.models import *

gophishClient = GophishUtility.createGophishClient()

for campaign in gophishClient.campaigns.get():
    print(campaign.name, campaign.status)

print("Finished.")
