#from yapsy.IPlugin import IPlugin
from categories import HTMLFormatter
import plantuml
import os
import logging
import json 

class PlantUMLConverterPlugin(HTMLFormatter):
    """ Plantuml based document converter. For demo purposes only!
	For real life use first install a PlantUML server
	To install, first install this:
	
    """

    def __init__(self):
        """ Create a new formatter for the dispatcher to use. """ 
        
        self.actions = [{"exts"   :[".plantuml"],\
                         "method" : self.convert,\
                          "sig"   : "plantuml",\
                          "name"  : "Plantuml converter"}]
        self.name  = "Plantuml converter"
        

        

    def convert(self, actableFile):
        """Simple conversion script that runs markdown thru pandoc.
        actableFile: ActionalableFile object from dispatcher.py
        TODO: Fix relative image paths

        """
            
        try:
            os.makedirs(actableFile.dirname)
        except:
            pass
            
       	pu = plantuml.PlantUML()
	pu.processes_file(actableFile.path, os.path.join(actableFile.dirname, "index.png"))
        html = "<html><body><img src='./index.png'></body></html>"
	open(actableFile.indexHTML, 'w').write(html)
        self.logger.info("Ran pandoc on " + os.path.join(actableFile.dirname, "index.png"))

        
  

   