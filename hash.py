import os
import hashlib
import stat
import time

# https://thispointer.com/python-how-to-get-last-access-creation-date-time-of-a-file
# https://www.tutorialspoint.com/python/os_walk.htm
# https://www.w3resource.com/python-exercises/python-basic-exercise-3.php
# https://docs.python.org/3/library/hashlib.html
# https://stackoverflow.com/questions/5498276/iterating-over-os-walk-in-linux
# https://www.pythonpool.com/python-sha256

# Variables
originalHashFile = ""
newHashFile = ""

# Present Multiple Options for the User: If it is their first time or their second time
print("Options:"+"\n\t(1) Make Original Hash\n\t(2) Make New Hash and Compare with Old")
userChoice = input("Select Your Option: ")

#Making the original hash
if(userChoice == '1'):
    originalHashFile = input("Enter Original Hash File Name: ")
    with open('./'+originalHashFile,'w') as F:
        #For Testing we will use '.' as the starting point, but for full system  we will use '/'
        for root,dirs,files in os.walk(".",topdown=False): #Change to '/'
            for name in files:
                #Checking if there is any unhashable/ignorable file/directory
                if(('/dev' in root) or ('/proc' in root) or ('/run' in root) or ('/sys' in root) or ('tmp' in root) or ('/var/lib' in root) or ('/var/run' in root)):
                    next
                else:
                    #We will open the file (if it is a file) and read in the data as bytes
                    with open(os.path.join(root,name),'rb') as textInfo:
                        actualText = textInfo.read()
                        encoded = actualText
                        #Hash the bytes
                        result = hashlib.sha256(encoded).hexdigest()
                        #We need to get the access date
                        fileStatsObj = os.stat(os.path.join(root,name))
                        accessTime = time.ctime(fileStatsObj[stat.ST_ATIME])
                        #This will write the following for each file (i.e. <file> <accessTime> <hash>)
                        F.write((os.path.join(root,name)+"\t"+str(accessTime)+"\t"+str(result)+"\n"))
                        print(os.path.join(root,name))
                    textInfo.close()
            #Same method for directories as explained using comments above
            for name in dirs:
                if(('/dev' in root) or ('/proc' in root) or ('/run' in root) or ('/sys' in root) or ('tmp' in root) or ('/var/lib' in root) or ('/var/run' in root)):
                    next
                else:
                    encoded = (os.path.join(root,name)).encode()
                    result = hashlib.sha256(encoded).hexdigest()
                    fileStatsObj = os.stat(os.path.join(root,name))
                    accessTime = time.ctime(fileStatsObj[stat.ST_ATIME])
                    F.write((os.path.join(root,name)+"\t"+str(accessTime)+"\t"+str(result)+"\n"))
                    print(os.path.join(root,name))
    F.close()

#User already created the hash and we want to compare
elif(userChoice == '2'):
    originalHashFile = input("Enter Original Hash File Name: ")
    newHashFile = input("Enter New Hash File Name: ")
    summaryFile = "./summary.txt"
    originalFileData = []
    newFileData = []
    #Try-catch in case it fails to find the original hash file
    try:
        with open("./"+originalHashFile,'r') as F:
            originalFileData = F.readlines()
        F.close()
    except:
        print("You never created this file or you have not entered the name correctly.")
    # First Create the New Hash File
    # Same steps as outlined above (checking for unhashable files/dirs, hash, access time, etc)
    with open('./'+newHashFile,'w') as F:
        for root,dirs,files in os.walk(".",topdown=False): #Change to '/'
            for name in files:
                if(('/dev' in root) or ('/proc' in root) or ('/run' in root) or ('/sys' in root) or ('tmp' in root) or ('/var/lib' in root) or ('/var/run' in root)):
                    next
                else:
                    with open(os.path.join(root,name),'rb') as textInfo:
                        actualText = textInfo.read()
                        encoded = actualText
                        result = hashlib.sha256(encoded).hexdigest()
                        fileStatsObj = os.stat(os.path.join(root,name))
                        accessTime = time.ctime(fileStatsObj[stat.ST_ATIME])
                        F.write((os.path.join(root,name)+"\t"+str(accessTime)+"\t"+str(result)+"\n"))
                        print(os.path.join(root,name))
                    textInfo.close()
            for name in dirs:
                if(('/dev' in root) or ('/proc' in root) or ('/run' in root) or ('/sys' in root) or ('tmp' in root) or ('/var/lib' in root) or ('/var/run' in root)):
                    next
                else:
                    encoded = (os.path.join(root,name)).encode()
                    result = hashlib.sha256(encoded).hexdigest()
                    fileStatsObj = os.stat(os.path.join(root,name))
                    accessTime = time.ctime(fileStatsObj[stat.ST_ATIME])
                    F.write((os.path.join(root,name)+"\t"+str(accessTime)+"\t"+str(result)+"\n"))
                    print(os.path.join(root,name))
    F.close()
    # Compare It and Make the Summary File
    with open("./"+newHashFile,'r') as F2:
        newFileData = F2.readlines()
    F2.close()
    # Check which lines are in both
    finalOGFileData = []
    finalNewFileData = []
    # What we are accomplishing is a list with each line; each line then breaks into an array with 3 items
    # This makes it easier to traverse through the array
    for item in originalFileData:
        finalOGFileData.append(item.split('\t'))
    for item in newFileData:
        finalNewFileData.append(item.split('\t'))
    removedLines = []
    # We want to see which files are already in both and can therefore be removed as potential missing or new
    for line in finalOGFileData:
        for line2 in finalNewFileData:
            if(line[0]==line2[0] and line[2]==line2[2]):
                removedLines.append(line2[0])
    realFinalOGFileData = []
    realFinalNewFileData = []
    # We need to check if it was in the removed array
    for line in range(0,len(finalOGFileData)):
        if(finalOGFileData[line][0] in removedLines):
            next
        else:
            # This would mean that it is not in the removed list
            realFinalOGFileData.append(finalOGFileData[line])
    for line in range(0,len(finalNewFileData)):
        if(finalNewFileData[line][0] in removedLines):
            next
        else:
            realFinalNewFileData.append(finalNewFileData[line])
    # Now check if missing or new
    # If missing, then file still in originalFileData
    # If new, then file in newFileData
    with open(summaryFile,'w') as FSum:
        for line in finalOGFileData:
            for line2 in finalNewFileData:
                if(line[0]==line2[0] and line[2]!=line2[2] and not str.__contains__(line[0],originalHashFile)):
                    # Now know that the file was changed
                    FSum.write("Modified File: "+line[0]+"\n")
                    realFinalOGFileData.remove(line)
        # We have identified that the original hash file is being edited since it is removing
        # Therefore, we se tthe conditional to ignore
        for line in realFinalNewFileData:
            if not str.__contains__(line[0],originalHashFile):
                FSum.write("New File: "+line[0]+" "+line[2])
        for line in realFinalOGFileData:
            if not str.__contains__(line[0],originalHashFile):
                FSum.write("Missing File: "+line[0]+" "+line[2])
    FSum.close()

else:
    print("Enter a viable option")
    exit()


