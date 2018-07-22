#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 23:55:00 2018

@author: shifu
"""
from in_memory_dao import Dao_in_memory
class Regionsupervisor():
    
    def __init__(self):
        self.in_memory_dao = Dao_in_memory('temp')
    
    def add_map(self, city_map):
        self.city_map = city_map
    
    def get_map(self):
        return self.city_map
    
    def add_blocks(self, blocks):
        self.in_memory_dao.add_blocks(blocks)
    def get_blocks(self):
    
        blocks = self.in_memory_dao.get_all_blocks()
        
        return blocks
    def get_block(self, address):
        return self.in_memory_dao.get_block(address)
            
