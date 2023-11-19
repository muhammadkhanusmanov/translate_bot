import json 
class DB:
    def __init__(self):
        try:
            with open('db.json', 'r') as f:
                self.db = json.load(f)
        except FileNotFoundError:
            self.db = {
                "users":{
                }
            }
            with open('db.json', 'w') as f:
                json.dump(self.db, f, indent=4)
    def save(self):
        with open('db.json', 'w') as f:
            json.dump(self.db, f, indent=4)
    
    def starting(self,chat_id):
        self.db["users"][str(chat_id)] = 'en-uz'
        return None
    
    def change(self,chat_id,til):
        self.db["users"][str(chat_id)] = til
        return None
    
    def get_lang(self,chat_id):
        return self.db["users"][str(chat_id)]
    
    def check_admins(self,chat_id):
        if str(chat_id) in self.db["admins"].keys():
            return True
        return False
    
    def allusers(self):
        return self.db["users"].keys()
    
    def ruxsatlar(self,chat_id):
        return self.db['admins'][str(chat_id)]
    
    def rfwd(self,chat_id, cmnd=False):
        self.db['admins'][str(chat_id)]['fwdmsg'] = cmnd
        return None
    
    def rmsg(self,chat_id, cmnd=False):
        self.db['admins'][str(chat_id)]['msg'] = cmnd
        return None
    
    def changer(self,chat_id,i,cmnd=False):
        self.db['admins'][str(chat_id)][i]=cmnd
        return None
    
    def add(self,chat_id,i,adding):
        if i=='admin':
            self.db['admins'][str(chat_id)]={
            "fwdmsg": False,
            "msg": False,
            "addd":False,
            "removed":False,
            "addc":False,
            "removec":False
            }
        else:
            self.db[i].append(adding)
        return None
    
    def delete(self, chat_id):
        self.db['admins'].pop(str(chat_id))
        return None
    
    def alladmins(self):
        return self.db['admins'].keys()