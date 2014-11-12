#!/usr/bin/env python
"""
Part of the Of The Web (otw) framework.

Scans one or more directories and creates web-ready versions of content therein

Start this using a shell script for the appropriate operating system

"""
import os, sys
import categories

import json
from yapsy.PluginManager import PluginManager
import logging
import json

from categories import HTMLFormatter

#TODO fail gracefully with usage


class WatcherDispatcher:
    def __init__(self, watchDirs, logger, pyinotify, EventHandler):
        self.mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_CLOSE_WRITE  
        self.wm = pyinotify.WatchManager()
        self.notifier = pyinotify.ThreadedNotifier(self.wm, EventHandler())
        self.notifier.start()
        logger.info("Starting watching")
        for watch in watchDirs:
            self.wm.add_watch(watch, self.mask, rec=True)
            logger.info("watching" + watch)
        logger.info("---------")

    #def start(self):
     #   watcher(wm)

#Starting watching on new thread

class FileAction:
    def __init__(self, ext, method, sig, name):
        self.ext = ext
        self.method = method
        self.sig = sig
        self.name = name


class FileActionStore:
    def __init__(self):
        self.actions = dict()

    def addAction(self,action):
        self.actions[action.ext] = action

    def addActions(self, actionDicts):
        for act in actionDicts:
            for e in act["exts"]:
		self.addAction(FileAction(e, act["method"],act["sig"], act["name"]))
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
                

    def extensionHasAction(self, ext):
        return ext in self.actions

    def getAction(self, ext):
        return self.actions[ext]

    def actions(self):	
        for a in actions:
            yield a


class ActionableFile:
    def __init__(self, file, logger, config, actions):
        self.logger = logger
        self.config = config
        self.actions = actions
        self.originalDirname, self.filename = os.path.split(file)
        self.ext = self.splitexts(self.filename)
        self.filestem = self.filename.replace(self.ext, "")
        htmlDirName = os.sep + config["generatedDirName"] + os.sep
        
        #TODO: make this 'proper' JSON-LD by adding @context
        #For now jsut use simple metadata which is 'JSON-LD ready'
        self.meta = {"dc:title":"Untitled","dc:creator":{"@list": []}}
        #TODO make meta private and add methods to change it
        try:       
            if (not htmlDirName in file and self.actions.extensionHasAction(self.ext)):
                action = self.actions.getAction(self.ext)
                self.path = file
                
                self.method = action.method
                self.actionable = True
                self.indexFilename = "index.html"
                self.metaFilename = "meta.json"
                self.dirname = os.path.join(self.originalDirname,
					    self.config["generatedDirName"],
                                            self.filename)
                
                self.indexHTML = os.path.join(self.dirname,self.indexFilename)
                self.metaJSON = os.path.join(self.dirname,self.metaFilename)
            else:
                self.actionable = False
        except Exception, e:
            self.complain(e)
   
    def splitexts(self, path):
        (file, ext) = os.path.splitext(path)
        if ext == "":
            return ""
        else:
            return self.splitexts(file) + ext.lower()        
            
    def complain(self, e):
        self.logger.warning(self.path)
        self.logger.warning(sys.exc_info()[0])
        self.logger.warning(e.__doc__)
        self.logger.warning(e.message)
        self.logger.warning("-------------")
            
    def saveMeta(self):
        j = open(self.metaJSON, "w")
        json.dump(self.meta,j)
            
    def act(self):
        try:
            if (self.actionable and 
               ((not os.path.exists(self.indexHTML)) or
                 (os.path.getmtime(self.indexHTML) < os.path.getmtime(self.path)))):
                    try:
                        os.makedirs(self.dirname)
                    except:
                        pass
                    html = "<p>There was an error creating this file, please contact you administrator</p>"
                    open(self.indexHTML, 'w').write(html)
                    self.method(self)
        except Exception, e:
            self.complain(e)
        

class FileDispatcher:
    """ One-pass file walker to find all the files already in our watched dirs 
	We want to get this list ASAP after starting as any subsequent changes
	should get picked up by the watcher directories"""

    def __init__(self, toWatch, logger, config, actions):
        self.fileList = []
        for watch in toWatch:
            for root, dirs, files in os.walk(watch):
                for file in files:
                    actionable = ActionableFile(os.path.join(root,file),logger, config, actions)
                    if actionable.actionable:
                        self.fileList.append(actionable)	
       


    # Call processors for initial list
    def acts(self):
        for file in self.fileList:
	        #Check if we still need to run as things might have changed
	         if file.actionable: file.act()

def get_config(from_filename=None):
    if from_filename <> None:
        config = json.load(open(from_filename))
    else:
        config = json.loads("""{
            "watchDirs" : ["."],
            "pluginDirs" : ["./plugins"],
            "scanRepeatedly" : false,
            "useInotify" : false,
            "generatedDirName" : "_html",
            "preferDataURIs" : false,
            "logFile" : "dispatcher.log"
            }""")
    return config
     
     
def get_logger(config):
    logger = logging.getLogger('dispatcher')
    hdlr = logging.FileHandler(config["logFile"])
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.DEBUG)
    return logger
    

def main():
    #TODO: proper argument handling, usage etc

    #Config   
    configFilePath = sys.argv[1]
    config = get_config(from_filename = configFilePath)
    logger = get_logger(config)
    scanRepeatedly = config["scanRepeatedly"]

    #logging
    logger = get_logger(config)
    logger.warning("OTW Dispatcher started")



    # Load the plugins from the plugin directory.
    manager = PluginManager(categories_filter={ "Formatters": HTMLFormatter})
    manager.setPluginPlaces(config["pluginDirs"])
    for dir in config["pluginDirs"]:
        sys.path.append(dir)
    manager.collectPlugins()

    # Loop round the loaded plugins and set up actions
    actions = FileActionStore()
    for plugin in manager.getAllPlugins():
        plugin.plugin_object.initialize(logger, config)
        logger.info("Loaded plugin: " + str(plugin.plugin_object.actions))
        actions.addActions(plugin.plugin_object.actions)
                                                                                                                                                                                                                                                                                
    useInotify = config["useInotify"]
    if useInotify:
        try:
            import pyinotify
            class EventHandler(pyinotify.ProcessEvent):
                def process_IN_CREATE(self, event):
                    if os.path.isfile(event.pathname):
                        ActionableFile(event.pathname, logger, config, actions).act()

                def process_IN_CLOSE(self, event):
                    if os.path.isfile(event.pathname):
                        ActionableFile(event.pathname,logger, config, actions).act()
                
                def process_IN_DELETE(self, event):
                    pass #TODO Deal with removing files
                    

        except Exception, e:
                logger.warn("Unable to import pyinotify")
                useInotify = False
          
    #Start watching
    if scanRepeatedly and useInotify:
        scanRepeatedly = False #Don't loop below we're already watching events
        WatcherDispatcher(config["watchDirs"], logger, pyinotify, EventHandler)
    
    #Get a list of existing files
    needToScanFiles = True
    while needToScanFiles:
        FileDispatcher(config["watchDirs"], logger, config, actions).acts()
        needToScanFiles = scanRepeatedly
       
  


if __name__ == "__main__":
    main()

