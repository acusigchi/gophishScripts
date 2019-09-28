from gophishUtility import *
from gophish.models import *
import csv
from math import ceil

# This client has all methods attached to it necessary to create, read, and run our campaigns.
gophishClient = GophishUtility.createGophishClient()


def createGroups(csvFilename, testFlag):
    students = [] # list of lists of users
    with open(csvFilename) as studentInfo:
        infoReader = csv.DictReader(studentInfo)
        count = 0
        index = 0
        for student in infoReader:
            newUser = User(first_name = student['firstName'], last_name = student['lastName'], email = student['email']+"@example.com")
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

    # Load groups into Gophish
    for group in groups:
        response = gophishClient.groups.post(group)
        if testFlag:
            gophishClient.groups.delete(response.id)


runTest = True
csvFilename = 'sigchiStudents.csv'
createGroups(csvFilename, runTest)
