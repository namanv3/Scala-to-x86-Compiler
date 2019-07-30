#!/usr/bin/python

import ply.lex as lex
import string
from tokens import *
from reserved_words import *
from regex import *
import sys, getopt
import re

lexer = lex.lex()
