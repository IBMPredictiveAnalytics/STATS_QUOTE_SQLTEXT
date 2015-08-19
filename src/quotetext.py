#/***********************************************************************
# * Licensed Materials - Property of IBM 
# *
# * IBM SPSS Products: Statistics Common
# *
# * (C) Copyright IBM Corp. 1989, 2013
# *
# * US Government Users Restricted Rights - Use, duplication or disclosure
# * restricted by GSA ADP Schedule Contract with IBM Corp. 
# ************************************************************************/

# This module takes as input a sequence of SQL lines and
# writes an output file with those lines quoted appropriately
# for use in IBM SPSS Statistics GET DATA /TYPE=ODBC
# Insert the output from this module into the GET DATA after
# /SQL =
# and add a period afterwards

# This module is meant to be run via SPSSINC PROGRAM, e.g.,
# SPSSINC PROGRAM quotetext.run "input filename" "output filename".

# The file may begin with a UTF8 BOM, which will be preserved.
# Other Unicode markings will not be recognized.

# Author JKP, IBM SPSS
# 30-Sep-2010 Initial version
# 06-Oct-2010  convert to form for use with SPSSINC PROGRAM, Unicode support


import sys
from codecs import BOM_UTF8

def _smartquote(s, qchar='"'):
    """ smartquote a string so that internal quotes are distinguished from surrounding
    quotes for SPSS and return that string with the surrounding quotes.  
    
    qchar is the character to use for surrounding quotes."""
    
    return qchar + s.replace(qchar, qchar+qchar) + qchar

escapemapping = \
    {"\t": r"\t", "\n":r"\n", "\r": r"\r", "\'":r"\'", "\a":r"\a","\b":r"\b", "\f":r"\f","\N":r"\N", "\v":r"\v"}

def unescape(item):
    "Undo any escape sequences due to the UP"
    
    if item is None:
        return item
    return "".join([escapemapping.get(ch, ch) for ch in item])

def run():
    """Smartquote the file passed as the first argument and write
    it to the filename passed as the second argument"""
    
    # version 18 interprets \t etc as an escape sequence, which must be undone
    try:
        inputname = unescape(sys.argv[1])
        outputname = unescape(sys.argv[2])
    except:
        print """Usage: python civilize.py "inputname" "outputname". """
        return
    
    try:
        f = open(inputname, "r")
        fout = open(outputname, "w")
    except:
        print "quotetext: ", sys.exc_info()[1]
        return
    
    
    plus = ""
    first = True
    for line in f:
        if first :
            first = False
            if line[:3] == BOM_UTF8:  # UTF8 with BOM
                fout.write(line[:3])
                line = line[3:]
        line = plus +  _smartquote(line[:-1] + " ") + '\n'
        plus = "+"
        fout.write(line)
        
    f.close()
    fout.close()

    print "Input file %s quoted and written to %s" % (inputname, outputname)

    
    
