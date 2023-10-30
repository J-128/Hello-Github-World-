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

    def __init__(self, name="", props={}, contents=None, *, _parent=None):
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
        self._parent = _parent

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
        return self.toXML('\n') + f"\t\tID: {id(self)}\t\tParent ID: {id(self._parent)}\n"

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
    
    with open(pathToXML, errors='surrogateescape') as f:
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

def toXMLements(inStr, parentElement=None, depth=0): #The main parser
    """Convert a string of XML data into a list of XMLements
    parentElement, if given, specifies the XMLement within which the current set of tags
    (inStr) is contained"""

    if parentElement is not None and type(parentElement) is not XMLement:
        raise TypeError("ParentElement, if specified, must be an XMLement")

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

    tags = [] #The list that will hold the XMLements

    #Get a list of tagnames in the string
    tagsByName = []
    for m in regex.findall(P_tag_names, inStr):
        if m.startswith("?"): #Processing instruction, not tag; ignore
            continue

        #We could also ignore comments (<!-- {text} -->) here, but for now, we'll not.
        
        if not m.startswith("/"): #At the moment, we're only interested in opening tags
            tagsByName.append(XMLement(m, _parent=parentElement)) #Create a list of the XMLements in the input.
                                           #  For now, we're just storing the tagname.
                                           #  We'll figure out the props/contents later.

    #Offset lists so we know where each instance of T starts/ends 
    openingOffsets = [0]
    closingOffsets = [0]
    
    for t in tagsByName:
        strOffs = inStr.find(f"<{t.name}", openingOffsets[-1]) #S.find each tag matching T

        tagCloseOffs = inStr.find(f"</{t.name}>", strOffs) #S.find a closing tag for T
        if tagCloseOffs == -1: #No closing tag found!  Perhaps it's an empty tag? (E.G. <nullTag /> )
            #TODO: Actually HANDLE THIS, rather than just print a warning!
            print("Warning! No closing tag found!")
            pass

        openingOffsets.append(strOffs)
        closingOffsets.append(tagCloseOffs)
    else:
        #Since the lists were initialized to [0] (so we could use the last item
        #  as S.find()'s starting offset), remove this first value from each
        #  once we're out of tags
        openingOffsets.pop(0)
        closingOffsets.pop(0)

    #That done, we can finally begin! (Right?)
    ctr = depth #Counter variable, incremented for each opening instance of T, decremented
            #  for each closing

    #_element = XMLement(_parent=parentElement) #The XMLement we're working on processing out

    ##DEBUG
    print("\t"*depth, "---------------")
    print("\t"*depth, openingOffsets)
    print("\t"*depth, closingOffsets)
    print("\t"*depth, tagsByName)
    print("\t"*depth, "---------------")
    #print(tagsByName)-len(openingOffsets))
    #######

    for idx, (t, oOfs, cOfs) in enumerate(zip(tagsByName, openingOffsets, closingOffsets)): #Iterate through the offsets list;
        
##        ##DEBUG
##        print("\t"*depth, "-----------")
##        print("\t"*depth, idx, repr(t), oOfs, cOfs)
##        print("\t"*depth, "-----------")
##        #######

        if cOfs > oOfs: #Normal situation
            #Slice inStr to get the full tag/contents
            fullTag = inStr[
                oOfs: #Slice start
                cOfs + len(f"</{t.name}>") #Slice end
                ]###

            ctr += 1 #Increment counter

##            ##DEBUG
##            print("\t"*depth, "-------")
##            print("\t"*depth, fullTag)
##            print("\t"*depth, "-------")
##            #######

            
            #And now, process that tag into a valid XMLement
            m = regex.match(P_tag_with_contents, fullTag, regex.DOTALL) #Use a regex to extract tag name, properties, and contents
            
            if not m: #Error case; should never happen
                raise RuntimeError("Regex failed to match the tag <{0}> at Offset {1} of input {2}".format(t.name, oOfs, inStr))

            #Collect parameters to initialize XMLement with
            n = m.group("name") #Tagname; Actually irrelevant, as we created the correct NAME for each XMLement at the top of the function
            p = {} #Properties dict
            if len(m.group("propsField")) > 0: #Have we properties?  If so...
                for prop in m.group("propsField").split(" "): #...Split apart the properties...
                    k, v = prop.split("=") #...Find each key and its value...
                    p.setdefault(k, v) #...and append them to the dictionary
            c = m.group("contents") #Contents; Needs post-processing, as it's just
                                    #  a string at this point.          
            t.props = p
            t.contents = c

            ##DEBUG
            print("\t"*depth, "-----")
            print("\t"*depth, id(t), '\t', repr(t), '\t\t', id(t._parent), '\t', repr(t._parent))
            print("\t"*depth, "-----")
            #######

            tags.append(t) #...and append it!  We now have a partial result; each
                           #  tag in in the list with its properties, and contents
                           #  as a string.  Step 2 will be to convert that string
                           #  into XMLements where required.

            ctr -= 1 #Decrement counter

        else: #Error
            raise RuntimeError(f"Problem parsing instance {idx+1} of tag <{t.name}> starting at Offset {oOfs} in input string {inStr}.")


    ##Step 2: CONTENTS to necessary XMLements; resolve _parent(?)
    for t in tags:
        c = t.contents
        cl = [] #List to hold processed Contents
        cm = regex.search(P_tag_with_contents, c, regex.DOTALL)
        if cm: #C contains XML; process into XMLements
            for e in toXMLements(c, t, ctr): #Feed C to the parser and iterate through the resultant list,
                cl.append(e) #adding each result to the list used to initalize the current XMLement?
        else: #C is only a string (or nothing); add to the Contents list
            cl.append(c) #Hope this is right...

        ##DEBUG
        print('\t'*depth, cl)
        #######
        
        t.contents = cl
        


    return tags



            
