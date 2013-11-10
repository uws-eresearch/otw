#from yapsy.IPlugin import IPlugin
from categories import HTMLFormatter
import subprocess
import os

class PandocConverterPlugin(HTMLFormatter):
    def __init__(self):
        self.actions = [{"exts"   :[".md"],\
                         "method" : self.convert,\
                          "sig"   : "pandocmd",\
                          "name"  : "Pandoc based markdown converter"}]
        

    def convert(self, actableFile):
        try:
            print "Trying to make" + actableFile.dirname
            os.mkdir(actableFile.dirname)
        except:
            pass
        subprocess.call(["pandoc", "-o",\
                           actableFile.indexHTML,\
                           actableFile.path])
        print "Ran pandoc on " + actableFile.path
        
    def print_name(self):
        print "Pandoc Converter Plugin"

   
