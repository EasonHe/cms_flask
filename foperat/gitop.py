#coding=utf-8
import os
import logging
import git
import json
from conf import  config
#giturl='ssh://git@gitlab.raiyee.cn:10022/afuos/afuos-config.git'

class gitcontrol:
    @classmethod
    def clone(cls,url,branch):
         name = url.rsplit("/", 1)[-1].split('.')[0]
         print "now clone ", name
         try:
             osp = ''
             repo = git.Repo.clone_from(url, osp.join(["./", name]), branch=branch)
             return "clone sccuess"
         except Exception as e:
            logging.error('clone erorr {}'.format(e))

    @classmethod
    def pull(cls):
        try:
           indir = os.getcwd()
           rootname=indir.split('workfile/')[-1].split('/')[0]
           root= config.WORKFILE + rootname
           g = git.Repo(root)
           return "a{}{}".format(str(g.git.status()),g.git.pull())
        except Exception as e:
            logging.error('git pull fail {}'.format(e))

    @classmethod
    def branpull(cls,branch):
        try:
            indir = os.getcwd()
            rootname = indir.split('workfile/')[-1].split('/')[0]
            root = config.WORKFILE + rootname
            g = git.Repo(root)
            g.git.checkout(branch)
            g.git.pull()
            return "success change to {}".format(branch)
        except Exception as e:
            logging.error('git pull fail {}'.format(e))

    @classmethod
    def gitaddf(cls,filename,msg):
        if not  os.path.isfile("./{}".format(filename)):
            os.mknod("./{}".format(filename))
        indir = os.getcwd()
        filepath = indir + '/'+ filename
        rootname = indir.split('workfile/')[-1].split('/')[0]
        root = config.WORKFILE + rootname
        try:
            g = git.Repo(root)
            g.git.add(filepath)
            g.git.commit('''-am "{}" '''.format(msg))
            g.git.push()
            return "add file {} success!".format(filename)
        except Exception as e:
            logging.error('add file error {}'.format(e))

    @classmethod
    def gitfdel(cls,filename):
        indir = os.getcwd()
        if os.path.isfile("./{}".format(filename)):
            os.remove("{}/{}".format(indir,filename))
        filepath = indir + '/'+ filename
        rootname = indir.split('workfile/')[-1].split('/')[0]
        root = config.WORKFILE + rootname
        try:
            g = git.Repo(root)
            g.git.add(filepath)
            g.git.commit('''-am "rm {}" '''.format(filename))
            g.git.push()
            return "rm file {} success!".format(filename)
        except Exception as e:
            logging.error('commt error {}'.format(e))

    @classmethod
    def commit(cls,msg):
        try:
            indir = os.getcwd()
            rootname = indir.split('workfile/')[-1].split('/')[0]
            root = config.WORKFILE + rootname
            g = git.Repo(root)
            g.git.commit('''-am "{}" '''.format(msg))
            g.git.push()
            m = {"stat": "success commit"}
            return  json.dumps(m)
        except Exception as e:
            m = {"commit": "commit false{}".format(e)  }
            logging.error('commt error {}'.format(e))
        return json.dumps(m)

class Fileop:
    @classmethod
    def makefile(cls, dir=None, file=None):
        if dir is not None:
            if not os.path.isdir(dir):
                os.makedirs(dir)
            if file is not None:
                os.chdir(dir)
                if not os.path.isfile(file):
                    os.mknod(file)

    @staticmethod
    def delfile(filename):
        try:
            ch = ["/", "&", ".." "~"]
            for li in ch:
                if li in filename:
                    print  'name err'
                    return 'name erro'
            if os.path.isdir(filename):
                return  'flse,you master del file'
            if os.path.isfile(filename):
                os.remove(filename)
                return  'ok'
            else:
                print 'file  not exist'
                return 'name erro,file not exist'
        except Exception as e:
            print e


