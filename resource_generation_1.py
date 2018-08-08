#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 15:17:31 2018

@author: shifu
"""
from random import randint, choice, uniform
import string    

def generate_buildings(number):
    city_buildings = set([])
    for i in range(number):
        first_part = choice(string.ascii_uppercase)
        second_part = ''.join(choice(string.ascii_lowercase) for j in range(5))
        third_part = randint(1, 50)
        
        city_buildings.add(first_part+second_part + ' ' + str(third_part))  
    
    return city_buildings


def create_adjacency_list_buildings(buildings):
    
    graph_adjacency_list = {}
    
    for building in buildings:
        building_adjacency = set([])    
            
        for i in range(4):
            building_adjacency.add(choice(buildings))
                
        graph_adjacency_list[building] = building_adjacency
                
    return graph_adjacency_list
def generate_computing_nodes(buildings):
    
    resources = []

    for building in buildings:
        resource = {}
        resource['address'] = building
        resource['band'] = randint(3300, 4000)
        resource['latency'] = uniform(0, 0.5)
        
        nodes = []
        for j in range (10):
            node = {}
            node['ip'] = str (randint (10, 20)) + '.' + str(randint(20, 30)) + '.' + str (randint (30, 50)) + '.' + str(randint(50, 70))
            node['cpu_mips'] = randint (3300, 4000)
            node['memory_mb']= randint(3000, 6000)
            node['avg_wt'] = uniform(0,1)
            nodes.append(node)
        resource['resources'] = nodes
        resources.append(resource)
    return resources

def generate_origin_iot():
    '''
    create static single resource properties
    '''
    #postal_code, address = generate_address()
    resource = {
        
        'postal_address': 'Hans-Leipelt-Str 2, 80805, Munich' ,
        'ip': '10.10.11.11'
        }
    return resource

def generate_task_details():
    
    task_details = {
        'cpu_time_predicted_sc': uniform(1, 6),
        'cpu_mips_profiled_machine': randint(3300, 4000),
        'required_exe_time_sc': uniform(3, 5),
        'data_size_mb': randint(200, 400),
        'required_memory_mb': randint(2500, 4500)
            }
    return task_details