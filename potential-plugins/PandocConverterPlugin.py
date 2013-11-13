#from yapsy.IPlugin import IPlugin
from categories import HTMLFormatter
import subprocess
import os

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
        

    def convert(self, actableFile):
        """Simple conversion script that runs markdown thru pandoc.
        actableFile: ActionalableFile object from dispatcher.py
        TODO: Fix relative image paths

        """
        try:
            os.mkdir(actableFile.dirname)
        except:
            pass
        subprocess.call(["pandoc", "-o",\
                           actableFile.indexHTML,\
                           actableFile.path])
        print "Ran pandoc on " + actableFile.path
        
    def print_name(self):
        print "Pandoc Converter Plugin"

   
