#developed on python 2.7.10

import urllib2
import urllib
import sys #for sys.exit("Error message")
import time #for timestamp on error logs and pause

valid = [] #holds list of verified email addresses
invalid = [] #holds list of invalid email addresses
cantValidate = [] #holds a list of email addresses that dont support being validated
outlookList = [] #holds list of emails imported from Outlook CSV
waitTime = 0 #time to wait between testing emails, this keeps a server from blacklisting you after too many tries

#test an email address using mailtester.com, has one paramater (email to be tested)
def testAddress(email):
    try:
        query_args = { 'email':email }
     
        url = 'http://mailtester.com/testmail.php'
     
        data = urllib.urlencode(query_args)
         
        request = urllib2.Request(url, data)
     
        response = urllib2.urlopen(request).read()
    
        searchString=['E-mail address is valid'] #string to search for to detect if the email was valid
        errorString=['503 Service Unavailable'] #string to search for to detect a timeout because to many request from same IP address
        cantValidateString=["Server doesn't allow e-mail address verification"] #string to search for to detect if the server doesnt support email validation
        
        if any(x in response for x in searchString):
            #print "valid email"
            valid.append(email)

        elif any(x in response for x in cantValidateString):
            #print "server doesnt support email validation"
            cantValidate.append(email)
            
        elif any(x in response for x in errorString):
            error = "Server Timeout because to many request from same IP address -"
            error += time.asctime() #add timestamp to error message
            timeOutError(error + " " + email) #add timeout message to log
            input (error + " Press Enter to exit")
            sys.exit(error)
        
        else:
            #print "invalid email"
            invalid.append(email)
    except urllib2.HTTPError:
        saveToFile() #if an error occurs testing an email then save all tested emails up to that point
        timeOutError(email) #add email that caused a problem to the error log
    except:
        saveToFile() #if an error occurs testing an email then save all tested emails up to that point
        unknownError(email) #if an error occurs testing an email then save all tested emails up to that point
        

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
    print "####TESTING ADDRESSES####"
    print "Emails addresses in CSV file: "
    #iterate through list of emails from the Outlook CSV and test each of them individually
    for x in outlookList:
        print x
        testAddress(x)
        time.sleep(waitTime) #pause so that the server gets a break between test and doesn't blacklist you

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
    i.close()

    #save emails that cant be validated to a file
    c = open( 'cantValidate.txt', 'w')
    for x in cantValidate:
        c.write(x)
        c.write("\n")
    c.close()
    
def errorEmailTest(email):
    error = "Couldn't validate this email because server doesn't support validation:  "
    error += email + time.asctime() #add email to error string
    errorLog(error)
    
def timeOutError(email):
    error = "Timed out on: "
    error += email + " " + time.asctime()
    errorLog(error)

def unknownError(email):
    error = "An unknown error occured: "
    error += email + " " + time.asctime()
    errorLog(error)
    
def errorLog(error):
    e = open( 'errors.txt', 'a')
    e.write(error)
    e.write("\n") #seperate errors by new line
    e.close
    
def main():
    choice = raw_input("Enter 1 for Outlook 2013 CSV: \n Enter 2 for Outlook 2010 CSV:\n")
    if choice=="1":
        print "You chose Outlook 2013 CSV"
        readOutlookCSV2013() #call function that reads emails from Outlook CSV file
    elif choice =="2":
        print "You chose Outlook 2010 CSV"
        readOutlookCSV2010()

    waitTime = input("\nEnter the amount of seconds you want to wait between email test (Default=0, use a higher value if you keep getting timed out errors): ")
                       
    testOutlookList() #call function that test emails from Outlook email list

    #display valid email addresses from valid email list
    print " "
    print "####VALID: "
    count = 0
    for x in valid:
        print valid[count]
        count += 1

    print " "

    #display invalid email addresses from invalid email list
    print "####INVALID: "
    count = 0
    for x in invalid:
        print invalid[count]
        count += 1

    saveToFile()

    print "Complete."
    raw_input ('Press the Enter key to exit')

    
main()
