#XMLParse.py:  A custom XML parsing library, since I don't understand the built-
#  in one and people say it doesn't work very well.
#
#  Methods:
#   Not implemented:
#    WriteXML: Write out an XML file from a list of XMLements
#      Returns: ???
#   WIP:
#    readFile: Read in an XML file and parse it
#      Returns:  Return value of toXMLements; should be LIST of XMLements if successful
#    toXMLements:  Parse a string of XML into a list of XMLements
#      Returns:  LIST of XMLelements, or None on failure
#   Probably done:
#    XMLement.toXML: Convert the XMLement to the XML text
#      Returns:  STRING
#    XMLement.contentsAdd: Add an arbitrary number of specified contents to the XMLement
#      Returns:  INT: New length of XMLement.contents
#    XMLement.contentsDel: Remove specified range of XMLement Contents
#      Returns:  INT: New length of XMLement.contents
#    XMLement.contentsPop: Remove and return specified range of XMLement Contents
#      Returns:  LIST of removed XMLement Contents


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
        ).  We store Contents as a tuple of strings and XMLements, or in the case of
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
        self.contents = tuple([contents])
        self._parent = _parent

    ###

    def __str__(self):
        return self.toXML('\n') + f"\t\tID: {id(self)}\t\tParent ID: {id(self._parent)}\n"

    ###

    def __repr__(self):
        return f"XMLement('{self.name}', {self.props}, {self.contents})"
    
    ###

    def __eq__(self, other):
        if type(other) is not XMLement:
            return NotImplemented
        else:
            if (
                self.name == other.name and
                self.props == other.props and
                self.contents == other.contents
                ):
                return True
            else:
                return False
        
    ###

    def contentsAdd(self, *newContents, idx=-1):
        '''Add the given NEWCONTENTS the XMLement's Contents at the index specified
        by IDX.  Any NEWCONTENT which is not an XMLement will be converted to a
        String.'''
        _contentsList = list(self.contents)

        for c in newContents:
            if type(c) is XMLement:
                _contentsList.insert(idx, c)
            else:
                _contentsList.insert(idx, str(c))

        self.contents = tuple(_contentsList)

        return len(self.contents)

    ###

    def contentsPop(self, start, stop=None, step=None):
        '''Remove and return XMLement Contents in [START:END:STEP] (slice notation)'''
        _contentsList = list(self.contents)
        rc = [] #Returned contents
        
        if stop is not None or step is not None:
            for c in range(start, stop, step):
                try:
                    rc.append(_contentsList[c])
                    _contentsList[c] = None
                except IndexError:
                    break

            while True:
                try:
                    _contentsList.remove(None)
                except ValueError:
                    break
                
        else: #Only START was specified
            rc = _contentsList.pop(start)

        self.contents = tuple(_contentsList)

        return rc
            
    ###

    def contentsDel(self, start, stop=None, step=None):
        '''Delete XMLement Contents in [START:END:STEP] (slice notation)'''

        self.contentsPop(start, stop, step)

        return len(self.contents)

    ###

        


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
        if self.contents is None or self.contents == (): #Empty (content-less) tag; format appropriately, and return
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


