import os
import json
import os.path as osp

USERDATABASE = json.load(open(osp.join(osp.dirname(__file__), 'activeusers.json'), 'rb'))
