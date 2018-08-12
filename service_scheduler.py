#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 23:20:16 2018

@author: shifu
"""

from genetic_algorithm import GeneticAlgorithm
from sequential_algorithm import Sequential_Algorithm
import threading
from threading import current_thread
from random import choice
import logging


def find_band_latency_origin(region_sp, origin_building):
    try:
        origin_block = region_sp.get_block(origin_building)
        return origin_block.get('band'), origin_block.get('latency')
    except Exception:
        return None, None

def bfs_traversal(graph, origin, level):
    result, queue = [], []
    current_level = 0
    queue.append(origin)
    queue.append(None)
    result.append(origin)
    current_level += 1
    
    if current_level == level:
        return result
    try:
        while queue:
            
            element = queue.pop(0)
                
            if element == None:
                queue.append(None)
                element = queue.pop(0)
                current_level += 1
                    
                if current_level == level:
                    return result
            for adja in graph[element]:
                if adja not in result:
                    queue.append(adja)
                    result.append(adja)
        return result
    except KeyError as KE:
        print (str(KE))
    except IndexError as IE:
        print (str(IE))
    except Exception as e:
        print (str(e))
    return result
    
class InitialState(object):
        
    def perform(self, service_entity, scheduling_result, level):
        return 1, scheduling_result, level

class SchedulingState(object):
    
    def __init__(self, region_sp, genetic):
        self.region_sp = region_sp
        self.genetic= genetic
        
    def perform(self, service_entity, scheduling_result, level):
        
        origin_node = service_entity.get('origin_node')
        task_details = service_entity.get('task_details')
        generation = service_entity.get('generation')
        mutation_factor = service_entity.get('mutation_factor')
        
        origin_band, origin_latency = find_band_latency_origin(self.region_sp, origin_node)
    
        
        bfs_result = bfs_traversal(self.region_sp.get_map(), origin_node, level)
        
        scheduling_result, indicator =self.genetic.get_matching_node(bfs_result, origin_band, origin_latency, task_details, generation, mutation_factor)
        
        logging.info (str(service_entity['service_id']) + ' in scheduling stage')
        if indicator == -1:
            scheduling_policy = service_entity.get('scheduling_policy')
            if scheduling_policy == 2:
                return 4, scheduling_result, level
            else:
                return 5, scheduling_result, level
        elif indicator == 0:
            return 2, scheduling_result, level
        elif indicator == 1:
            scheduling_policy = service_entity.get('scheduling_policy')
            
            if scheduling_policy == 2:
                return 4, scheduling_result, level
            elif scheduling_policy == 1:
                return 5, scheduling_result, level
            else:
                return 3, scheduling_result, level
class DispatchState(object):
    
    def perform(self, service_entity, scheduling_result, level):
        logging.info ( str(service_entity['service_id'])+' dispatched to ' + str(choice(list(scheduling_result.items()))))
        return 0, scheduling_result, level


class RecalculationState(object):
    
    def perform(self, service_entity, scheduling_result , level):
        logging.info (str(service_entity['service_id']) + ' in re-calculation stage')
        return 2, scheduling_result, level

class RetryState(object):
    
    def perform(self, service_entity, scheduling_result , level):
        logging.info (str(service_entity['service_id']) + ' in retry stage')
        level += 1
        return 1, scheduling_result, level

class HoldingState(object):
    
    def perform(self, service_entity, scheduling_result, level):
        logging.info(str(service_entity['service_id']) + ' in holding stage')
        return 0, scheduling_result, level


class Scheduler(threading.Thread):
    def __init__(self, region_supervisor, service_queue, threadnumber):
        threading.Thread.__init__(self)
        self.region_sp = region_supervisor
        self.genetic = GeneticAlgorithm(region_supervisor)
        self.sequential = Sequential_Algorithm(region_supervisor)
        self.service_queue = service_queue
        self.states = [InitialState(), SchedulingState(self.region_sp, self.genetic), DispatchState(), RecalculationState(), RetryState(), HoldingState()]
        logging.basicConfig(filename='Scheduler '+str(threadnumber)+ ' .log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def run(self):
        
    
        while True:
            service_entity = self.service_queue.get()
            level = service_entity.get('level')

            currentState = 0
            
            scheduling_result = {}
            
            while True:     
                state = self.states[currentState]
                currentState, scheduling_result, level = state.perform(service_entity, scheduling_result, level)
                if currentState == 0:
                    break
            
            self.service_queue.task_done()
        '''
        
        if algorithm == 'sequential_all':
        
            computing_nodes = self.sequential.find_available_computing_nodes(task_details, origin_band, origin_latency, bfs_result, True)
        
            print (computing_nodes)
            
        elif algorithm == 'sequential_fast':
        
            computing_nodes = self.sequential.find_available_computing_nodes(task_details, origin_band, origin_latency, bfs_result, False)
        
            print (computing_nodes)
        '''
        
        #self.genetic.get_matching_node(bfs_result, origin_band, origin_latency, task_details, generation, mutation_factor)
            
            


        
 
        