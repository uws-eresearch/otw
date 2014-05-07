from PlantUMLConverterPlugin import PlantUMLConverterPlugin
import sys
sys.path.append("..")
import dispatcher
import unittest
import logging
import re
import os
import json
import shutil
class TestPlantUMLConverter(unittest.TestCase):

    def setUp(self):
        self.converter = PlantUMLConverterPlugin()
        self.config = dispatcher.get_config()

        self.logger = dispatcher.get_logger(self.config)
        self.converter.initialize(self.logger, self.config)    
        self.actions = dispatcher.FileActionStore()
        self.actions.addActions(self.converter.actions)    
       
                 
 
    def test_plantuml_using_jar(self):
        """
        Simple Smoke test to check that everything is actually happening 
        """
        self.config["plantuml_path"] = os.path.join(os.getcwd(), "plantuml.jar")
        to_do = dispatcher.ActionableFile("./PlantUMLConverterPlugin_tests/license.plantuml.txt", self.logger, self.config, self.actions)
        try:
            shutil.rmtree(to_do.dirname)
        except:
            pass
            
        assert(not os.path.exists(to_do.indexHTML))
        to_do.act()
       
        assert(os.path.exists(to_do.indexHTML))
        assert(os.path.exists(os.path.join(to_do.dirname, "license.plantuml.png")))
        meta = json.load(open(to_do.metaJSON))
        self.assertEqual(meta["dc:title"], "Untitled")
        
        
    def test_plantuml_title(self):
        """
        Simple Smoke test to check that everything is actually happening 
        """
        self.config["plantuml_path"] = os.path.join(os.getcwd(), "plantuml.jar")
        to_do = dispatcher.ActionableFile("./PlantUMLConverterPlugin_tests/test.plantuml.txt", self.logger, self.config, self.actions)
        try:
            shutil.rmtree(to_do.dirname)
        except:
            pass

        to_do.act()
       
        assert(os.path.exists(to_do.indexHTML))
        assert(os.path.exists(os.path.join(to_do.dirname, "test.plantuml.png")))
        meta = json.load(open(to_do.metaJSON))
        self.assertEqual(meta["dc:title"], "The title of this diagram is title")


if __name__ == '__main__':
    unittest.main()
