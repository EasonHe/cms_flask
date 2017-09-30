import  pickle,bcrypt
from conf import config
import  os

pik = config.WORKPATH + 'sec/pick.pkl'
def query_user(username):
    with open(pik, 'r') as f:
        users = pickle.load(f)
    for user in users:
        if user['username'] == username:
            return user


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

makesex('hewei','Hell!@#')
#user=query_user('hewei')
#print  user['password']
#print bcrypt.checkpw('123456', user['password'].encode('utf-8'))