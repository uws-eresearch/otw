#!/usr/bin/env python

from neo import *
import dominate
from dominate import *
from dominate.tags import *
import numpy as np
import os, time
from stat import *
from categories import HTMLFormatter
from abf import ABFPreviewer
import os
import logging
import json 
import subprocess
import re
html = ABFPreviewer.create_HTML_document('/home/david/4a/abf/sin-stdp7.abf')
f = open("junk.html", "w")
print >>f, html
f.close()
