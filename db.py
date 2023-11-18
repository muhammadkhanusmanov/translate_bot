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