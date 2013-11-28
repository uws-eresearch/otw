#  OF the web (otw)

This project aims to bring together an extensible set of tools for creating web-ready views of all kinds of files. The idea is that everything should not only have the opportunity to be ON the web but should also be able to be OF the web - that is, available in HTML, or wrapped in HTML, with as much rich machine readable metadata as possible.

This is for Linux based systems only as it relies on the inotify file event notification service.


It contains:
* A file-watching framework that can monitor directories and automatically create web-ready content.

* A set of plugins. The first commit has a markdown converter which uses Pandoc, a Word document converter is coming very soon.

## Protocol for generated files ** WARNING ** work in progress will almost certainly change

Plugins generate new directories alongside existing files. So if you have a file like:

```
test.md
```

Then the system will generate a set of web-ready files alongside it:

```
test.md
/_html/test.md/index.html
            /snippet.html #NOT implemented yet
            /eotx.txt #Not implemented yet will contain info about what 
                       generated this file  
```

## Install

These instructions are for Ubuntu and at this stage we are assuming you know your way around the commandline, where to put bits of code etc. 


* Check it out from github

    ```cd /opt/```

	```sudo mkdir otw```

	```sudo chown $USER:$USER eotw```

    ```git clone https://github.com/uws-eresearch/otw.git```

* Install the dependencies TODO: Check

    ```sudo easy_install yapsy pyinotify ```

* For each of the plugins you're going to use, install _their_ dependecies. For the example pandoc markdown converter

    ```sudo apt-get install pandoc``` 

    or (better) install Pandoc via cabal and set your path to include ```~/.cabal/bin``` (see the Pandoc site)

* Copy the sample config file to make your own:

    ```cp dispatcher-config.json.sample dispatcher-config.json```

* Edit the sample congfig file to tell the dispatcher which directories to watch. That is, change the entry for Watchdirs to an array of one or more paths to watch.
  * ```"PreferDataURIs" : true``` will try to save images as data URIs rather than separate files 

## Add plugins

A pluging for _OF The Web_ consists of (at least) two files, a plugin info file with the extension ```.epsy-plugin``` and a python file (```.py```).

Out of the box, the system will look in the ```plugins/``` directory for conversion plugins that format files into HTML.

A simple way to get started is to copy the whole directory:

    ```cp -r /opt/otw/potential-plugins /opt/otw/plugins```
    
There is an office document converter that run on word processing documents in this project: https://code.google.com/p/jischtml5/

Assuming you [install it](https://code.google.com/p/jischtml5/wiki/WordDownCommandlineOpenOffice), add it to your plugins like so:
  * Add this to your array of pluginPaths array ```"/opt/jischtml5/tools/commandline"```

# Run

There will be more options for running this toolkit in future, but for now, run it like so:

 *  ```python dispatcher.py```





