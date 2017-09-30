import os
import pickle
from flask import Flask, render_template, redirect, url_for, request, flash,jsonify
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, logout_user, current_user, login_required, fresh_login_required, \
    login_user
from gevent import monkey
from conf import config
from foperat import fop
from  foperat.gitop import gitcontrol
from foperat.srun import runscript, stop_task
from  foperat.us import query_user
monkey.patch_all()
from  gevent  import pywsgi
import  json
import bcrypt
app = Flask(__name__)
app.secret_key = '12345dsfdsfdsfdsfdsfdsfdsfdsfds67'
login_manager = LoginManager(app)
login_manager.init_app(app)

login_manager.login_message = 'Unauthorized User'
login_manager.login_message_category = "info"
login_manager.session_protection = "strong"
bootstrap = Bootstrap(app)

class User(UserMixin):
    pass
@login_manager.user_loader
def load_user(username):
    if query_user(username) is not None:
        curr_user = User()
        curr_user.id = username
        return  curr_user

@login_manager.unauthorized_handler
def unauthorized_handler():
    return  'Unauthorized'


@app.route('/')
@fresh_login_required
def index():
    return   render_template('index.html')



@app.route('/home')
@fresh_login_required
def home():
    return  'LOgged in as {}:'.format(current_user.get_id())

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = str(request.form.get('password'))
        user =  query_user(username)
        if user is not None and  bcrypt.checkpw(password,user['password'].encode('utf-8')):
            curr_user = User()
            curr_user.id = username
            login_user(curr_user,remember=True)
            #nex = request.args.get('next')
            return redirect(request.args.get(next) or url_for('index'))
        #flash('Wrong username or password')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return  redirect(url_for('login'))

@app.route('/edt/<path:file>',methods=['POST','GET'])
@login_required
def edt(file):
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")
    showfile=file
    showdir=str(file).rsplit('/',1)[0]
    print showdir
    root =config.WORKPATH
    os.chdir(root)
    file = root + file
    file = file.replace('//','/')
    nowfile = file.replace(root,'')
    print file
    if request.method == 'POST':
        ft = request.form.get('ft')
        print ft
        with open(file,'w') as chfile:
            chfile.write(ft)
    #with open(file) as f:
    newline = ''
    with open(file) as f:
        for line in f:
            newline += line


    return render_template('edt.html',filename=newline,showdir=showdir,file=nowfile)

@app.route('/showdir/<path:dir>',methods=['POST','GET'])
@login_required
def showdir(dir):
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")
    dir=str(dir)
    print dir
    os.chdir('{}{}'.format(config.WORKPATH,dir))
    files=os.listdir('.')
    getdir = os.getcwd()
    getdir = getdir.replace(config.WORKPATH,'')
    getdir= getdir.strip()
    superior=getdir.rsplit('/',1)
    superior = '/showdir/' +superior[0]
    print superior,11111
    Str = ''
    for file in files:
        if os.path.isfile(file):
            a = "<a href='/edt/{}/{}'>{}</a><br>".format(dir,file,file)

        else:
            a = "<a href='/showdir/{}/{}'>{}/</a><br>".format(dir,file,file)

        Str = Str + a

    return render_template('showlist.html',top=Str,sent=getdir,superior=superior)

@app.route('/filedt',methods=['POST'])
@login_required
def filedt():
    if request.method == 'POST':
        os.chdir(config.WORKPATH)
        dir = request.form.get('dir')
        filename = request.form.get('filename')
        filetype = request.form.get('fd')
        filename = str(filename)
        #print filetype,filename,dir
        if filetype in 'none':
             return "don't post none to me,so sb!"
        d = config.WORKPATH + dir
        os.chdir(d)
        print filetype
        if filetype == 'dir':
            if len(filename) == 0:
                return 'you file name is null'
            return fop.createdir(filename)
        if filetype == 'file':
            if len(filename) == 0:
                return 'you file name is null'
            return  fop.createfile(filename)
        if filetype == 'del':
            if len(filename) == 0:
                return 'you file name is null'
            return  fop.dell(filename)
        if filetype == 'rmtree':
            if len(filename) == 0:
                return 'you file name is null'
            return  fop.rmtree(filename)
        if filetype == 'clone':
            if len(filename) == 0:
                return 'you file name is null'
            filename=str(filename)
            b,url = filename.split()
            return gitcontrol.clone(url,b)
        if filetype == 'pull':
            branch = filename.strip()
            if len(branch) == 0:
                return gitcontrol.pull()
            return  gitcontrol.branpull(branch)
        if filetype == 'gitadd':
            filename = filename.strip()
            msg = 'add  {}'.format(filename)
            return gitcontrol.gitaddf(filename,msg)
        if  filetype == 'gitfdel':
            return gitcontrol.gitfdel(filename)

    return 'false'
