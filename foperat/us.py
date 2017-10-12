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

