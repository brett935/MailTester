#
#
#Working on fixing function readOutlookCSV2010(), readOutlookCSV2013() does work
#


import urllib2
import urllib

valid = [] #holds list of verified email addresses
invalid = [] #holds list of invalid email addresses
outlookList = [] #holds list of emails imported from Outlook CSV

#test an email address using mailtester.com, has one paramater (email to be tested)
def testAddress(email):
    query_args = { 'email':email }
     
    url = 'http://mailtester.com/testmail.php'
     
    data = urllib.urlencode(query_args)
     
    request = urllib2.Request(url, data)
     
    response = urllib2.urlopen(request).read()
    
    searchString=['E-mail address is valid']
    
    if any(x in response for x in searchString):
        #print "valid email"
        valid.append(email)
        
    else:
        #print "invalid email"
        invalid.append(email)

#imports emails from a Outlook formatted CSV file
def readOutlookCSV2013():
    print " "
    filename = raw_input('Enter name of CSV file: ')
    f = open( filename, 'r')
    f.readline() #read first line and dont use it because it contains no email addresses
    for line in f:
        email =  line.split(' ')[0] #split by first character after email address
        #email = email[:-1] #was used to remove blank space from end of email
        outlookList.append(email) #add email to list that contains all emails read from the Outlook CSV file
    f.close()

def readOutlookCSV2010():
    print " "
    filename = raw_input('Enter name of CSV file: ')
    f = open( filename, 'r')
    f.readline() #read first line and dont use it because it contains no email addresses
    for line in f:
        if line!='""':
            email =  line.split(' ')[0] #split by first character after email address
            #email = email[1:] #removes quotation mark from beginning of email
            email = email.lstrip('"')
            email = email.lstrip('\n')
            print email
            outlookList.append(email) #add email to list that contains all emails read from the Outlook CSV file
    f.close()

def testOutlookList():
    print " "
    print "TESTING ADDRESSES"
    print "Emails addresses in CSV file: "
    #iterate through list of emails from the Outlook CSV and test each of them individually
    for x in outlookList:
        print x
        testAddress(x) 

def saveToFile():
    print " "

    #save valid emails to a file
    v = open( 'valid.txt', 'w')
    for x in valid:
        v.write(x)
        v.write("\n") #seperate emails by a new line
    v.close()

    #save invalid emails to a file
    i = open( 'invalid.txt', 'w')
    for x in invalid:
        i.write(x)
        i.write("\n") #seperate emails by a new line
    
    #i.close()
    
def main():
    choice = raw_input("Enter 1 for Outlook 2013 CSV: \n Enter 2 for Outlook 2010 CSV:\n")
    if choice=="1":
        print "You chose Outlook 2013 CSV"
        readOutlookCSV2013() #call function that reads emails from Outlook CSV file
    elif choice =="2":
        print "You chose Outlook 2010 CSV"
        readOutlookCSV2010()
                       
    testOutlookList() #call function that test emails from Outlook email list

    #display valid email addresses from valid email list
    print " "
    print "VALID: "
    count = 0
    for x in valid:
        print valid[count]
        count += 1

    print " "

    #display invalid email addresses from invalid email list
    print "INVALID: "
    count = 0
    for x in invalid:
        print invalid[count]
        count += 1

    saveToFile()

    print "Complete."
    raw_input ('Press the Enter key to exit')

    
main()
