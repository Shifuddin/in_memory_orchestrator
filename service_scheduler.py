#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 23:20:16 2018

@author: shifu
"""

from genetic_algorithm import GeneticAlgorithm
from sequential_algorithm import Sequential_Algorithm
class Scheduler():
    def __init__(self, region_supervisor):
        self.region_sp = region_supervisor
        self.genetic = GeneticAlgorithm(region_supervisor)
        self.sequential = Sequential_Algorithm(region_supervisor)

    '''
    def get_exec_time(self, resource, band, latency,from_origin):
        
        avg_band = (self.origin_block.get('band') + band) /2
        if from_origin == True:
            total_latency = 0
        else:
            total_latency = (self.origin_block.get('latency') + latency)
        
        cpu_time = (self.task_details.get('cpu_mips_profiled_machine')/ resource.cpu_mips) * Decimal(self.task_details.get('cpu_time_predicted_sc'))
        avg_wt = resource.avg_wt
        dtt = Decimal(self.task_details.get('data_size_mb') / avg_band) + Decimal(Decimal((self.task_details.get('data_size_mb') / 64 ) )* total_latency)
            
        total_ex_time = cpu_time + avg_wt + dtt            
        
        return total_ex_time
    

    '''
    
    def find_band_latency_origin(self,origin_building):
        try:
            origin_block = self.region_sp.get_block(origin_building)
            return origin_block.get('band'), origin_block.get('latency')
        except Exception:
            return None, None
        
    def bfs_traversal(self, graph, origin, level):
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
        
    
  
    def schedule(self, task_details, origin_node, algorithm, level, generation, mutation_factor):
        
    
        origin_band, origin_latency = self.find_band_latency_origin(origin_node)
    
        
        bfs_result = self.bfs_traversal(self.region_sp.get_map(), origin_node, level)
        
        if algorithm == 'sequential_all':
        
            computing_nodes = self.sequential.find_available_computing_nodes(task_details, origin_band, origin_latency, bfs_result, True)
        
            print (computing_nodes)
            
        elif algorithm == 'sequential_fast':
        
            computing_nodes = self.sequential.find_available_computing_nodes(task_details, origin_band, origin_latency, bfs_result, False)
        
            print (computing_nodes)
        
        elif algorithm == 'genetic_algo':
            self.genetic.get_matching_node(bfs_result, origin_band, origin_latency, task_details, generation, mutation_factor)
            
            


        
 
        