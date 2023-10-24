#XMLParse.py:  A custom XML parsing library, since I don't understand the built-
#  in one and people say it doesn't work very well.
#
#  Methods:
#   Not implemented:
#    WriteXML: Write out an XML file from a list of XMLements
#      Returns: ???
#   WIP:
#    readFile: Read in an XML file and parse it
#      Returns: Return value of toXMLements; should be LIST of XMLements if successful
#    toXMLements:  Parse a string of XML into a list of XMLements
#      Returns:  LIST of XMLelements, or None on failure
#    XMLement.toXML: Convert the XMLement to the XML text
#      Returns: String

class XMLement:
    '''This class represents a single element of XML.  An 'element' consists of three
parts:
    Name:
        Every XMLement has a name.  In this example:
            <element1>
                <element2 />
            </element1>
        the XMLement names are, of course, 'element1' and 'element2'.  We store Name
        as a string.
    Properties:
        Any XMLement can have 0 or more 'Properties'.  For instance, going to HTML,
        consider
            <div align="center" style="color:red">
        The XMLement Name is "div", and it has two properties: "align='center'" and
        "style='color:red'".  We store Properties as a dictionary, empty if there are
        none.
    Contents:
        Most XMLements contain something. Usually text (E.G.
            <element>Element text!</element>
        ) and/or other elements (E.G.
            <element><subelement /></element>
        ).  We store Contents as a list of strings and XMLements, or in the case of
        an empty tag (such as <subelement> in the example above), as NoneType.'''

    def __init__(self, name="", props={}, contents=None):
        #Test for validity:
        if type(name) is not str: #Name is string
            raise TypeError("XMLement Name must be a string")
        self.name = name

        if type(props) is not dict: #Props is dictionary
            raise TypeError("XMLement Properties must be expressed as a dictionary")
        self.props = props

        if type(contents) in (list, tuple): #Contents is list/tuple...
            for v in contents:
                if type(v) not in (str, XMLement): #Of strings/XMLements
                    raise TypeError("XMLement Contents may only consist of strings and/or other XMLements")
        elif contents is None: #...Or None
            pass
        else:
            raise TypeError("XMLement Contents must be expressed as a list/tuple")
        self.contents = contents

    '''Context:
        Elements can be embedded in elements, like
            <element1>
                <element2 />
            </element1>
        'Context' is where we are.  The context of <element2> in the above is, of
        course, <element1>.  We store Context as a list of strings, or as an empty
        list if the element is toplevel.'''

    ###

    def __str__(self):
        return self.toXML('\n')

    ###

    def __repr__(self):
        return f"XMLement('{self.name}', {self.props}, {self.contents})"
    
    ###
    
    def toXML(self, sep=""):
        '''Return the actual XML representation of an XMLement
        Return type: Str'''

        def _propsToStr():
            propsStrs = []
            for k, v in self.props.items():
                propsStrs.append("=".join([str(k), str(v)]))
            return " ".join(propsStrs)

        def _contentsToStr(sep=sep):
            cStrs = []

            for i in self.contents: #Iterate through the contents...
                if type(i) is str: #...Just appending them if they're strings...
                    cStrs.append(i)
                else: #...or converting them to XML text, if they're XMLements
                    cStrs.append(i.toXML())
            return sep.join(cStrs) #Join them up and return them

        #Returns
        if self.contents is None: #Empty (content-less) tag; format appropriately, and return
            if len(self.props) == 0:
                return f"<{self.name} />{sep}"
            else:
                return f"<{self.name} {_propsToStr()} />{sep}"
        else: #Non-empty tag; format and return like before
            if len(self.props) == 0:
                return f"<{self.name}>{sep}{_contentsToStr()}{sep}</{self.name}>"
            else:
                return f"<{self.name} {_propsToStr()}>{sep}{_contentsToStr()}{sep}</{self.name}>"


################################
            
def readFile(pathToXML):
    '''Open path 'pathToXML' and process it to be parsable by toXMLements()''' 

    #Verify that we ARE trying to open an "XML", for basic idiot-proofing.
    #  Obviously, anyone can rename any file to end with .xml to make this code not
    #  complain, but if you're doing that, you're actively TRYING to break things.
    #  At that point, you deserve any problems that causes.
    if not pathToXML.lower().endswith(".xml"): raise NameError("PathToXML must must be a path to a .XML file")

    lines = []  
    
    with open(pathToXML) as f:
        try:
            firstLine = f.readline()
            if not (firstLine.startswith("<?xml") and firstLine.endswith("?>\n")):
                raise Warning("File does not appear to be a proper XML")
        except Warning as w:
            print("Proceed with caution; encountered Warning: {0}".format(w))
        except:
            print("Unhandled error:")
            raise
        finally:
            f.seek(0,0)
        
        
        for l in f:
            #Strip whitespace and line-delimiters, and add the lines to the LINES list
            l = l.lstrip()
            lines.append(l.rstrip("\n"))

    linesStr = "".join(lines) #Compile all lines into a single string, for easier tag-matching

    return toXMLements(linesStr) #Feed the XML data to the parser, return the output