@app.route('/commit', methods=['POST'])
def commit():
    os.chdir(config.WORKPATH)
    path = request.form.get("path")
    msg = request.form.get("msg")
    path=str(path).split('/showdir/',1)[1]
    print msg
    post = {"path": path,
           "msg": msg}
    print post
    os.chdir(path)
    ret = gitcontrol.commit(msg)
    print  ret
    return  ret

@app.route('/task')
@login_required
def task():
    os.chdir(config.WORKSPACE)
    files=os.listdir('.')
    lists= ''.join('''<tr class='active'><td><button class="btn-warning" onclick='del(this)' value={}>delete</button> {}</td><td><a href='/task/pedt/{}'>{}</a></td>
       <td><a name="{}"class='btn'><img src='static/img/clock.png'>action</a></td><td><a href='/task/read_log/{}'>log</a></td><td><a name ='{}' onclick='stop(this)'>stop</a></td></tr>'''.format(fs,fs,fs,fs,fs,fs,fs,fs)  for fs in files)
    return render_template('task.html',lists=lists)

@app.route('/task/run',methods=['POST','GET'])
@login_required
def run():

    if request.method == 'POST':
        name = request.form.get('name')
        dir= '{}{}'.format(config.WORKSPACE,name)
        os.chdir(dir)
        return runscript.Run(name)
    return  redirect(url_for(task))

@app.route('/task/stop')
@login_required
def stop():
    return stop_task.Stop(request.args.get('name'))


@app.route('/task/create_t',methods=['POST'])
@login_required
def create_t():
     name= str(request.form.get('name')).strip().replace(' ','')
     ty= request.form.get('type')
     if len(name) != 0:
         print os.getcwd()
         dir = config.WORKSPACE
         os.chdir(dir)
         if os.path.exists(name):
             return 'exit'
         else:
            os.makedirs(name)
            os.chdir(name)
            temple = {"name":name,"stype":ty,"inputval":'',"paras":'',"script":
'''import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/"+"../../")
from pymethod.pymethod import Filechan ,CMD_run
hostname = ''
username = 'nginx'
password = None
logname='{}'
local_dir=''
remote_dir=''
#Filechan.diruploaddir(local_dir=local_dir,remote_dir=remote_dir,hostname=hostname,port=22,logname=logname)
#CMD_run.run_cmd(hostname,username,password=password,cmd=cmd,logname='he')
#Filechan.rm_fd(hostname=hostname,username=username,prmdir='/tmp/test/sss',logname=logname)
#Filechan.uplodfile(hostname=None,username=None,port=22,password=None,localfile=None,rmotefile=None,logname=None):
'''.format(name)}
            with open(name,"w") as f:
                pickle.dump(temple,f)
         return 'ok'
     return 'plese input name'

@app.route('/task/delete',methods=['POST'])
@login_required
def delete():
    name = str(request.form.get('name')).strip()
    print name
    os.chdir(config.WORKSPACE)
    print os.getcwd()
    return fop.rmtree(name)

@app.route('/task/pedt/<path:name>',methods=["GET","POST"])
@login_required
def pedt(name):
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")
    dir = config.WORKSPACE + "/" + name
    os.chdir(dir)
    print os.getcwd()
    with open(name,'r') as f:
        temple = pickle.load(f)
    print temple
    name=temple.get('name')
    stype = temple.get('stype')
    inputval = temple.get('inputval')
    paras = temple.get('paras')
    script =temple.get('script')
    if request.method=="POST":
        Name = request.form.get('name')
        Stype = request.form.get('stype')
        Inputval= request.form.get('inputval')
        Paras = request.form.get('paras')
        Script = request.form.get('script')
        temple = {"name": Name, "stype": Stype, "inputval": Inputval, "paras": Paras, "script": Script}
        with open(name,'w') as f:
            pickle.dump(temple,f)
        return redirect(url_for('task'))

    return  render_template('taskedt.html',name=name,stype=stype,inputval=inputval,paras=paras,script=script)

@app.route('/task/read_log/<path:file>',methods=['GET','POST'])
@login_required
def red_log(file):
    path = config.WORKSPACE + "/" + file
    try:
       os.chdir(path)
    except KeyError:
        print 'key erro'
    if request.method == 'POST':
        filename= request.form.get('name')
        with open('{}.log'.format(filename),'r') as f:
           log =f.readlines()
           lines =''
           for line in log:
               lines =lines  + line.replace('\n','<br/>')

           if 'finish' in lines:
               kg= 'off'
           else:
               kg = 'on'
           data = {
               'nowstat': kg,
               'log': lines
           }
           return json.dumps(data)
    return  render_template('read_log.html', path=file)
if __name__ == '__main__':
   # app.run(host='0.0.0.0',debug=True)
    server = pywsgi.WSGIServer(('0.0.0.0',5000),app)
    server.serve_forever()
