#mailTester 

README:

	This program was intended to test multiple email addresses exported from Microsoft Outlook in CSV format.
	
	PRECONDITIONS:
	
		Requires a valid CSV file from either:
			--Outlook 2010
			--Outlook 2013
		To get a valid file you need to go to export, then export to a file, then comma seperated values, then click contacts, then chose location to save the
		file to, then click map custom fields and clear map, then drag email from the left box to the right. This program will only work if all that you export 
		is the email address. It can not process any other information.
	
	POSTCONDITIONS:
	
		Outputs emails in shell as it reads them.
		Creates 3 files:
			--valid.txt : emails that are listed here are definitely real emails 
			--invalid.txt: emails here are either invalid or the server does not support email validation
			--errors.txt: error messages are listed here along with the email that caused the problem and a timestamp
			
	BUGS:
		Doesn't support Outlook 2010 yet and has bugs when reporting errors