#from yapsy.IPlugin import IPlugin
from categories import HTMLFormatter
import subprocess
import os
import logging
import json 
import Image
import StringIO
import rdflib
import re

class ImageConverterPlugin(HTMLFormatter):
    """ Image converter - requires Exiftool to be installed
    and on the path, and the Python Image Library, PIL.
    
    This converter uses DATA URIS; extra
    image files will be confusing as they will be picked up
    by image management software such as Picasa.

    """

    def __init__(self):
        """ Create a new formatter for the dispatcher to use. """ 

        self.actions = [{"exts"   :[".jpg", ".png"],\
                         "method" : self.convert,\
                          "sig"   : "images",\
                          "name"  : "Image converter"}]
        self.config = json.load(open("dispatcher-config.json"))
        self.previewSize = self.config["previewSize"]
        self.thumbnailSize = self.config["thumbnailSize"]
        self.meta = dict()
        self.defaultMetaOrder = ["Keywords",  "File Name",  "Directory",  "File Size",  "File Modification Date/Time",  "File Permissions",  "File Type",  "MIME Type",  "JFIF Version",  "Exif Byte Order",  "Image Description",  "Make",  "Camera Model Name",  "X Resolution",  "Y Resolution",  "Resolution Unit",  "Software",  "Modify Date",  "Artist",  "Y Cb Cr Positioning",  "Copyright",  "Exposure Time",  "F Number",  "Exposure Program",  "ISO",  "Sensitivity Type",  "Exif Version",  "Date/Time Original",  "Create Date",  "Components Configuration",  "Exposure Compensation",  "Max Aperture Value",  "Metering Mode",  "Light Source",  "Flash",  "Focal Length",  "Special Mode",  "Camera ID",  "User Comment",  "Flashpix Version",  "Color Space",  "Exif Image Width",  "Exif Image Height",  "Interoperability Index",  "Interoperability Version",  "Related Image Width",  "Related Image Height",  "File Source",  "Custom Rendered",  "Exposure Mode",  "White Balance",  "Digital Zoom Ratio",  "Scene Capture Type",  "Gain Control",  "Contrast",  "Saturation",  "Sharpness",  "Image Unique ID",  "Lens Info",  "Lens Model",  "PrintIM Version",  "Compression",  "Thumbnail Offset",  "Thumbnail Length",  "XMP Toolkit",  "Creator",  "Subject",  "Current IPTC Digest",  "Envelope Record Version",  "Coded Character Set",  "Application Record Version",  "Image Width",  "Image Height",  "Encoding Process",  "Bits Per Sample",  "Color Components",  "Y Cb Cr Sub Sampling",  "Aperture",  "Image Size",  "Shutter Speed",  "Thumbnail Image",  "Focal Length",  "Light Value"]
        

    def rdfToDict(self, rdf):
        """
        Take an RDF graph from exiftool and flatten it into a dict keyed by label 
        where meta[label] = (predicate,object)
        All objects are Literals (strings)
        """
        g = rdflib.Graph()
        g.parse(data=rdf)
        subjectURI = rdflib.term.URIRef(u"http://ns.exiftool.ca/XMP/XMP-dc/1.0/Subject")
        keywordsURI = rdflib.term.URIRef(u"http://ns.exiftool.ca/IPTC/IPTC/1.0/Keywords")
        def unpackBag(term):
            for s,o in g.subject_objects(term):
                contentArray = []
                for p1,o1 in g.predicate_objects(o):
                   if type(o1) is rdflib.term.Literal:
                        contentArray.append(o1)
                #Get rid of statements about the bag / flatten
                content = ", ".join(contentArray)
                g.remove((o, None, None))
                g.remove((None,None,o))
                g.add((s,term,rdflib.term.Literal(content)))     
        unpackBag(subjectURI)
        unpackBag(keywordsURI)
        
        for s,p,o in g:
            label = re.sub(".*/","",p)
            label = re.sub("([A-Z][a-z])", " \\1", label)
            self.meta[label[1:]] = (p, o)
            
    def dictToTable(self):
        self.body = "<table>"
        def formatRow(m):
            (p,o) = self.meta.pop(m)
            self.body += "<tr><td>%s</td><td property='%s'>%s</td></tr>" % (m,p,o)
        for m in self.defaultMetaOrder:
            if m in self.meta:
                formatRow(m)
                
        #Spit out whats left
        for m in self.meta.keys():
            formatRow(m)
            
        self.body += "</table>"
        

    def convert(self, actableFile):
        """
           Extract metadata from image files and create an RDFa-ish index.html with a preview using a data URI

        """
            
        try:
            os.makedirs(actableFile.dirname)
        except:
            pass
       
        self.rdf = subprocess.check_output(["exiftool", "-X", actableFile.path])
        self.rdfToDict(self.rdf)
        self.dictToTable()
        
        im = Image.open(actableFile.path)
        im.thumbnail(self.previewSize)
        
        def makeURI(im):
            f = StringIO.StringIO() #File-like thing
            im.save(f,"PNG") #Need to do this to convert the image
            return "data:image/png;base64,%s" % (f.getvalue().encode("base64"))
        prevURI = makeURI(im)
        im = Image.open(actableFile.path)
        im.thumbnail(self.thumbnailSize)
        thumbURI = makeURI(im)
        actableFile.meta["dc:title"] = actableFile.filename
        actableFile.meta["thumbnail"] = thumbURI 
        #actableFile.meta["preview"] = prevURI #TOO big consider having a separate JSON file
        html = "<html><title>%s</title><body><p><a href='../../%s'><img src='%s'></a></p>%s</body></html>" % (actableFile.meta["dc:title"],actableFile.filename, prevURI, self.body)
        
        f = open(actableFile.indexHTML,"w")
        
        f.write(html)
        f.close()
        actableFile.saveMeta()
        self.logger.info("Ran Exfitool on " + actableFile.path)
        
    def print_name(self):
        print "Image Converter Plugin"

   
