# coding=utf-8
import  pickle
import  codecs
import subprocess
import  os
import signal
import  datetime
import  psutil
class Get_data:
    @staticmethod
    def Get_all(name):
        with open(name, 'r') as f:
            temple = pickle.load(f)
        return temple




class Runing:

    @staticmethod
    def run_py(l,k,name,script):
        if l == 0 and k == 0:
            print script
            scriptname =  '{}.py'.format(name)
            with  codecs.open(scriptname,'wb','utf-8') as f:
                f.write(script)
            with open('{}.log'.format(name),'w') as f:
                 f.write('start {}\n'.format(datetime.datetime.now()))
            try:
                ret=subprocess.Popen(['python' ,'./{}'.format(scriptname) ],close_fds=True,stderr=subprocess.PIPE)
                pid = ret.pid
                runscript.in_run[name]=pid
                ret.wait(timeout=10)
                erro=ret.stderr.read()
                if len(erro) != 0:
                    with open('{}.log'.format(name), 'a') as f:
                        f.write('errro {}'.format(erro))
                with open('{}.log'.format(name), 'a') as f:
                    f.write('finish {}'.format(datetime.datetime.now()))
                if  psutil.pid_exists(runscript.in_run[name]):
                    os.kill(pid,signal.SIGKILL)
                runscript.in_run.pop(name)
            # execfile("./{}".format(scriptname))
            #is python 3 use exex if python2 shi low  use exexfile
            #exec(open("./{}".format(scriptname)).read())
            #runpy.run_path("./{}".format(scriptname))
            except Exception as e:
                with open('{}.log'.format(name), 'a') as f:
                    f.write('{}'.format(e))
                    return '{}'.format(e)
            return '{} run finish'.format(name)

class runscript:
    in_run = {}
    @classmethod
    def Run(cls,name):
        temple= Get_data.Get_all(name)
        name = temple.get('name')
        stype = temple.get('stype')
        inputval = temple.get('inputval')
        paras = temple.get('paras')
        script = temple.get('script')
        script = script.replace('\r\n', '\n')
        print runscript.in_run
        if runscript.in_run.has_key(name):
            return 'runing now wating...'
        if stype == 'python':
           l= len(inputval)
           k= len(paras)
           return Runing.run_py(l,k,name,script)
        return '{},,,,{}'.format(l,k)

class stop_task:
    @classmethod
    def Stop(cls,name):
        if  runscript.in_run.has_key(name):
            os.kill(runscript.in_run[name],signal.SIGKILL)
            return 'have stop'
        else:
            return 'task not exist'