#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 11:49:35 2018

@author: shifu
"""
from region_supervisor import Regionsupervisor
from service_scheduler import Scheduler
class Engine():
    def __init__(self, engine_name):
        self.engine_name = engine_name
        self.region_su = Regionsupervisor()
        self.scheduler = Scheduler(self.region_su)
    
    def assign_service_to_scheduler(self, task_details, origin_node, algorithm, level, generation, mutation_factor):
        self.scheduler.schedule(task_details, origin_node, algorithm, level, generation, mutation_factor)
    
    def add_map(self, city_map):
        self.region_su.add_map(city_map)
        
    def get_map(self):
        return self.region_su.get_map()
    def add_blocks(self, blocks):
        self.region_su.add_blocks(blocks)
    def get_blocks(self):
        return self.region_su.get_blocks()