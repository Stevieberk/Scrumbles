from data import ScrumblesData, ScrumblesObjects


def printUserDetails(user):
    print(user.userID)
    print(user.userName)
    print(user.userEmailAddress)
    print(user.userRole)
    print()
    


login_info = ScrumblesData.DataBaseLoginInfo()
login_info.userID = 'test_user'
login_info.password = 'testPassword'
login_info.ipaddress = '173.230.136.241'
login_info.defaultDB = 'test'

dataConnection = ScrumblesData.ScrumblesData(login_info)
dataConnection.connect()
userTable = dataConnection.getData(ScrumblesData.Query.getAllUsersQuery)
dataConnection.close()

listOfAllUsers = []
for row in userTable:
    user = ScrumblesObjects.User(row)
    listOfAllUsers.append(user)

for user in listOfAllUsers:
    printUserDetails(user)
