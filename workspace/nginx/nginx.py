import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/"+"../../")
from pymethod.pymethod import Filechan ,CMD_run
hostname = '192.168.249.138'
username = 'root'
password = None
logname='nginx'
local_dir=''
remote_dir=''
#Filechan.diruploaddir(local_dir=local_dir,remote_dir=remote_dir,hostname=hostname,port=22,logname=logname)
CMD_run.run_cmd(hostname=hostname,username=username,cmd='ip waddr',logname=logname)
#Filechan.rm_fd(hostname=hostname,username=username,prmdir='/tmp/test/sss',logname=logname)
#Filechan.uplodfile(hostname=None,username=None,port=22,password=None,localfile=None,rmotefile=None,logname=None):
