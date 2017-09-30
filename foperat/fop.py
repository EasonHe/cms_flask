import  os
import shutil
def createdir(pathname):
    pathname =str(pathname).strip()
    if '/'  in pathname or '..' in pathname:
        return 'name erro'
    if os.path.exists(pathname):
        return  'dir is exist'
    else:
        os.mkdir(pathname)
        return  '{} is ok'.format(pathname)


def createfile(filename):
    filename=str(filename).strip()
    try:
        ch = ["/","&","..","~"]
        for li in ch:
            if li in filename:
                print  'err'
                return 'name erro'
        if os.path.isfile(filename):
            print 'exist'
            return "{} is exist".format(filename)
        else:
            os.mknod(filename)
            return  '{}is touch'.format(filename)
    except Exception as e:
            print  e,
            return 'err {} '.format(filename)


def dell(filename):
    try:
        ch = ["/", "&", ".." "~"]
        for li in ch:
            if li in filename:
                print  'name err'
                return 'name erro'
        if os.path.isdir(filename):
            os.removedirs(filename)
            return 'dir {} have del'.format(filename)
        if os.path.isfile(filename):
            os.remove(filename)
            return 'file {} have del '.format(filename)
        else:
            print 'file  not exist'
            return 'file  not exist'
    except Exception as e:
        print e
        return   'err del{}'.format(filename)

def rmtree(filename):
    try:
        ch = ["/", "&", ".." "~"]
        for li in ch:
            if li in filename:
                print  'name err'
                return 'name erro'
        if os.path.isdir(filename):
            shutil.rmtree(filename)
            return 'dir {} have del'.format(filename)
        if os.path.isfile(filename):
            os.remove(filename)
            return 'file {} have del '.format(filename)
        else:
            print 'file  not exist'
            return 'file  not exist'
    except Exception as e:
        print e
        return 'err rm {}'.format(filename)






