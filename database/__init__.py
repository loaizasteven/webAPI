import os
import json
import os.path as osp

USERDATABASE = json.load(open(osp.join(osp.dirname(__file__), 'activeusers.json'), 'rb'))
USERQUESTIONS = ['Provide First and Last Name e.g.(John Doe) if middle name provide just the initials: ',
                'Provide Password: ']
