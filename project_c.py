# -*- coding: utf-8 -*-
"""
Created on Tue Sep 30 15:24:16 2025

@author: Kai
"""


import math



class Plant:
    
    def __init__(self, name, symbol, size, preferred_ph, preferred_soil, sun_requirements):
        self.name = name
        self.symbol = symbol
        self.size = size
        self.preferred_ph = preferred_ph
        self.preferred_soil = preferred_soil
        self.sun_requirements = sun_requirements
    def __str__(self):
        return f'{self.symbol} ({self.size}x{self.size})'
        

class GardenRow:
    def __init__(self, max_length, max_width):
        self.plants = []
        self.max_length = max_length
        self.max_width = max_width
        self.current_length = 0
        self.current_width = 0
        self.finalised = False

    def can_add_plant(self, plant):
        if self.finalised:
            return False
        if self.current_length + plant.size > self.max_length:
            return False
        if plant.size > self.max_width:
            return False
        return True

    def add_plant(self, plant):
        if self.can_add_plant(plant):
            self.plants.append(plant)
            self.current_length += plant.size
            self.current_width = max(self.current_width, plant.size)
            return True
        return False

    def __str__(self):
        lines = []
        for i in range(1, self.current_width + 1):
            row_str = ""
            for plant in self.plants:
                if plant.size >= i:
                    row_str += plant.symbol * plant.size
                else:
                    row_str += " " * plant.size
            # pad to full width
            if len(row_str) < self.max_length:
                row_str += " " * (self.max_length - len(row_str))
            lines.append("|" + row_str + "|")
        return "\n".join(lines) + "\n"
                    
         
    
class GardenBed:
    
    
    def __init__(self, length, width, ph, soil_type, sun_amount):
        self.length = length
        self.width = width
        self.ph = ph
        self.soil_type = soil_type
        self.sun_amount = sun_amount
        self.rows_of_plants = [GardenRow(length, width)]
        self.id = None        
    
    
    def can_be_planted_here(self, plant):
        #checks sun requirements
        if self.sun_amount != plant.sun_requirements:
            return False
        #checks soil type requirements
        if len(self.soil_type.intersection(plant.preferred_soil)) == 0:
            return False
        #Checks if pH meets (within 1.5)
        if abs(self.ph - plant.preferred_ph) > 1.5:
            return False
        #Checks is there is room
        if not self.is_enough_room(plant):
            return False
       
        #if everything passes, then it can be planted
        return True

        
    def is_enough_room(self, plant):
        current_row = self.rows_of_plants[-1]
       
        #checks if the current row has room for plant
        if current_row.can_add_plant(plant):
            return True
        #calculates room used
        used = sum(row.current_width for row in self.rows_of_plants)
        remain = self.width - used
       
        #is plant size is less than remaining spae then True, else False
        return plant.size <= remain
    
    
    def add_plant(self, plant):
        if not self.can_be_planted_here(plant):
            return False

        current_row = self.rows_of_plants[-1]
       
        #if you added plant to row, then you have added it to garden bed
        if current_row.add_plant(plant):
            return True

        #sees if there is space horizontally, if not new row
        used_height = sum(row.current_width for row in self.rows_of_plants)
        remaining_height = self.width - used_height
       
        #no vertical space, nope plant is not added
        if plant.size > remaining_height:
            return False  

        #finalises current row
        current_row.finalised = True
        current_row.max_width = current_row.current_width
        new_row = GardenRow(self.length, remaining_height)
       
        #adds the plant to the row
        new_row.add_plant(plant)
        self.rows_of_plants.append(new_row)
       
        #if it has gotten here then the plant has been added to garden bed
        return True        
            

    def __str__(self):
        lines = []
        lines.append("+" + "-" * self.length + "+")
        for i, row in enumerate(self.rows_of_plants):
            #converts each row to string and removes empty lines
            row_lines = [line for line in str(row).split("\n") if line.strip() != ""]
            lines.extend(row_lines)
            if i < len(self.rows_of_plants) - 1:
                #adds separator if needed
                lines.append("|" + "." * self.length + "|")
        lines.append("+" + "-" * self.length + "+")
        return "\n".join(lines)    
    
