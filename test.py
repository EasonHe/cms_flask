import os
import  git
from  conf import config
def git_op():
    g = git.Repo("/root/gzw/workfile/afuos-config")
    #g.git.checkout('demo' )
    #g.git.pull()
    print  "baranch is :",g.git.status()

    #g.git.commit('''-am "{}" '''.format('test'))
    g.git.push()
    #g.git.add('/root/gzw/workfile/afuos-config/nginx/test')
    print  g.git.status()

def git_clone(giturl="ssh://git@gitlab.raiyee.cn:10022/afuos/afuos-config.git",dir="/root/gzw/workfile/",b='master'):
    osp=''
    #repo = git.Repo.clone_from(giturl, osp.join(["./","afuos-config"]), branch=b)

#git_op()
#print type(indir)
#print config.WORKFILE
git_op()