################################

def toXMLements(inStr): #The main parser
    """Convert a string of XML into a list of XMLements"""

    import re as regex
    
    #Regex strs:
    #  Tag properties: r'(?P<prop>\s\S+)=(?P<val>[^>\s\?]+)'
    #  Full tags: r'<.*?>'
    #  Opening tags: r'<[^/]+>'
    #  Closing tags: r'</.+?>'
    #  Tag names: r'<(?P<name>[^\s>]+)'
    #    NOTE: Matches closing tags, too
    #  Comment tags: r'<!--.*-->'
    #  Processing instructions: r'<\?.*\?>'
    #  Tag and contents: r'<(?P<name>[^\s>]*)((?P<prop>\s\S+)=(?P<val>[^>\s\?]+))*>(?P<contents>.*)</(?P=name)>'
    #    Also r'<(?P<name>[^\s>]*) ?(?P<propsField>[^>]*)>(?P<contents>.*)</(?P=name)>'
    #      Note that the latter needs post-processing to extract the individual props/vals

    P_tag_properties = r'(?P<prop>\s\S+)=(?P<val>[^>\s\?]+)'
    P_tags_full = r'<.*?>'
    P_tags_opening = r'<[^/]+>'
    P_tags_closing = r'</.+?>'
    P_tag_names = r'<(?P<name>[^\s>]+)'
    P_tags_comments = r'<!--.*-->'
    #P_tag_with_contents = r'<(?P<name>[^\s>]*) ?(?P<propsField>[^>]*)>(?P<contents>.*)</(?P=name)>' ##Older regex; would not match empty tags
    P_tag_with_contents = r'<(?P<name>[^\s>]*) ?(?P<propsField>[^>]*)( />|>(?P<contents>.*)</(?P=name)>)'

    #Get a list of tagnames in the string
    tagsByName = []
    for m in regex.findall(P_tag_names, inStr):
        if m.startswith("?"): #Processing instruction, not tag; ignore
            continue

        #We could also ignore comments (<!-- {text} -->) here, but for now, we'll not.
        
        if not m.startswith("/"): #At the moment, we're only interested in opening tags
            tagsByName.append(m)

    #From that list, generate a list of UNIQUE tagnames, so we know what we're looking
    #  for when we're actually parsing the string into a list of XMLements
    #
    #Note that we /could/ collapse this code into the tagsByName loop, but a list of every
    #  tag name /COULD/ potentially be useful, so /for now/, we'll not.
    uniqueTags = []
    for t in tagsByName:
        if not t in uniqueTags:
            uniqueTags.append(t)


    #That done, we can finally begin! (Right?)
    tags = [] #The list that will hold the XMLements


    #print(uniqueTags) ##DEBUG


    for t in uniqueTags:
        strOffs = -1 #We'll need to run S.find() multiple times to collect every instance
                     #  of a given tag.  Thus, we'll need to store each offset (in the string)
                     #  where the tag is found, so we can pass that (plus 1) in as
                     #  S.find's 'start' argument each time.
                     #We use strOffs + 1 each time so we don't sit and match the same
                     #  tag ad infinitum; thus, it is necessary to initialize it to -1
                     #  so we don't miss the first tag (I.E. the tag at Offset 0).

        ctr = 0 #Counter variable, incremented for each opening instance of T, decremented
                #  for each closing

        #Offset lists so we know where each instance of T starts/ends 
        openingOffsets = []
        closingOffsets = []
    
        while True:
            strOffs = inStr.find(f"<{t}", strOffs+1) #S.find each tag matching T
            if strOffs == -1: break #No more matching tags; exit loop

            #nextStrOffs = inStr.find(f"<{t}", strOffs+1) ##Shouldn't be necessary, right?

            tagCloseOffs = inStr.find(f"</{t}>", strOffs) #S.find a closing tag for T
            if tagCloseOffs == -1: #No closing tag found!  Perhaps it's an empty tag? (E.G. <nullTag /> )
                #TODO: Actually HANDLE THIS, rather than just print a warning!
                print("Warning! No closing tag found!")
                pass

            openingOffsets.append(strOffs)
            closingOffsets.append(tagCloseOffs)

        print(openingOffsets, closingOffsets)

        for idx, ofs in enumerate(openingOffsets): #Iterate through the offsets list;

            #Find the correct case to execute
            if idx + 1 == len(openingOffsets): #We cannot do the three-part compare;
                #Instead, do a simpler (but less safe) compare
                if ofs < closingOffsets[idx]: #Everything's good;
                    case = 1 #Tag closes normally
                else: #Otherwise,
                    case = -1 #We've got a problem.
            else: #We can do the safer, three-part test-compare
                if ofs < closingOffsets[idx] < openingOffsets[idx+1]: #So do it
                    case = 1 #Tag ends before next instance begins
                elif ofs < closingOffsets[idx] > openingOffsets[idx+1]: #Case 2: Another instance of T begins within the instance being parsed
                    case = 2 #New T instance begins before current one closes 
                else: #Something's weird;
                    case = -1 #We've got problems! (Fortunately, you don't have to jump... yet. :P XD)

            #Now, execute it!
            if case == 1: #Normal

                #Slice inStr to get the full tag/contents
                fullTag = inStr[
                    ofs: #Slice start
                    closingOffsets[idx] + len(f"</{t}>") #Slice end
                    ]###

                ctr += 1 #Increment counter
                
                #And now, process that tag into a valid XMLement
                m = regex.match(P_tag_with_contents, fullTag, regex.DOTALL) #Use a regex to extract tag name, properties, and contents
                
                if not m: #Error case; should never happen
                    raise IOError("Regex failed to match the tag <{0}> at Offset {1}".format(t, offs))

                #Collect parameters to initialize XMLement with
                n = m.group("name") #Tagname
                p = {} #Properties dict
                if len(m.group("propsField")) > 0: #Have we properties?  If so...
                    for prop in m.group("propsField").split(" "): #...Split apart the properties...
                        k, v = prop.split("=") #...Find each key and its value...
                        p.setdefault(k, v) #...and append them to the dictionary
                c = m.group("contents") #Contents

                #Post-process C, since at this point, it's just a string
                cl = [] #List to hold processed Contents
                cm = regex.search(P_tag_with_contents, c, regex.DOTALL)
                if cm: #C contains XML; process into XMLements
                    pass #Somehow
                    for e in toXMLements(c): #Feed C to the parser and iterate through the resultant list,
                        cl.append(e) #adding each result to the list used to initalize the current XMLement?
                else: #C is only a string (or nothing); add to the Contents list
                    cl.append(c) #Hope this is right...

                tags.append(XMLement(n, p, cl))

                ctr -= 1
            ##End Case 1

            elif case == 2: #T instance embedded in T
                pass
            ##End Case 2

            elif case == -1: #Error
                raise IOError(f"Problem parsing instance {idx+1} of tag <{t}> starting at Offset {ofs}.")

        """if tagCloseOffs < nextStrOffs: #Tag closes before next one begins; thus...
            '''ctr -= 1 #Decrement counter,
            fullTag = inStr[strOffs:tagCloseOffs+len(f"</{t}>")] #Extract full tag/contents,

            #And now, process that tag into a valid XMLement


            #print(ctr, strOffs, nextStrOffs, tagCloseOffs, fullTag) ##DEBUG
            
            
            m = regex.match(P_tag_with_contents, fullTag, regex.DOTALL) #Use a regex to extract tag name, properties, and contents
            
            if not m: #Error case; should never happen
                raise IOError("Regex failed to match the tag <{0}>".format(t))

            #Collect parameters to initialize XMLement with
            n = m.group("name") #Tagname
            p = {} #Properties dict
            if len(m.group("propsField")) > 0: #Have we properties?  If so...
                for prop in m.group("propsField").split(" "): #...Split apart the properties...
                    k, v = prop.split("=") #...Find each key and its value...
                    p.setdefault(k, v) #...and append them to the dictionary
            c = m.group("contents") #Contents
                                    #  Just a string; needs post-processing
            #Thus, post-process it!
            cl = [] #List to hold processed Contents
            cm = regex.search(P_tag_with_contents, c, regex.DOTALL)
            if cm: #C contains XML; process into XMLements
                pass #Somehow
                for e in toXMLements(c): #Feed C to the parser and iterate through the resultant list,
                    cl.append(e) #adding each result to the list used to initalize the current XMLement?
            else: #C is only a string (or nothing); add to the Contents list
                cl.append(c) #Hope this is right...

            tags.append(XMLement(n, p, cl))'''

        else: #Tag either A) does NOT close before the next one begins, or B) is the last/only instance
            print(f"Alert while parsing tag <{t}>! Tag does not close before next one begins.\n\tStrOffs:{strOffs} nextStrOffs:{nextStrOffs} tagCloseOffs:{tagCloseOffs} ctr:{ctr}\n")
            pass #REMINDER: Actually handle this!
        """
                



    return tags



            
