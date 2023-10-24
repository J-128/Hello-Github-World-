# About my programs here

Okay, each program that I decide to share here will have its own section in this document, detailing what it does, how it's used, etc.  So, let's begin!

### VBinDiffGui.py
This program is a graphical frontend to the very good vbindiff Binary Diff program.  My script uses nothing but the tkinter module along with the filedialog and messagebox submodules, the os module, and built-in python commands, so it should be easy to run on just about any *Linux* system.  The reason I wrote this is because, as much as I like vbindiff, because it's a terminal program, I didn't like having to type the *complete paths* to the files I wanted to compare on the command line.  With this little GUI application, you still have the option to type out the full paths to the files you want to compare, or you can just browse for them using the graphical interface, which makes things a lot easier and more user-friendly.  This program has some error checking;  it will give you an error message if you enter a path that doesn't exist, or if the path is to a directory.  I may add some screenshots of it in action at a later date.

_Warnings/tips:_ This program was developed on and for Linux, so it _Will Not Work_ for Windows users.  It relies on the vbindiff binary being at /usr/bin/vbindiff, so if you have vbindiff installed somewhere else, you'll either have to modify the program, or add a link/symlink to it in the previously given path.  Of course, this is all assuming anyone will actually find, let alone actually _use_ this program...

### WinProdKeyDec_improved.py
This _command line_ program basically just tells you what your Windows product key is.  It's pretty basic.  I adapted this from a Python script that someone shared _somewhere_.  I can't remember who authored it, or where they shared it, so my appologies. I don't own the actual decoding routine.  This program _should_ work for either Linux or Windows users, but it has only been tested on Linux, so I can't make any promises.  It should work for any version of Windows, but I have only tested it with XP and 7.  If it doesn't work for you, you can always file a bug report in the issue tracker. :D

_Warnings/tips:_ None? I can't think of any...

### DeCVS.py
This CLI script was created as a result of _Gigaleak II_, which happened on 7/25/20.  _Hopefully_ what it does is walk trough a directory tree, creating copies of all the *\*,v* files with the CVS metadata removed and the ",v" removed from the filename.

_Warnings/tips:_ I have only tested this on a few of the leaked files; I can't guarantee it works for any other CVS repository.  Also, it should be noted that if the (as I probably incorrectly called it) ending semaphore is not found, the output _should_ (although I can guarantee nothing) be the file with only the starting metadata removed.  This program should be considered a public alpha; I haven't tested it very thoroughly, and I hardly know if it works!

### xmlparse.py
Okay, you can call me ridiculous, but I decided to write this script becuase I couldn't figure out how to use Python's built-in XML-parsing library, I had a use for an XML parser, and I've been told the built-in one doesn't work very well.  You should just be able to import and use this like any other module.  It depends on Python 3(.8 is the version I developed it in) and the built-in `re` module, but nothing else.

_Warnings/tips:_  This is UNFINISHED, WORK-IN-PROGRESS software.  Do not expect clean code, good functionality, and flawless operation.  Really, at this point, the only thing I'd recommend actually _doing_ with it is perhaps trying to improve it.  The *most* basic functionality is _kind of_ there, but not much else.
