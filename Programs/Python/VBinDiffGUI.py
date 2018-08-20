#!/usr/bin/python3
##VBinDiffGUI:  A graphical frontend for the 'Vbindiff' binary diff program.
import tkinter, tkinter.messagebox, tkinter.filedialog
import os


##Firstly, define the callback function for the button
def beginDiff():
    """Function that actually calls VBinDiff.""" #Description line (absolutely unnecessary)

    #Assign file1Path and file2Path to a couple of local vars, so we don't have confusing calls to [x].get() in the command lines
    file1PathL = file1Path.get()
    file2PathL = file2Path.get()

    if file2PathL == "": #If you have entered NOTHING for File2...

        if not os.path.exists(file1PathL): #...Test for the existance File 1...
            #If it fails, display an error message and blank the entry box
            f1Err = tkinter.messagebox.showerror("File 1", "The specified file was not found.  Re-check your path to File 1 and try again.")
            file1Path.set("")

            return f1Err
        else: #And if it succeeds...

            if os.path.isdir(file1PathL): #Make sure it is a FILE, not a directory.
                f1Err = tkinter.messagebox.showerror("File 1", "The specified path is a directory.  Enter a path to a file instead.")
                return f1Err
            else: #If it is a file...
                print("Success!")
                os.execl("/usr/bin/vbindiff", "", file1PathL) #...Proceed to execute vbindiff with just 1 argument!

    else: #Now, if you HAVE entered ANYTHING for File2...

        if not os.path.exists(file1PathL): #...First test for the existance of File 1...

            #If it fails, display an error message and blank the entry box
            f1Err = tkinter.messagebox.showerror("File 1", "The specified file was not found.  Re-check your path to file 1 and try again.")
            file1Path.set("")

            return f1Err

        else: #But if it succeeds...

            if os.path.isdir(file1PathL): #Make sure it is a FILE, not a directory.
                f1Err = tkinter.messagebox.showerror("File 1", "The specified path is a directory.  Enter a path to a file instead.")
                return f1Err
            
            if os.path.exists(file2PathL) == False: #...Proceed to test File 2's existance...
                f2Err = tkinter.messagebox.showerror("File 2", "The specified file was not found.  Re-check your path to File 2 and try again.") #If it fails, raise an error message
                file2Path.set("")

                return f2Err
            else: #But if not...

                if os.path.isdir(file2PathL): #Make sure it is a FILE, not a directory.
                    f2Err = tkinter.messagebox.showerror("File 2", "The specified path is a directory.  Enter a path to a file instead.")
                    return f2Err

                print("Success!")
                os.execl("/usr/bin/vbindiff", "", file1PathL, file2PathL) #...Proceed to execute vbindiff!

#Next, define the callback functions for the 'Browse...' buttons
def file1Browse():
    """The callback function for the file1Browse button.""" #Description line

    filePath = tkinter.filedialog.askopenfile(filetypes =[("All Files", "*")])
    file1Path.set(filePath.name) #Set the value of the File 1 Entry widget to the path to the file you just selected

def file2Browse():
    """The callback function for the file2Browse button.""" #Description line

    filePath = tkinter.filedialog.askopenfile(filetypes =[("All Files", "*")])
    file2Path.set(filePath.name) #Set the value of the File 2 Entry widget to the path to the file you just selected

##Okay, now begin defining widget variables!

win = tkinter.Tk() #Main window/widget

file1Path = tkinter.StringVar(win) #A tkinter StringVar to hold the contents of file1
file2Path = tkinter.StringVar(win) #Another tkinter StringVar to hold the contents of file2

#Set the previous vars to a default value
file1Path.set("Path to file 1")
file2Path.set("Path to file 2")

label1 = tkinter.Label(win, text="Please enter the FULL PATHS of the files you want to compare.") #Instructional text widget

file1 = tkinter.Entry(win, textvariable=file1Path) #Entry widget to enter file 1's path
file2 = tkinter.Entry(win, textvariable=file2Path) #Another entry widget to enter file 2's path
file1Label = tkinter.Label(win, text="File 1") #Label widget to label the file1 input box
file2Label = tkinter.Label(win, text="File 2") #Another label widget to label the file2 input box

file1BrowseBtn = tkinter.Button(win, text="Browse...", command=file1Browse)
file2BrowseBtn = tkinter.Button(win, text="Browse...", command=file2Browse)

beginBtn = tkinter.Button(win, text="Begin Diff", command=beginDiff, default=tkinter.ACTIVE) #Button widget

##Okay, done defining things. Now, let's start using our definitions!
win.title("VBinDiff: Select files...") #Set the window's title...
win.resizable(False, False) #...and resizability! (Is that even a word?)

##Now, begin gridding our widgets into the main window...
label1.grid(column=0, row=0, columnspan=5, sticky=tkinter.W, padx=5)
file1.grid(column=1, row=1, columnspan=4, sticky=tkinter.NSEW, padx=5, pady=3)
file1Label.grid(column=0, row=1, padx=3)
file1BrowseBtn.grid(column=5, row=1, padx=3)
file2.grid(column=1, row=2, columnspan=4, sticky=tkinter.NSEW, padx=5, pady=3)
file2Label.grid(column=0, row=2, padx=3)
file2BrowseBtn.grid(column=5, row=2, padx=3)

beginBtn.grid(column=5, row=3, padx=5, pady=5)

#And, finally: run the Tcl/Tk MainLoop
win.mainloop()
