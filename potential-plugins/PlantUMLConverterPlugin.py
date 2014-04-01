#from yapsy.IPlugin import IPlugin
from categories import HTMLFormatter
import plantuml
import os
import logging
import json 

class PlantUMLConverterPlugin(HTMLFormatter):
    """ Plantuml based document converter. For demo purposes only!
	This uses the public plantUML server as per the default in the
	python-plantuml library.

	For real life use first install a PlantUML server
	To install, first install this:
	https://github.com/dougn/python-plantuml
	
	Download as Zip from github, and:
		sudo python setup.py install
    """

    def __init__(self):
        """ Create a new formatter for the dispatcher to use. """ 
        
        self.actions = [{"exts"   :[".plantuml"],\
                         "method" : self.convert,\
                          "sig"   : "plantuml",\
                          "name"  : "Plantuml converter"}]
        self.name  = "Plantuml converter"
        

        

    def convert(self, actableFile):
        """Simple conversion script that runs PlantUML via HTTP.
        actableFile: ActionalableFile object from dispatcher.py
      

        """
            
        try:
            os.makedirs(actableFile.dirname)
        except:
            pass
            
       	pu = plantuml.PlantUML()
	pu.processes_file(actableFile.path, os.path.join(actableFile.dirname, "index.png"))
        html = "<html><body><img src='./index.png'></body></html>"
	open(actableFile.indexHTML, 'w').write(html)
        self.logger.info("Ran PlantUML on " + os.path.join(actableFile.dirname, "index.png"))

        
  

   