class XMLDocument:
    '''This class represents an entire XML document (essentially a collection of
    XMLements).  If FILEPATH is specified, an attempt will be made to automatically
    parse it, setting instance attributes appropriately.'''

    def __init__(self, filepath=None, errpol='surrogateescape', encoding="utf-8", xmlver=1.0):
        self.processingInstructions = [] #List of Processing Instructions
        self.exclamElements = [] #List of what I'm calling "Exclamation Elements" (couldn't find an official term), which include (but are not necessarily limited to) <!DOCTYPE ...>, <!ATTLIST ...>, <!ENTITY ...>, <!ELEMENT ...>, and comments
        self.elements = [] #List of actual XMLements in the documents
        self.xmlversion = xmlver
        self.encoding = encoding
        
        if filepath:
            _xmlfil = open(filepath, errors=errpol, encoding=encoding) #Open the file for reading with the given error policy
            self.readFile(_xmlfil)

    #######

    def readFile(self, file):
        '''Process FileObject FILE into the XMLDocument's XMLements''' 

        #Verify that we ARE trying to open an "XML", for basic idiot-proofing.
        #  Obviously, anyone can rename any file to end with .xml to make this code not
        #  complain, but if you're doing that, you're actively TRYING to break things.
        #  At that point, you deserve any problems that causes.
        if not file.name.lower().endswith(".xml"):
            file.close()
            raise NameError("FILE must wrap a .XML file") 
        
        try:
            firstLine = file.readline()
            if not (firstLine.startswith("<?xml") and firstLine.endswith("?>\n")):
                raise Warning("File does not appear to be a proper XML")
        except Warning as w:
            print("Proceed with caution; encountered Warning: {0}".format(w))
        except:
            print("Unhandled error:")
            file.close()
            raise
        finally:
            if not file.closed:
                file.seek(0,0)

        _lines = []
        for l in file:
            #Strip whitespace and line-delimiters, and add the lines to the LINES list
            l = l.lstrip()
            _lines.append(l.rstrip("\n"))

        file.close() #Close the file object
        
        _linesStr = "".join(_lines) #Compile all lines into a single string, for easier tag-matching

        self.elements = self.toXMLements(_linesStr, self) #Feed the XML data to the parser

    ###

    def toXMLements(self, inStr, parentElement=None, depth=0): #The main parser
        """Convert a string of XML data into a list of XMLements
        parentElement, if given, specifies the XMLement within which the current set of tags
        (inStr) is contained"""

        if parentElement and type(parentElement) not in (XMLement, XMLDocument):
            raise TypeError("ParentElement, if specified, must be an XMLement or XMLDocument")

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
        pis = self.processingInstructions
        ees = self.exclamElements

        #Get a list of tagnames in the string
        tagsByName = []
        for m in regex.findall(P_tag_names, inStr):
            if m.startswith("?"): #Processing instruction, not tag;
                pis.append(m) #FOR NOW, just indiscriminately add it to the list
                continue #Should actually process these eventually, but for now, just skip to the next tagname
            elif m.startswith("!"): #Exclamation Element, also not tag;
                ees.append(m) #As with a PI, just stuff it into the appropriate list
                continue #Should DEFINITELY process these, too, but as with a PI, just skip ahead for now
            
            if not m.startswith("/"): #At the moment, we're only interested in opening tags
                tagsByName.append(XMLement(m)) #Create a list of the XMLements in the input.
                                               #  For now, we're just storing the tagname.
                                               #  We'll figure out the props/contents later.

        #Offset lists so we know where each instance of T starts/ends 
        openingOffsets = [0]
        closingOffsets = [0]
        
        for t in tagsByName:
            strOffs = inStr.find(f"<{t.name}", openingOffsets[-1]) #S.find each tag matching T

            tagCloseOffs = inStr.find(f"</{t.name}>", strOffs) #S.find a closing tag for T
            if tagCloseOffs == -1: #No closing tag found!  Perhaps it's an empty tag? (E.G. <nullTag /> )
                #Check that:
                if inStr.find(" />", strOffs) < inStr.find(">", strOffs): #Valid empty tag; we get a " />" before we get the next ">"
                    tagCloseOffs = inStr.find(" />", strOffs) + 3 #Add 3 to cover the " />"
                else: #Invalid;
                    raise RuntimeError(f"Broken/unclosed tag <{t.name}> at Offset {strOffs} in input {inStr}")

            openingOffsets.append(strOffs)
            closingOffsets.append(tagCloseOffs)
        else:
            #Since the lists were initialized to [0] (so we could use the last item
            #  as S.find()'s starting offset), remove this first value from each
            #  once we're out of tags
            openingOffsets.pop(0)
            closingOffsets.pop(0)

        #That done, we can finally begin! (Right?)
       
    ##    ##DEBUG
    ##    print("\t"*depth, "---------------")
    ##    print("\t"*depth, openingOffsets)
    ##    print("\t"*depth, closingOffsets)
    ##    print("\t"*depth, tagsByName)
    ##    print("\t"*depth, "---------------")
    ##    #print(tagsByName)-len(openingOffsets))
    ##    #######

        for t, oOfs, cOfs in zip(tagsByName, openingOffsets, closingOffsets): #Iterate through the offsets list;
            
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
                t.contents = c #CONTENTS /should/ be null at this point, so this should be fine... I hope
    ##            ##DEBUG
    ##            print("\t"*depth, "-----")
    ##            print("\t"*depth, id(t), '\t', repr(t), '\t\t', id(t._parent), '\t', repr(t._parent))
    ##            print("\t"*depth, "-----")
    ##            #######

                #tags.append(t) #...and append it!  We now have a partial result; each
                               #  tag in in the list with its properties, and contents
                               #  as a string.  Step 2 will be to convert that string
                               #  into XMLements where required.
            else: #Error
                raise RuntimeError(f"Problem parsing tag <{t.name}> starting at Offset {oOfs} in input string {inStr}.")


        ##Step 2: CONTENTS to necessary XMLements
        for t in tagsByName:
            t._parent = parentElement
            if t.contents:
                c = t.contents
                cl = [] #List to hold processed Contents
                cm = regex.search(P_tag_with_contents, c, regex.DOTALL)
                if cm: #C contains XML; process into XMLements
                    for e in self.toXMLements(c, t, depth): #Feed C to the parser and iterate through the resultant list,
                        cl.append(e) #adding each result to the list used to initalize the current XMLement?
                else: #C is only a string (or nothing); add to the Contents list
                    cl.append(c) #Hope this is right...
        ##        ##DEBUG
        ##        print('\t'*depth, cl)
        ##        #######          
                t.contents = tuple(cl) #Set contents to the list

            tags.append(t) #Add the 'final' result to the return list

        return tags




################################
            

            
