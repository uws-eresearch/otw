#from yapsy.IPlugin import IPlugin
from categories import HTMLFormatter
import subprocess
import os
import logging
import json 


class PandocConverterPlugin(HTMLFormatter):
    """ Pandoc based document converter.
    Initial release handles markdown only.

    """

    def __init__(self):
        """ Create a new formatter for the dispatcher to use. """ 

        self.actions = [{"exts"   :[".md"],\
                         "method" : self.convert,\
                          "sig"   : "pandocmd",\
                          "name"  : "Pandoc based markdown converter"}]
        self.config = json.load(open("dispatcher-config.json"))
        if "preferDataURIs" in self.config:
            self.preferDataURIs = self.config["preferDataURIs"]
        else:
            self.preferDataURIs = False
        

        

    def convert(self, actableFile):
        """Simple conversion script that runs markdown thru pandoc.
        actableFile: ActionalableFile object from dispatcher.py
        TODO: Fix relative image paths

        """
            
        try:
            os.makedirs(actableFile.dirname)
        except:
            pass
            
        os.chdir(actableFile.originalDirname)
        if self.preferDataURIs:
             try:
                subprocess.check_output(["pandoc", "--self-contained", "-o",
                           actableFile.indexHTML, actableFile.path])
                return
             except:
                pass
        subprocess.check_output(["pandoc", "-o",
                           actableFile.indexHTML, actableFile.path])
    
        logging.info("Ran pandoc on " + actableFile.path)
        
    def print_name(self):
        print "Pandoc Converter Plugin"

   
