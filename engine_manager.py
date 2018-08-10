#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 22:10:00 2018

@author: shifu
"""
from orch_engine_1 import Engine
class EngineManager():
    def __init__(self, city_map):
        #self.engine_list = []
        #self.dao = dao
        #self.create_engine_on_startup()
        self.engine = Engine('Munich')
        self.engine.add_map(city_map)
        
    def create_engine_on_startup(self):
        blocks = self.dao.get_all_blocks()
        
        for block in blocks:
            postal_address = block.postal_address
            region_name = postal_address[postal_address.find(',')+2: postal_address.rfind(',')]
            city_name = postal_address[postal_address.rfind(',')+2:]
            self.create_new_engine(city_name+'_'+region_name, block)
            
    def check_engine_exists(self, engine_name):
        engine_index = 0
        for engine in self.engine_list:
            
            if engine.engine_name == engine_name:
                return True, engine_index
            engine_index +=1
        return False, -1
        
    def create_new_engine(self, engine_name, block):
        '''
        Create new engine and pass resource to that engine
        '''
        exists, index = self.check_engine_exists(engine_name)
        if exists:
            self.engine_list[index].region_su.in_memory_dao.add_new_block(block)
            print ('Engine already exists. Data added')
        else:
            
            orch_en = Engine(engine_name)
            orch_en.region_su.in_memory_dao.add_new_block(block)
            self.engine_list.append(orch_en)
    
    def update_blocks(self, blocks):
        self.engine.update_blocks(blocks)
        
    def place_blocks(self, blocks):
        '''
        Take blocks from resouce pool to be added to the database
        '''
        
        self.engine.add_blocks(blocks)
        '''
        for block in blocks:
            if self.dao.add_new_block(block):
                postal_address = block.get('postal_address')
                region_name = postal_address[postal_address.find(',')+2: postal_address.rfind(',')]
                city_name = postal_address[postal_address.rfind(',')+2:]
                self.create_new_engine(city_name+'_'+region_name, block)
            else:
                print ("Block already exists. Need block update or resource update")
        '''         
        
    def place_service(self, service_id, task_details, origin_node, algorithm, level, generation, mutation_factor, scheduling_policy):
        
        self.engine.assign_service_to_service_queue(service_id, task_details, origin_node, algorithm, level, generation, mutation_factor, scheduling_policy)
        '''
        origin_postal_address = origin_node.get('postal_address')
        region_name = origin_postal_address[origin_postal_address.find(',')+2: origin_postal_address.rfind(',')]
        city_name = origin_postal_address[origin_postal_address.rfind(',')+2:]
        engine_name = city_name + '_'+ region_name
        for engine in self.engine_list:
            if engine_name == engine.engine_name:
                engine.assign_service_to_scheduler(task_details, origin_node)
        '''
    def wait_for_finish(self):
        self.engine.join_threads()
    def inspect_engine(self):
        city_map = self.engine.get_map()
        print (city_map)
        print (len(city_map))
        
        blocks = self.engine.get_blocks()
        
        for block in blocks:
            print (block)
        #print (len(available_blocks))
        
        
        
        
        