#!/usr/bin/env python
import os, sys
import categories
import pyinotify
import json
from yapsy.PluginManager import PluginManager
import logging

from categories import HTMLFormatter

logging.basicConfig(level=logging.DEBUG)


class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        ActionableFile(event.pathname).act()

    def process_IN_CLOSE(self, event):
        ActionableFile(event.pathname).act()
    
    def process_IN_DELETE(self, event):
        print "Removing:", event.pathname

class WatcherDispatcher:
    def __init__(self, watchDirs):
        self.mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_CLOSE_WRITE  
        self.wm = pyinotify.WatchManager()
        self.notifier = pyinotify.ThreadedNotifier(self.wm, EventHandler())
        self.notifier.start()
        print "Started watching"
        for watch in watchDirs:
            self.wm.add_watch(watch, self.mask, rec=True)

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
	    print act
            for e in act["exts"]:
                self.addAction(FileAction(e, act["method"], act["sig"], act["name"]))

    def extensionHasAction(self, ext):
        return ext in self.actions

    def getAction(self, ext):
        return self.actions[ext]

    def actions(self):	
        for a in actions:
            yield a


class ActionableFile:
    def __init__(self, file):
        _,ext = os.path.splitext(file)
        #todo get rid of globals
        if ACTIONS.extensionHasAction(ext):
            action = ACTIONS.getAction(ext)
            self.path = file
            dirname, self.filename = os.path.split(file)
            self.method = action.method
            self.actionable = True
            self.dirname = os.path.join(dirname,
                                        self.filename + 
                                        CONFIG["generatedDirSuffix"])
            self.indexHTML = os.path.join(self.dirname,"index.html")
        else:
            self.actionable = False
        
    def act(self):
        if (self.actionable and 
           ((not os.path.exists(self.indexHTML)) or
             (os.path.getmtime(self.indexHTML) < os.path.getmtime(self.path)))):
            self.method(self)
        else:
            pass

class FileDispatcher:
    """ One-pass file walker to find all the files already in our watched dirs 
	We want to get this list ASAP after starting as any subsequent changes
	should get picked up by the watcher directories"""

    def __init__(self, toWatch):
        self.fileList = []
        for watch in toWatch:
            for root, dirs, files in os.walk(watch):
                for file in files:
                    actionable = ActionableFile(os.path.join(root,file))
                    if actionable.actionable:
			self.fileList.append(actionable)	
       


    # Call processors for initial list
    def acts(self):
        for file in self.fileList:
	        #Check if we still need to run as things might have changed
	         if file.actionable: file.act()


# Now watch and call processors for each file

#TODO - can I get rid of this global?
ACTIONS = FileActionStore()
CONFIG = json.load(open("dispatcher-config.json"))


def main():   
    
    # Load the plugins from the plugin directory.
    manager = PluginManager(categories_filter={ "Formatters": HTMLFormatter})
    manager.setPluginPlaces(CONFIG["pluginDirs"])
    for dir in CONFIG["pluginDirs"]:
        sys.path.append(dir)
    manager.collectPlugins()
    
    # Loop round the loaded plugins and print their names.
    for plugin in manager.getAllPlugins():
	print "Loaded plugin: ",
        plugin.plugin_object.print_name()
        ACTIONS.addActions(plugin.plugin_object.actions)
          
    #Start watching
    
    WatcherDispatcher(CONFIG["watchDirs"])

    #Get a list of existing files
    
    FileDispatcher(CONFIG["watchDirs"]).acts()
  


if __name__ == "__main__":
    main()

