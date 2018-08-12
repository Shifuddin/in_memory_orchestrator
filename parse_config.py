# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 02:21:10 2018

@author: shifuddin
"""

import yaml
def get_config_dict(config_file):
    with open(config_file, 'r') as stream:
        config_dic = yaml.load(stream)
    return config_dic

con = get_config_dict('config.yaml')
print (con.get('ga_properties').get('threshold'))