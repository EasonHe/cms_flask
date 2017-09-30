import paramiko,datetime,os
import logging

class w_log:
    @staticmethod
    def script_log(logname=None, info=None, warning=None, debug=None):
        logging.basicConfig(
            filename=str(logname) + '.log',
            level=logging.INFO,
            format='%(asctime)s -%(levelname)- s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        if info != None:
            logging.info('{}'.format(info))
        if warning != None:
            logging.warning('{}'.format(warning))
        if debug != None:
            logging.debug('{}'.format(debug))

class ssh_conn:
    def __init__(self,address,port=22,username=None,password=None, ssh = paramiko.SSHClient()):
        self.address = address
        self.port = port
        self.usename= username
        self.password = password
        self.ssh = ssh

    def __enter__(self):
        if self.address is not None:
            self.ssh
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(hostname=self.address,port=self.port, username=self.usename, password=self.password)
            return self.ssh
    def __exit__(self, exc_type, exc_val, exc_tb):
            self.ssh.close()
            self.ssh = None

class Filechan:

    @classmethod
    def diruploaddir(cls,local_dir=None, remote_dir=None, hostname=None, username='root', password=None, port=22,logname=None):
        try:
            SSH = ssh_conn(address=hostname,port=port,username=username,password=password)
            with SSH as ssh:
                sftp=ssh.open_sftp()
                p1= 'upload file start %s ' % datetime.datetime.now()
                print p1
                if logname != None:
                    w_log.script_log(logname=logname, info=p1)
                for root, dirs, files in os.walk(local_dir):
                    for filespath in files:
                        local_file = os.path.join(root, filespath)
                        a = local_file.replace(local_dir, '')
                        remote_file = os.path.join(remote_dir, a)
                        try:
                            sftp.put(local_file, remote_file)
                        except Exception, e:
                            sftp.mkdir(os.path.split(remote_file)[0])
                            sftp.put(local_file, remote_file)
                        p2= "upload %s to remote %s" % (local_file, remote_file)
                        print p2
                        if logname != None:
                            w_log.script_log(logname=logname, info=p2)
                    for name in dirs:
                        local_path = os.path.join(root, name)
                        a = local_path.replace(local_dir, '')
                        remote_path = os.path.join(remote_dir, a)
                        try:
                            sftp.mkdir(remote_path)
                            print "mkdir path %s" % remote_path
                        except Exception, e:
                            print e
                p3 = 'upload file success %s ' % datetime.datetime.now()
                print p3
                if logname != None:
                    w_log.script_log(logname=logname, info=p3)
        except Exception, e:
            print e
            if logname != None:
                w_log.script_log(logname=logname,debug=e)

    @classmethod
    def rm_fd(cls,hostname, username='root', password=None, port=22,prmdir=None,prmfile=None,logname=None):
        try:
            SSH = ssh_conn(address=hostname, port=port, username=username, password=password)
            with SSH as ssh:
                sftp = ssh.open_sftp()
                try:
                    if  prmdir != None:
                        sftp.rmdir(prmdir)
                        if logname != None:
                            w_log.script_log(logname=logname, info='remov dir {}'.format(prmdir))
                    if prmfile != None:
                        sftp.remove(prmfile)
                        if logname != None:
                            w_log.script_log(logname=logname, info='remov file {}'.format(prmfile))
                except Exception as e:
                    w_log.script_log(logname=logname, warning=e)
        except Exception as e:
            if logname != None:
                w_log.script_log(logname=logname,warning=e)
            print e
    @classmethod
    def uplodfile(cls,hostname=None,username='root',port=22,password=None,localfile=None,rmotefile=None,logname=None):
        SSH = ssh_conn(address=hostname, port=port, username=username, password=password)
        with SSH as ssh:
            sftp = ssh.open_sftp()
            try:
                sftp.put(localfile,rmotefile)
                if logname != None:
                    w_log.script_log(logname=logname, info='file succes put {}'.format(localfile))
            except Exception as e:
                print e
                if logname != None:
                    w_log.script_log(logname=logname, warning=e)

class CMD_run:
    @classmethod
    def run_cmd(cls,hostname=None,username='root',port=22,password=None,cmd=None,logname=None):
        SSH = ssh_conn(address=hostname, port=port, username=username, password=password)
        with SSH as ssh:
            try:
                stdin, stdout, stderr = ssh.exec_command(cmd,timeout=200)

                st = str(stdout.read())
                print st
                if logname !=None:
                    w_log.script_log(logname=logname,info=st)

                er = str(stderr.read())

                if logname != None:
                    w_log.script_log(logname=logname,warning=er)
                print line
            except Exception as e:
                if logname != None:
                    w_log.script_log(logname=logname, warning=e)
                print e