class Garden:
    
    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.spots = [[None for i in range(length)] for j in range(width)]
        self.next_bed_id = 0
        self.beds = []        
        
        
    def add_bed(self, new_bed, x, y):
        if x < 0 or y < 0:
            return False
        if len(self.beds) >= 10:
            return False
        #checks if out of bounds
        if x + new_bed.length > self.length or y + new_bed.width > self.width:
            return False
        #checks if the location is empty for the bed (no overlap)
        for row in range(y, y + new_bed.width):
            for col in range(x, x + new_bed.length):
                if self.spots[row][col] is not None:
                    return False
        #assigns a id, makes the next id different
        new_bed.id = self.next_bed_id
        self.next_bed_id += 1
        #placing the bed down
        for row in range(y, y + new_bed.width):
            for col in range(x, x + new_bed.length):
                self.spots[row][col] = new_bed

        self.beds.append(new_bed)

        return True                

    def __str__(self):
        lines = []
        #top boundary
        lines.append("+" + "-" * self.length + "+")
       
        #iterates through each row
        for row in self.spots:
           
            #left boundary
            line = "|"
           
            #adds bed ID, or otherwise a space
            for spot in row:
                line += str(spot.id) if spot is not None else " "
            #right boundary
            line += "|"
           
            #adds completed row to lines list
            lines.append(line)
        #bottom boundary
        lines.append("+" + "-" * self.length + "+")
       
        #combine all lines into a single string to be returned
        return "\n".join(lines)
    
def print_menu():
    print("Please choose from one of the following options: ")
    print("(p)rint the entire garden")
    print("print a garden (b)ed")
    print("(a)dd a new garden bed")
    print("add a new p(l)ant")
    print("(q)uit the application")    
    return input()           
 
def add_new_plant(garden, bed_idx):
    name = input("Please enter the name of the plant: ")
    symbol = input("Please enter a symbol for the plant (only one character!): ")
    size = int(input("Please enter the size of the plant (an int): "))
    ph = float(input("Please enter the preferred pH of this plant (a number from 0 to 14): "))
    soil = input("Please enter the preferred soil types of this plant (one or more values, separated by commas): ")
    sun_req = input("Please enter the amount of sun this plant requires (a string): ")
    
    
    soil_set = {word.strip() for word in soil.split(",")}
    
    new_plant = Plant(name, symbol, size, ph, soil_set, sun_req)
    
    if (garden.beds[bed_idx].add_plant(new_plant)):
        print("Your plant has been added successfully")
    else:
        print("Sorry, the plant could not be added")
        
def add_new_bed(garden):
    if garden.next_bed_id >= 10:
        print("Sorry, the Garden is already full")
    else:
        l = int(input("Please enter the length of the garden bed: "))
        w = int(input("Please enter the width of the garden bed: "))
        ph = float(input("Please enter the pH of the soil in this garden bed (a number from 0 to 14): "))
        soil = input("Please enter the characteristics of the soil types in this garden bed (one or more values, separated by commas): ")
        sun_amt = input("Please enter the amount of sun this garden bed receives (a string): ")
        
        soil_set = {word.strip() for word in soil.split(",")}
        
        new_bed = GardenBed(l, w, ph, soil_set, sun_amt)
        
        x = int(input("Please enter the x coordinate of the top left corner of this garden bed: "))
        y = int(input("Please enter the y coordinate of the top left corner of this garden bed: "))
        
        if (garden.add_bed(new_bed, x, y)):
            print("Your garden bed has been added successfully")
        else:
            print("Sorry, the garden bed could not be added (probably too big or out of bounds)")

        
if __name__ == "__main__":
    
    print("Welcome to the Garden Planner")
    l = int(input("Please enter the length of the garden: "))
    w = int(input("Please enter the width of the garden: "))
    
    garden = Garden(l, w)
    
    print("OK, here's your garden")
    print(garden)
    
    choice = ""
    while choice != "q":
        
        choice = print_menu()
        
        if choice =="p":
            print(garden)
        elif choice == "b" or choice == "l":
            if garden.next_bed_id == 0:
                print("Sorry, there are no beds available.  Please add one")
                continue
            
            max_id = garden.next_bed_id
            print("Please choose from one of the following garden beds:")
            for i in range(max_id):
                print(i)
            which = int(input())
            if which not in range(max_id):
                print("Invalid choice")
                continue
            
            if choice == "b":
                print(garden.beds[which])
            
            elif choice == "l":
                add_new_plant(garden, which)
                
                    
        elif choice == "a":
            add_new_bed(garden)
