import json
import os
import os.path as osp
import sys

from typing import Dict
from operator import itemgetter

import warnings

sys.path.insert(0, osp.dirname(osp.dirname(__file__)))
from database import USERQUESTIONS

def format_user(username:str, password:str) -> Dict:
    name_elements = username.split(' ')
    assert len(name_elements) < 4, "UserName should be at most three words"
    # Get elements
    getnames = itemgetter(0, -1)
    full_name = list(getnames(name_elements))

    if len(name_elements)>2 and len(name_elements[1])>1:
        warnings.warn("Middle name should only be an Initial. We'll fix it for you")
        name_elements[1] = name_elements[1][0].upper()

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

def hashinput(val:str) -> str:
    return str(hash(val)) 


if __name__ == "__main__":
    # DataBase
    database = osp.join(osp.dirname(__file__), 'activeusers.json')

    # User Input
    for ques in USERQUESTIONS:
        reponse = input(ques)
        if "password" in ques.lower():
            pass_ = hashinput(reponse)
        else:
            user_ = reponse

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
