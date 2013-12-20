#from yapsy.IPlugin import IPlugin
from categories import HTMLFormatter
import subprocess
import os
import logging
import json 
import Image
import StringIO

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
        

        

    def convert(self, actableFile):
        """Simple conversion script that runs markdown thru pandoc.
        actableFile: ActionalableFile object from dispatcher.py
        TODO: Fix relative image paths

        """
            
        try:
            os.makedirs(actableFile.dirname)
        except:
            pass
       
        body = subprocess.check_output(["exiftool", "-h", actableFile.path])
        # TODO add to config
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
        html = "<html><title>%s</title><body><p><a href='../../%s'><img src='%s'></a></p>%s</body></html>" % (actableFile.meta["dc:title"],actableFile.filename, prevURI, body)
        
        f = open(actableFile.indexHTML,"w")
        
        f.write(html)
        f.close()
        actableFile.saveMeta()
        logging.info("Ran Exfitool on " + actableFile.path)
        
    def print_name(self):
        print "Image Converter Plugin"

   
