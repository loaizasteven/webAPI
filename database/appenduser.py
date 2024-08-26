import json
import os
import os.path as osp

from typing import Dict
from operator import itemgetter

def format_user(username:str, password:str) -> Dict:
    # Get elements
    getnames = itemgetter(0, -1)
    name_elements = username.split(' ')
    full_name = list(getnames(name_elements))

    nameconcat = ''.join(list(map(str.lower, full_name)))
    return {
        nameconcat: {
            "username": name_elements[0].lower(),
            "fullname":  ' '.join(list(map(str.title, name_elements))),
            "email": nameconcat + "@example.com",
            "hashed_password": password,
            "disabled": True
        }
    }

if __name__ == "__main__":
    # DataBase
    database = osp.join(osp.dirname(__file__), 'activeusers.json')

    # User Input
    static_val = ['Provide First and Last Name e.g.(John Doe) if middle name provide just the initials: ',
                'Provide Password: ']
    
    for ques in static_val:
        if "password" in ques.lower():
            pass_ = str(hash(input(ques)))
        else:
            user_ = str(input(ques))
    new_data = format_user(username=user_, password=pass_)
    # Run
    if os.path.exists(database) and os.path.getsize(database)>0:
        with open(database, 'r+') as file:
            current_users = json.load(file)
            current_users.update(new_data)
            # Set pointer to beginning of file, writing places the new content at the top of the file
            # now pointer is after the new content and then we use truncate to remove content after 
            # pointers new position
            file.seek(0)
            json.dump(current_users, file, indent=4)
            file.truncate()
    else:
        raise('File Does Not Exist or is Empty')
