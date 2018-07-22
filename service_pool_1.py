#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 17:15:16 2018

@author: shifu
"""

class ServicePool():
    
    def __init__(self, callback):
        self.callback = callback
        
    def accept_service(self, command, task_details, origin_block, algorithm, level, generation, mutation_factor):
        self.callback(command, task_details, origin_block, algorithm, level, generation, mutation_factor)
    