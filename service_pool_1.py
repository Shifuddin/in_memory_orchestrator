#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 17:15:16 2018

@author: shifu
"""

class ServicePool():
    
    def __init__(self, callback, callback2):
        self.callback = callback
        self.callback2 = callback2
    def accept_service(self, service_id, task_details, origin_block, algorithm, level, generation, mutation_factor, scheduling_policy):
        self.callback(service_id, task_details, origin_block, algorithm, level, generation, mutation_factor, scheduling_policy)
    
    def wait_for_finish(self):
        self.callback2()