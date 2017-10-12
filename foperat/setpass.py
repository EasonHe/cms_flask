import  pickle,bcrypt,os
import sys
sys.path.append("../conf")
import config
import  getpass
pik = config.WORKPATH + 'sec/pick.pkl'


def makesex(username,password):
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    u = {'id':hash(username),'username':username,'password':hashed}
    print u

    print pik
    if os.path.isfile(pik):
        with open(pik,'r') as f:
            data=pickle.load(f)
            for user in data:
                if user['username'] ==username:
                    data.remove(user)
                data.append(u)
        with open(pik,'w') as f:
            pickle.dump(data,f)
    else:
        users = []
        users.append(u)
        f = open(pik,'w')
        pickle.dump(users,f)
        f.close()
    print "\033[36mpassword set ok"

def set_user():
    print "\033[34mplease enter username"
    username=raw_input('>>>').replace(' ','')
    print "\033[31mplease enter password"
    password1 = getpass.getpass().replace(' ','')
    print "\033[31mplease confirm password "
    password2 = getpass.getpass().replace(' ', '')
    if password1 == password2:
        password = password1
        print "{}\n{}".format(username,password)
        makesex(username,password)
    else:
        print "wrong two password enter"


if __name__ == "__main__":
    set_user()
