from gophish import Gophish


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
    def CreateGophishClient():
        # This client has all methods attached to it necessary to create, read, and run our campaigns.
        return Gophish(GophishUtility.apiKey, host=GophishUtility.baseUri, verify=False)
