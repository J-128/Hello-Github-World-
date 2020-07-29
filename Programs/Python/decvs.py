#DeCVS:  This script (theoretically) will traverse a directory tree, removing
#  the CVS metadata from each file.

#NOTES: Semaphore marking end of starting metadata is '40 0A 74 65 78 74 0A 40'
#  Semaphore marking end of file data (and start of ending metadata) is '40 0A 0A 0A 31 2E 31 2E 31 2E 31 0A 6C 6F 67 0A'

import os, time

treeroot = input("Please enter the complete path to the directory at the root of the CVS Repo: ")
filesFound = [] #A list to store all files found

print("Beginning walk... ", end="")
startTime = time.time() #Store the time the walk began, for elapsed time calculation

#Copied (with changes) from an online example
for dirpath, dirnames, files in os.walk(treeroot):
    for name in files:
        if name.endswith(",v"):
            filesFound.append(os.path.join(dirpath, name))
##

endTime = time.time() #Store the time the walk ended

print("Walk finished with {0} results in {1} seconds".format(len(filesFound), endTime - startTime))
showResults = input("Show results? Y/N ")

if showResults.upper().startswith("Y"):
    print(filesFound)

print()
input("Press Enter to continue. Warning, this may take a long, LONG time!") #Courtesy warning

print("De-CVS process started.  Please wait... ", end="")
startTime = time.time()

for file in filesFound: #Now, iterate through every file found, so we can make the necassary edits
    inFile = open(file, "br")

    #There HAS to be a better way to do this, but I sadly don't know it.
    while not inFile.read(8) == b'\x40\x0A\x74\x65\x78\x74\x0A\x40':
        inFile.seek(-7, 1) #Seek back 7 bytes from the stream position (designated by the 1) so we can rerun the search

    #Now, theoretically, when the loop exits, the stream position will be right at
    #    the start of the actual file data.  Therefore, we store this offset.
    print("Data Start found at offset {}".format(hex(inFile.tell())))
    dataStart = inFile.tell()

    #Now, do basically the same thing, but search for the ending semaphore.
    while not inFile.read(16) == b'\x40\x0A\x0A\x0A\x31\x2E\x31\x2E\x31\x2E\x31\x0A\x6C\x6F\x67\x0A':
        inFile.seek(-15, 1)

    inFile.seek(-16, 1) #Seek back 16 bytes so we don't include the data-end semaphore
    print("Data end found at offset {}".format(hex(inFile.tell())))
    dataEnd = inFile.tell()

    #Now, start writing the de-CVS'd file!
    outFile = open(file.rstrip(",v"), "bw") #Open the output file
    print("Output file opened")

    inFile.seek(dataStart) #Seek to the start of the data
    
    print("Writing... ", end="")
    while inFile.tell() != dataEnd:
        outFile.write(inFile.read(1)) #Funny, the actual data-writing is the simplest piece of code.

    #When that loop finishes, if everything worked, we have the complete de-CVS'd file!  Now, close the handles, and move on the the next.
    print("Done.")
    print("Closing... ", end="")

    outFile.close()
    inFile.close()

    print("Done. Moving to next file...")
endTime = time.time()

print("Operation finished in {0} seconds. (Do the math yourself if you want a different time unit. :P)".format(endTime - startTime))
