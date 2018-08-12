#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 11:49:35 2018

@author: shifu
"""
from region_supervisor import Regionsupervisor
from service_scheduler import Scheduler
from queue import Queue
class Engine():
    def __init__(self, engine_name):
        self.engine_name = engine_name
        self.service_queue = Queue()
        self.region_sp = Regionsupervisor()
        
        for i in range(6):
            t = Scheduler(self.region_sp, self.service_queue, i)
            t.setDaemon(True)
            t.start()
        
        
    
    def assign_service_to_service_queue(self, service_id, task_details, origin_node, algorithm, level, generation, mutation_factor, scheduling_policy):
        #self.scheduler.schedule(task_details, origin_node, algorithm, level, generation, mutation_factor)
        service_entity = {}
        service_entity['service_id'] = service_id
        service_entity['task_details'] = task_details
        service_entity['origin_node'] = origin_node
        service_entity['algorithm'] = algorithm
        service_entity['level'] = level
        service_entity['generation'] = generation
        service_entity['mutation_factor'] = mutation_factor
        service_entity['scheduling_policy'] = scheduling_policy
        self.service_queue.put(service_entity)
    
    def join_threads(self):
        self.service_queue.join()
    def add_map(self, city_map):
        self.region_sp.add_map(city_map)
        
    def get_map(self):
        return self.region_sp.get_map()
    def add_blocks(self, blocks):
        self.region_sp.add_blocks(blocks)
    def update_blocks(self, blocks):
        self.region_sp.update_blocks(blocks)
    def get_blocks(self):
        return self.region_sp.get_blocks()