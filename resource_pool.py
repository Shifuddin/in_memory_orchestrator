# -*- coding: utf-8 -*-
"""
Spyder Editor

Resource pool accepts new resource at startup time
It accepts new resource at runtime
It also accepts resource for update
"""

class ResourcePool():
    
    def __init__(self, add_callback, update_callback):
        self.add_callback = add_callback
        self.update_callback = update_callback
        
    def accept_resource(self, resource):
        '''
        accept a new resource
        @param resource: propertifes of fog node as dict 
        '''
        self.add_callback([resource])
    
    def accept_bulk_resources(self, resources):
        '''
        accept a list of resources
        @param resources: list of properties of fog nodes.
        '''
        self.add_callback(resources)
    def update_bulk_resources(self, resources):
        self.update_callback(resources)
        
    