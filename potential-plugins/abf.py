#!/usr/bin/env python

from neo import *
import dominate
from dominate import *
from dominate.tags import *
import numpy as np 
import os, time
from stat import *


class ABFPreviewer:

   @staticmethod
   def f(value):
      return "{}".format(value)


   @staticmethod
   def extract_units(signal):
      full = "{}".format(signal.units)
      index = full.rfind(" ") + 1
      return full[index:]
   

   @staticmethod
   def create_HTML_document(filename):
      try:
         st = os.stat(filename)
      except:
         d = document(title = filename)
         d += h1(os.path.basename(filename))
         divvy = d.body.add(div(class_name = 'error'))
         with divvy:
            p("cannot open file {}".format(filename))
         return d
      
      r = AxonIO(filename=filename)
      bl = r.read_block(lazy=False, cascade=True)
      if bl.name == None:
         d = document(title = filename)
         d += h1(filename)
      else:
         d = document(title = bl.name)
         d += h1(bl.name)

      with d:
         # File statistics
         h2("File Information")
         l = dl()
         with l:
            dt("Created:")
            dd(time.asctime(time.localtime(st[ST_MTIME])))
            dt("Size:")
            dd("{} bytes".format(st[ST_SIZE]))
  

         # Any attributes that we can find for this block
         h2("Block Header")
         l = dl()
         with l:
            dt("Name:")
            if bl.name == None:
               desc = dd()
               desc.add(i("none"))
            else:
               dd(bl.name)
            dt("Description:")
            if bl.description == None:
               desc = dd()
               desc.add(i("none"))
            else:
               dd(bl.description)
            dt("File:")
            if bl.file_origin == None:
               desc = dd()
               desc.add(i("none"))
            else:
               dd(bl.file_origin)
            dt("Creation Date:")
            if bl.file_datetime == None:
               desc = dd()
               desc.add(i("none"))
            else:
               dd(ABFPreviewer.f(bl.file_datetime))
            dt("Recording Date:")
            if bl.rec_datetime == None:
               desc = dd()
               desc.add(i("none"))
            else:
               dd(ABFPreviewer.f(bl.rec_datetime))
            dt("Index:")
            if bl.index == None:
               desc = dd()
               desc.add(i("none"))
            else:
               dd(bl.index)


      # Segments and Signals information
      segNum = 0
      for seg in bl.segments:
         if seg.name == None:
             d += h2("Segment {}".format(segNum))
         else:
             d += h2(seg.name)


         # Create the table summarising this segment's signals
         sigNum = 0
         t = d.body.add(table(border = 1))
         with t:
            header = thead()
            with header:
               r = tr()
               r += th("Signal")
               r += th("Sampling Rate")
               r += th("Duration")
               r += th("Shape")
               r += th("Size")
               r += th("Units")
               r += th("Min")
               r += th("Max")
               r += th("Values")
   
            body = tbody()
            with body:
               for sigs in seg.analogsignals:
                  r = tr()
                  if sigs.name == None:
                      r += td("Signal {}".format(sigNum))
                  else:
                      r += td(sigs.name)
                  r += td("{}".format(sigs.sampling_rate))
                  r += td("{}".format(sigs.duration))
                  r += td("{}".format(sigs.shape))
                  r += td("{}".format(sigs.size))
                  r += td(ABFPreviewer.extract_units(sigs))
                  r += td("{}".format(sigs.min()))
                  r += td("{}".format(sigs.max()))
                  r += td("{}".format(sigs))
                  sigNum = sigNum+1
         segNum = segNum+1
      return d
