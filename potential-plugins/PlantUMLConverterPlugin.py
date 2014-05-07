
from categories import HTMLFormatter
import os
import logging
import json 
import subprocess
import re

class PlantUMLConverterPlugin(HTMLFormatter):
    """ Plantuml based document converter. 

	For real life use make sure you install Graphviz:
	    sudo apt-get install graphviz
	    
	and add a value to your dispatcher-config.json for the plantuml path
	    "plantuml_path" : "/opt/otw/plugins/plantuml.jar"   

	PlantUML is distributed under the GPL license. 
    You can print the license using the command line option:
	    java -jar plantuml.jar -license
    Or you can use the special diagram:
	@startuml
	license
	@enduml        

	
    """

    def initialize(self, logger, config):
        """ Create a new formatter for the dispatcher to use. """ 
        self.logger = logger
        self.config = config
        self.actions = [{"exts"   :[".plantuml.txt"],
                         "method" : self.convert,
                          "sig"   : "plantuml",
                          "name"  : "Plantuml converter"}]
        self.name  = "Plantuml converter"
        self.logger.info(self.actions)
 

    def convert(self, actable_file):
        """Simple conversion script that runs PlantUML.
        actable_file: ActionalableFile object from dispatcher.py


        """
       
        try:
            os.makedirs(actable_file.dirname)
        except:
            pass
        html = "<html><body>"
       
        command = ["java", "-jar", 
                    self.config["plantuml_path"], "-o",
                    os.path.abspath(actable_file.dirname), actable_file.path]           
        self.logger.warning(subprocess.check_output(command))
            
        html += "<img src='./%s.plantuml.png'></body></html>" % actable_file.filestem
        open(actable_file.indexHTML, 'w').write(html)
        source = open(actable_file.path).read()
        r = re.compile("^title (.*)$",re.M)
        titleMatch = r.search(source)
        if  titleMatch != None:
            actable_file.meta["dc:title"] = titleMatch.group(1)
        actable_file.saveMeta()
        self.logger.warning("Ran PlantUML on " + actable_file.filename)

        
  

   
