#config.py
import os,sys
confpath = os.path.split(os.path.realpath(__file__))[0]
WORKPATH =  confpath.replace('conf','') 
WORKSPACE =  confpath.replace('conf','workspace')
WORKFILE = confpath.replace('conf','workfile/')

