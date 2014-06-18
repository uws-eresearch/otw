
from categories import HTMLFormatter
from abf import ABFPreviewer
import os
import logging
import json 
import subprocess
import re

class ABFConverterPlugin(HTMLFormatter):
    """ ABF based document converter. 
    """

    def initialize(self, logger, config):
        """ Create a new formatter for the dispatcher to use. """ 
        self.logger = logger
        self.config = config
        self.actions = [{"exts"   :[".abf"],
                         "method" : self.convert,
                          "sig"   : "ABF",
                          "name"  : "ABF converter"}]
        self.name  = "ABF converter"
        self.logger.info(self.actions)
 

    def convert(self, actable_file):
        """Simple conversion script that extracts a preview from anxd ABF file.
        actable_file: ActionalableFile object from dispatcher.py


        """
       
        try:
            os.makedirs(actable_file.dirname)
        except:
            pass
        self.logger.warning("Starting ABF previewer on " + actable_file.filename)
        html = ABFPreviewer.create_HTML_document(actable_file.path)
        f = open(actable_file.indexHTML, 'w')
        print >>f, html
        f.close()

        self.logger.warning("ABF previewer on " + actable_file.filename)
