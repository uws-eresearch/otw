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

	For real life use make sure you install Graphviz:
	    sudo apt-get install graphviz
	    
	and add a value to your dispatcher-config.jsonn for the plantuml path
	    "plantuml_path" : "/opt/otw/plugins/plantuml.jar"      

	To install, first install this:
	https://github.com/dougn/python-plantuml
	
	Download as Zip from github, and:
		sudo python setup.py install
    """

    def initialize(self, logger, config):
        """ Create a new formatter for the dispatcher to use. """ 
        self.logger = logger
        self.config = config
        self.actions = [{"exts"   :[".plantuml.txt"],\
                         "method" : self.convert,\
                          "sig"   : "plantuml",\
                          "name"  : "Plantuml converter"}]
        self.name  = "Plantuml converter"
        

        

    def convert(self, actable_file):
        """Simple conversion script that runs PlantUML.
        actable_file: ActionalableFile object from dispatcher.py


        """
            
        try:
            os.makedirs(actable_file.dirname)
        except:
            pass
        html = "<html><body>"
        if "plantuml_path" in self.config: 
            #Installed locally
            logger.info(subprocess.check_output(["java", "-jar", 
                        self.config["plantuml_path"], "-o",
                        actable_file.dirname]))
            #TODO: SVG as well
        else:
            #Phone a friend
            pu = plantuml.PlantUML()
            pu.processes_file(actable_file.path, os.path.join(actable_file.dirname, "%s.png" % actable_file.filestem))
            
        html += "<img src='./%s.png'></body></html>" % actable_file.filestem
        open(actable_file.indexHTML, 'w').write(html)
        self.logger.info("Ran PlantUML on " + os.path.join(actable_file.dirname, "index.png"))

        
  

   
