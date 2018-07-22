#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 12:26:33 2018

@author: shifu
"""
import string    
from random import choice, randint, uniform
from pydblite import Base
from decimal import Decimal

db = Base('abc', save_to_file=False)

def generate_buildings(number):
    city_buildings = set([])
    for i in range(number):
        first_part = choice(string.ascii_uppercase)
        second_part = ''.join(choice(string.ascii_lowercase) for j in range(5))
        third_part = randint(1, 50)
        
        city_buildings.add(first_part+second_part + ' ' + str(third_part))  
    
    return city_buildings

def generate_resource_under_building(buildings):
    
    resources = []

    for building in buildings:
        resource = {}
        resource['address'] = building
        resource['band'] = randint(3300, 4000)
        resource['latency'] = uniform(0, 0.5)
        
        nodes = []
        for j in range (5):
            node = {}
            node['ip'] = str (randint (10, 20)) + '.' + str(randint(20, 30)) + '.' + str (randint (30, 50)) + '.' + str(randint(50, 70))
            node['cpu_mips'] = randint (3300, 4000)
            node['memory_mb']= randint(3000, 6000)
            node['avg_wt'] = uniform(0,1)
            nodes.append(node)
        resource['resources'] = nodes
        resources.append(resource)
    return resources

def create_adjacency_list_buildings(buildings):
    
    graph_adjacency_list = {}
    
    for building in buildings:
        building_adjacency = set([])    
            
        for i in range(4):
            building_adjacency.add(choice(buildings))
                
        graph_adjacency_list[building] = building_adjacency
                
    return graph_adjacency_list



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

def generate_origin_iot(building):
    '''
    create static single resource properties
    '''
    #postal_code, address = generate_address()
    iot_device = {
        
        'block': building ,
        'ip': '10.10.11.11'
        }
    return iot_device

def generate_task_details():
    
    task_details = {
        'cpu_time_predicted_sc': uniform(1, 6),
        'cpu_mips_profiled_machine': randint(3300, 4000),
        'required_exe_time_sc': uniform(3, 5),
        'data_size_mb': randint(200, 400),
        'required_memory_mb': randint(2500, 4500)
            }
    return task_details

def save_blocks_db(blocks):
    
    db.create('address', 'band', 'latency', 'resources', mode="override")
    
    for block in blocks:
        db.insert(address=block.get('address'), band=block.get('band'),
                       latency=block.get('latency'), resources=block.get('resources'))


def find_band_latency_origin(origin_building):
    try:
        origin_block = db(address=origin_building)[0]
        return origin_block.get('band'), origin_block.get('latency')
    except IndexError:
        return None, None

def calculate_expected_exec_time(resource_avg_wt, resource_cpu_mips, avg_band, total_latency,task_details):
                
    avg_wt = Decimal(resource_avg_wt)
    cpu_time = Decimal((task_details.get('cpu_mips_profiled_machine')/ resource_cpu_mips)) * Decimal(task_details.get('cpu_time_predicted_sc'))
   
    dtt = Decimal(task_details.get('data_size_mb') / avg_band) + Decimal(Decimal((task_details.get('data_size_mb') / 64 ) )* Decimal(total_latency))
    
    total_ex_time = cpu_time + avg_wt + dtt            
        
    return total_ex_time

def find_available_computing_nodes(origin_band, origin_latency, bfs_result, task_details):
    
    total_computing_nodes = []
    origin_block = True

    for v in bfs_result:
        try:
            block = db(address=v)[0]
            resources = block.get('resources')
            
            avg_band = (origin_band + block.get('band')) /2
            total_latency = (origin_latency + block.get('latency'))
            
            if origin_block == True:
                total_latency = 0
                origin_block = False
            for resource in resources:
                expected_exe_time = calculate_expected_exec_time(resource.get('avg_wt'), resource.get('cpu_mips'), avg_band, total_latency,task_details )
                
                memory_mb = resource.get('memory_mb')
                
                if expected_exe_time <= task_details.get('required_exe_time_sc') and memory_mb >= task_details.get('required_memory_mb'):
                    
                    computing_node = {}
                    computing_node['address'] = v
                    computing_node['ip'] = resource.get('ip')
                    computing_node['expected_ex_time'] = expected_exe_time
                    computing_node['memory_mb'] = memory_mb
                    
                    total_computing_nodes.append(computing_node)
        except IndexError as IE:
            print (str(IE))
    return total_computing_nodes

# create buildings of the city    
buildings = generate_buildings(20)

# create city map from the buildings
city_map = create_adjacency_list_buildings(list(buildings))

# each block is a building with associated computing resources (edge nodes)
blocks = generate_resource_under_building(buildings)

# save blocks to db so that they can be queried later
save_blocks_db(blocks)

# Choice the orgin building where task will be generated
origin_building = choice(list(buildings))

# traverse the city map started from origin building
# traversing is based on bfs, specify level of traversing in bfs
bfs_result = bfs_traversal(city_map, origin_building, 3)
print (bfs_result)

#generate_origin_iot(origin_block)
origin_band, origin_latency = find_band_latency_origin(origin_building)


# check each node of the bfs result with the task details 
computing_nodes = find_available_computing_nodes(origin_band, origin_latency, bfs_result, generate_task_details())

print (computing_nodes)