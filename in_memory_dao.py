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
        self.db.create('postal_address', 'band', 'latency', 'resources', mode="override")
    
    def add_new_block(self, block):
        self.db.insert(postal_address=block.postal_address, band=block.band,
                       latency=block.latency, resources=block.resources)
    
    def get_block_from_postal_address(self, address):
        blocks = self.db(postal_address=address)
    
        if len(blocks) > 0:
            return blocks[0]
        else:
            return None
    def get_all_blocks(self):
        
        for r in self.db:
            yield r
        
    
        