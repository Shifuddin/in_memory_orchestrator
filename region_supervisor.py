#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 23:55:00 2018

@author: shifu
"""
import city_map as cm
from in_memory_dao import Dao_in_memory
class Regionsupervisor():
    
    def __init__(self, region_name):
        self.region_name = region_name
        self.in_memory_dao = Dao_in_memory(region_name)
        
    def get_blocks(self):
    
        blocks = self.in_memory_dao.get_all_blocks()
        
        for block in blocks:
            print (block)
            
    def get_region_map(self):
        return cm.get_adjacency_list(self.region_name)
    