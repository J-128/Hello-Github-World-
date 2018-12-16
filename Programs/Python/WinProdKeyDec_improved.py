#!/usr/bin/env python
import sys, os ##Import required modules

##Try to import the 'Python-Registry' module, so we can actually work with the Windows registry...
try:
  from Registry import Registry
except ImportError: ##If it fails to import, inform the user so, suggest corrective steps to take, and exit.
  print("Error: You must install the 'python-registry' module. Try `pip install python-registry`.")
  sys.exit(-1) 

##Ask for the path to Windows' root...
winRootPath = input("Please enter the path to the root of the drive where Windows is installed, followed by a forward slash: ")

print()
print("OK, testing if path is good...") ##Inform the user what's going on...
print(winRootPath)

##Test if the path exists, and points to a valid Windows install...
if os.path.exists(winRootPath + "Program Files"):
  print("...Okay, path exists!") ##If so, inform the user that we have succeeded!
  print()
else: #And if not, tell the user so, and exit.
  print("Error: Path either does not exist, or is not a valid Windows installation.  Check your input and try again.")
  sys.exit(1)
  
##Ask the user to identify the Windows version, because apparently different versions store the hives in different places.
winVer = input("If your Windows version is 7 or earlier, enter 0. Otherwise, enter 1: ")

##Test for / find the correct case for the path to the 'software' hive...
if winVer == "0":
  try:
    reg = Registry.Registry(winRootPath + "WINDOWS/system32/config/software")
  except:
    try: 
      reg = Registry.Registry(winRootPath + "WINDOWS/system32/config/SOFTWARE")
    except:
       try:
         reg = Registry.Registry(winRootPath + "WINDOWS/System32/config/software")
       except:
         try:
           reg = Registry.Registry(winRootPath + "WINDOWS/System32/config/SOFTWARE")
         except:
           try:
             reg = Registry.Registry(winRootPath + "Windows/System32/config/software")
           except:
             try:
               reg = Registry.Registry(winRootPath + "Windows/System32/config/SOFTWARE")
             except:
               try:
                 reg = Registry.Registry(winRootPath + "Windows/system32/config/software")
               except:
                 reg = Registry.Registry(winRootPath + "Windows/system32/config/SOFTWARE")

elif winVer == "1":
  reg = Registry.Registry(winRootPath + "Windows/System32/config/RegBack/SOFTWARE")
else: ##If the user enters invalid input, inform them of such and exit
  print("Error: Bad input. You must type either 0 or 1.")
  sys.exit(2)

##We now have the path (Hopefully!), so we can do the decoding!  And no, I don't understand this step. At all. :(
key = reg.open("Microsoft\Windows NT\CurrentVersion")
did = bytearray([v.value() for v in key.values() if v.name() == "DigitalProductId"][0])
idpart = did[52:52+15]
charStore = "BCDFGHJKMPQRTVWXY2346789";
productkey = "";
for i in range(25):
  c = 0
  for j in range(14, -1, -1):
    c = (c << 8) ^ idpart[j]
    idpart[j] = c // 24
    c %= 24
  productkey = charStore[c] + productkey
print()
print("Product Key: " + '-'.join([productkey[i * 5:i * 5 + 5] for i in range(5)]))
