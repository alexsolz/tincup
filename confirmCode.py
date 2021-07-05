# This script will be responsible for rendering 

from ftplib import FTP
import time

def returnPassCode():
    '''
    This function will be responsible for ftping into the linux desktop server which will communicate with the passcode website and parse proper passcode data.
    '''

    # Log into target directory to the linux server.
    passCode = []
    targetDirectory = '/home/tincup/CS370_Team'
    ftp = FTP('192.168.1.31')
    ftp.login('tincup', 'tincup')
    ftp.cwd(targetDirectory)

    def readData(line):
        '''
        Helper function for downloading data via ftp.
        '''
        tmpLineData = line.split(' ')
        passCode.append(tmpLineData[1])

    # Download data from the linux server.
    ftp.retrlines('RETR pwInfo.txt', readData)

    # Only return passcode data when all three users have the same code. This is to prevent any potential gaps caused by time difference.
    if len(passCode) == 3 and (passCode[0] == passCode[1] and passCode[0] == passCode[2] and passCode[1] == passCode[2]):
        print(passCode)

        ftp.quit()
        return passCode

#try:
#    while True:
#        returnPassCode()
#        time.sleep(2)

#except KeyboardInterrupt:
#    print("Done!")