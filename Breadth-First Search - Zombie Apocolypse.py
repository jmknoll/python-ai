"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
            
    def __str__(self):
        """
        Return multi-line string represenation for grid
        """
        zomb = "Zombies: "
        hums = "Humans: "
        zomb += str(self._zombie_list)
        hums += str(self._human_list)
        zomb += "\n"
        hums += "\n"
        return zomb + hums
    
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        self._zombie_list = []
        self._human_list = []
        poc_grid.Grid.clear(self)
        
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        #poc_grid.Grid.set_full(self, row, col)
        self._zombie_list.append((row,col))
        
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for item in self._zombie_list:
            yield item

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        #poc_grid.Grid.set_full(self, row, col)
        self._human_list.append((row,col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for item in self._human_list:
            yield item
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        #initialize visited as grid to track cells visited during search
        visited = [[EMPTY for dummy_col in range(self._grid_width)] 
                       for dummy_row in range(self._grid_height)] 
        
        maxval = self._grid_width * self._grid_height
        
        #call to self with inherited method get_width and get_height
        #distance_field = poc_grid.Grid(self._grid_width, self._grid_height)
        distance_field = [[maxval for dummy_col in range(self._grid_width)] 
                       for dummy_row in range(self._grid_height)]
        
        #make boundary a queue
        boundary = poc_queue.Queue()
        
        #set items for boundary according to entity type
        if entity_type == HUMAN:
            for human in self._human_list:
                boundary.enqueue(human)
        else:
            for zombie in self._zombie_list:
                boundary.enqueue(zombie)
        
        #populate grid with entities from boundary    
        for entity in boundary:
            distance_field[entity[0]][entity[1]] = 0
            visited[entity[0]][entity[1]] = FULL
         
        
        #loop to calculate all the distances - should look similar to wildfire
        #going to be repeating some code here - refactor later
        
            
        while len(boundary) != 0:
            cell = boundary.dequeue()
            neighbors = self.four_neighbors(cell[0], cell[1])
            for neighbor in neighbors:
                if self.is_empty(neighbor[0], neighbor[1]):
                    if visited[neighbor[0]][neighbor[1]] == 0:
                        visited[neighbor[0]][neighbor[1]] = 1
                        boundary.enqueue(neighbor)
                        distance_field[neighbor[0]][neighbor[1]] = distance_field[cell[0]][cell[1]] + 1
         
        return distance_field


    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
               
        #iterate over humans in human_list_clone
        new_human_list = []
        for human in self._human_list:
            
            #initialize dictionary of position coordinates and distance values
            coord_distance_dict = {}
            
            #add self to the dictionary as a key, with distance as a value
            coord_distance_dict[human] = zombie_distance[human[0]][human[1]] 
           
            
            #find eight neighbors
            neighbors = self.eight_neighbors(human[0],human[1])
            
            #neighbors is a list of tuples
            #iterate over neighbors and add tuple-coord/int-distance key/value pairs
            for neighbor in neighbors:
                #check to see if not already full
                if self.is_empty(neighbor[0], neighbor[1]):
                #if not, add to dictionary
                     coord_distance_dict[neighbor] = zombie_distance[neighbor[0]][neighbor[1]]
            
            #get key of highest value in dictionary
            
            #put all values in list
            distance_values = []
            
            for key, value in coord_distance_dict.items():
                distance_values.append(value)
            
            #take max of list
            maxdist = max(distance_values)
            
            
            for key, value in coord_distance_dict.items():
                if value == maxdist:
                    bestmove = key
                    #bestmove is a tuple
                
            #new list of humans
            
            new_human_list.append(bestmove)
            
        self._human_list = new_human_list
 
   
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        new_zombie_list = []
        for zombie in self._zombie_list:
            
            #initialize dictionary of position coordinates and distance values
            coord_distance_dict = {}
            
            #add self to the dictionary as a key, with distance as a value
            coord_distance_dict[zombie] = human_distance[zombie[0]][zombie[1]] 
           
            
            #find eight neighbors
            neighbors = self.four_neighbors(zombie[0],zombie[1])
            
            #neighbors is a list of tuples
            #iterate over neighbors and add tuple-coord/int-distance key/value pairs
            for neighbor in neighbors:
                #check to see if not already full
                if self.is_empty(neighbor[0], neighbor[1]):
                #if not, add to dictionary
                     coord_distance_dict[neighbor] = human_distance[neighbor[0]][neighbor[1]]
            
            #get key of highest value in dictionary
            
            #put all values in list
            distance_values = []
            
            for key, value in coord_distance_dict.items():
                distance_values.append(value)
            
            #take max of list
            mindist = min(distance_values)
            
            
            for key, value in coord_distance_dict.items():
                if value == mindist:
                    bestmove = key
                    #bestmove is a tuple
                
            #new list of humans
            
            new_zombie_list.append(bestmove)
            
        self._zombie_list = new_zombie_list
 
    
#TESTING

#disregard this code - it is just to help find problems in the code should they appear

#my_apoc = Zombie(6, 6)
#my_apoc.clear()
#my_apoc.add_zombie(5,5)
#my_apoc.add_zombie(4,4)
#print my_apoc.num_zombies()
#my_apoc.add_human(3,3)
#my_apoc.add_human(2,2)
#print my_apoc.num_humans()
#print my_apoc
#print my_apoc.compute_distance_field(ZOMBIE)
#zombie_distance = my_apoc.compute_distance_field(ZOMBIE)
#human_distance = my_apoc.compute_distance_field(HUMAN)
#my_apoc.move_humans(zombie_distance)
#my_apoc.move_humans(human_distance)


# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Zombie(30, 40))
