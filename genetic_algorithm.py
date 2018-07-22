#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 16:22:44 2018

@author: shifu
"""
from random import shuffle, randint, uniform, choice
from math import ceil
from decimal import Decimal
class GeneticAlgorithm():
    def __init__(self, region_sp):
        self.region_sp = region_sp
        print ('Genetic created')
        
    def calculate_expected_exec_time(self, resource_avg_wt, resource_cpu_mips, avg_band, total_latency):
                
        avg_wt = Decimal(resource_avg_wt)
        cpu_time = Decimal((self.task_details.get('cpu_mips_profiled_machine')/ resource_cpu_mips)) * Decimal(self.task_details.get('cpu_time_predicted_sc'))
       
        dtt = Decimal(self.task_details.get('data_size_mb') / avg_band) + Decimal(Decimal((self.task_details.get('data_size_mb') / 64 ) )* Decimal(total_latency))
        
        total_ex_time = cpu_time + avg_wt + dtt            
            
        return total_ex_time
    
    def create_initial_population(self, origin_band, origin_latency):
        
        origin_address = self.bfs_result.pop(0)
        init_population_length =  ceil(len(self.bfs_result)/3)
        shuffle(self.bfs_result)
        init_population = []
        
        origin_block = self.region_sp.get_block(origin_address)
        
        chromosome = []
        for resource in origin_block.get('resources'):
            expected_exe_time = self.calculate_expected_exec_time(resource.get('avg_wt'), resource.get('cpu_mips'), origin_band, 0)
            dna = {}
            dna['address'] = origin_block.get('address')
            dna['ip'] = resource.get('ip')
            dna['expected_ex_time'] = expected_exe_time
            dna['avail_mem_mb'] = resource.get('memory_mb')
            chromosome.append(dna)
        init_population.append(chromosome)
        
        while True:
            if init_population_length == 0:
                break
            chromosome = []
            # get block info from db
            block = self.region_sp.get_block(self.bfs_result.pop(0))
            
            # resources of the block
            resources = block.get('resources')
            
            # calculate avg_band and total latency between two blocks 
            avg_band = (origin_band + block.get('band')) /2
            total_latency = (origin_latency + block.get('latency'))
            
            for resource in resources:
                expected_exe_time = self.calculate_expected_exec_time(resource.get('avg_wt'), resource.get('cpu_mips'), avg_band, total_latency )
                dna = {}
                dna['address'] = block.get('address')
                dna['ip'] = resource.get('ip')
                dna['expected_ex_time'] = expected_exe_time
                dna['avail_mem_mb'] = resource.get('memory_mb')
                chromosome.append(dna)
            init_population.append(chromosome)    
            init_population_length -= 1
        return init_population
    
    
    def change_dna(self, child, origin_band, origin_latency):
        '''
        Get a random dna from the total population
        :param child: Chrosomoe where change will be applied
        
        Algorithm:
            1. Choice a random dna from total population
            2. Check whether this dna not in the child already
            3. If yes, return new dna
            4. If no, repeat 1 to 3 unlimited times
        '''
        
        random_address = choice(self.bfs_result)
        random_block = self.region_sp.get_block(random_address)
        random_resource = choice(random_block.get('resources'))
        avg_band = (origin_band + random_block.get('band')) /2
        total_latency = (origin_latency + random_block.get('latency'))
        expected_exe_time = self.calculate_expected_exec_time(random_resource.get('avg_wt'), random_resource.get('cpu_mips'), avg_band, total_latency )
        random_dna = {}
        random_dna['address'] = random_address
        random_dna['ip'] = random_resource.get('ip')
        random_dna['expected_ex_time'] = expected_exe_time
        random_dna['avail_mem_mb'] = random_resource.get('memory_mb')
            
        return random_dna
    def perform_mutation (self,child, mutation_factor, origin_band, origin_latency):
        '''
        Change dna in a chromosome 
        :param child: A chromosome 
        :param mutation_factor: Possibility of change
        
        Algorithm:
            1. Generate random uniform number from 0 to 1
            2. Check wheter random is smaller than mutation factor
            3. If yes, change current dna with another newly generated dna
            4. Repeat step 1 to 3 for all dna in a given chromosome
            
        :return child: changed chrosome 
        '''
        for i in range(len(child)):
            RU = uniform(0,1)
            
            if (RU < mutation_factor):
                new_dna = self.change_dna(child, origin_band, origin_latency)
                child [i] = new_dna
                
        return child
    def perform_crossover(self,chromosome_1, chromose_2):
        '''
        Create a new chromosome from two old chromosomes
        :param chromosome_1: First Parent
        :param chromose_2: Second Parent
        
        Algorithm:
            1. Generate a random mid point between 1 to chromosome size
            2. Join first parent's 0 to midpoint-1 dnas and second parent's midpoint - end dnas
            3. Return newly created child
        
        :return child: crossover product from parents
        '''
        mid_point = randint(1, len(chromosome_1))
        child = chromosome_1[0:mid_point] + chromose_2[mid_point:] 
    
        return child
    def calculate_pool_occurance(self,chromosome_fitness_score, total_popu_fitness):
        '''
        Calculate how many times a chromosome will in the mating pool
        :param chromosome_fitness_score: How many dnas of that chromosome satisfies objective 
        functions.
        :param total_popu_fitness: sum of all the chromosome's score in current generation
        
        Algorithm:
            1. Divide chromosome_fitness_score by total population fitness 
            2. Multiply the ration by 100 to the percentage
        
        :return occurance: percent value
        '''
        occurance = 0
        if total_popu_fitness > 0:
            ratio = chromosome_fitness_score/ total_popu_fitness
            occurance = ceil((ratio*100))
        return occurance    
    
    def calc_chromosome_fitness(self, chromosome):
        chromose_score = 0
        for dna in chromosome:
            if dna.get('expected_ex_time') <= self.task_details.get('required_exe_time_sc') and dna.get('avail_mem_mb') >= self.task_details.get('required_memory_mb'):
                chromose_score += 1
        return chromose_score
    
    def calculate_population_fitness(self, population):
        population_fitness_score = []
        for chromosome in population:
            chromosome_fitness_score = self.calc_chromosome_fitness(chromosome)
            population_fitness_score.append(chromosome_fitness_score)
        return population_fitness_score
    def calculate_fitness_mating_pool(self, population):
        population_fitness = self.calculate_population_fitness(population)
        
        sum_score = sum(population_fitness)
        
            
        mating_pool = []    

        for i in range(len(population_fitness)):
            chr_occurance = self.calculate_pool_occurance(population_fitness[i], sum_score)
            for _ in range (1, chr_occurance+1):
                mating_pool.append(i)
        return mating_pool

    def get_matching_node(self, bfs_result, origin_band, origin_latency, task_details, generation, mutation_factor):
        
        
        self.task_details = task_details
        self.bfs_result = bfs_result
        current_population = self.create_initial_population(origin_band, origin_latency)
        
        current_generation = 0
        

        while current_generation < generation:
            mating_pool = self.calculate_fitness_mating_pool(current_population)
            
            if len(mating_pool) == 0:
                print ('Algorithm terminated.')
                break
            
            new_population = []
            
            for _ in range(len(current_population)):
                best_chr_1 = current_population[ choice(mating_pool)]
                best_chr_2 = current_population[ choice(mating_pool)]
                
                plain_child = self.perform_crossover(best_chr_1, best_chr_2) 
                mutated_child = self.perform_mutation(plain_child, mutation_factor, origin_band, origin_latency)
                new_population.append(mutated_child)
                    
            current_population = new_population
            current_generation +=1
            mutation_factor -= 0.00005
        '''
        for i in range (0, len(fitness)):
            for j in range(0, len(fitness[i])):
                if fitness[i][j] == 1:
                    matched_nodes.add(current_population[i][j]) 
        print (matched_nodes)
        '''
        matche_nodes = {}
        for chromose in current_population:
            for dna in chromose:
                if dna.get('expected_ex_time') <= task_details.get('required_exe_time_sc') and dna.get('avail_mem_mb') >= task_details.get('required_memory_mb'):
                    matche_nodes[dna.get('address') + ', ' +dna.get('ip')] = dna.get('expected_ex_time') 
                    
        print (matche_nodes)