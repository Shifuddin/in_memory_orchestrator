#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 18:39:29 2018

@author: shifu
"""
from decimal import Decimal
class Sequential_Algorithm():
    
    def __init__(self, region_sp):
        self.region_sp = region_sp
        print ('Sequential created')
    
    def calculate_expected_exec_time(self, resource_avg_wt, resource_cpu_mips, avg_band, total_latency):
                
        avg_wt = Decimal(resource_avg_wt)
        cpu_time = Decimal((self.task_details.get('cpu_mips_profiled_machine')/ resource_cpu_mips)) * Decimal(self.task_details.get('cpu_time_predicted_sc'))
       
        dtt = Decimal(self.task_details.get('data_size_mb') / avg_band) + Decimal(Decimal((self.task_details.get('data_size_mb') / 64 ) )* Decimal(total_latency))
        
        total_ex_time = cpu_time + avg_wt + dtt            
            
        return total_ex_time
    
    def find_available_computing_nodes(self, task_details, origin_band, origin_latency, bfs_result, all_nodes):
    
        self.task_details = task_details
        
        total_computing_nodes = []
        origin_block = True
    
        for v in bfs_result:
            try:
                block = self.region_sp.get_block(v)
                
                if block is not None:
                    resources = block.get('resources')
                    
                    avg_band = (origin_band + block.get('band')) /2
                    total_latency = (origin_latency + block.get('latency'))
                    
                    if origin_block == True:
                        total_latency = 0
                        origin_block = False
                    for resource in resources:
                        expected_exe_time = self.calculate_expected_exec_time(resource.get('avg_wt'), resource.get('cpu_mips'), avg_band, total_latency )
                        
                        memory_mb = resource.get('memory_mb')
                        
                        if expected_exe_time <= self.task_details.get('required_exe_time_sc') and memory_mb >= self.task_details.get('required_memory_mb'):
                            
                            computing_node = {}
                            computing_node['address'] = v
                            computing_node['ip'] = resource.get('ip')
                            computing_node['expected_ex_time'] = expected_exe_time
                            computing_node['avail_mem_mb'] = memory_mb
                            
                            if all_nodes == False:
                                if len(total_computing_nodes) >= 2:
                                    return total_computing_nodes
                            total_computing_nodes.append(computing_node)
            except IndexError as IE:
                print (str(IE))
        return total_computing_nodes    