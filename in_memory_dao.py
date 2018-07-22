#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 10:56:06 2018

@author: shifu
"""

from pydblite import Base

class Dao_in_memory():
    
    def __init__(self, region_name):
        self.db = Base(region_name, save_to_file=False)
        self.db.create('address', 'band', 'latency', 'resources', mode="override")
    
    def add_blocks(self, blocks):
        
        for block in blocks:
            self.db.insert(address=block.get('address'), band=block.get('band'),
                       latency=block.get('latency'), resources=block.get('resources'))
    
    def get_block(self, address):
        
        try:
            block = self.db(address=address)[0]
            return block
        except IndexError:
            return None
        
    def get_all_blocks(self):
        
        return self.db
        
    
        