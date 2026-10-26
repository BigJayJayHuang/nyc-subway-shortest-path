import csv
from collections import defaultdict
import heapq

def parse_subway_csv(file_path): #building out the graph, from station is the first node then to station is the next, time & wait for the edge, i added the 1 min possible wait time at every station included into the travel time to each node. I wanted to added it togehter to use one unit to represent the weight to measure the total travel time
    graph = defaultdict(list)
    
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            route_short_name = row['route_short_name']
            from_station = row['from_station']
            to_station = row['to_station']
            travel_time = float(row['average_travel_time_minutes'])
            wait_time = row['average_wait_time_minutes']
            if wait_time == '':
                wait_time = 0
            total_time = travel_time + float(wait_time)
            
            #check if the to_station already exists in the connections, the data contained the same stations names(multiple shared the same names, aka 79th st in bk and manhattan but same thing in tech perspective, and same 71st in bk and manhatan) this code is to have a singular, unique mapping. Made it one 79th to 71st. The problem is I dont know if its the 79th in bk or manhattan. Main point is i wanted to remove duplicates to ensure singular station but the main fundamental issue is that the stations shared the same name and we dont know which boroughs its using. Show one that works and dont work
            exists = False
            for connection in graph[from_station]:
                if connection[0] == to_station:
                    exists = True
                    break

            if not exists:
                graph[from_station].append((to_station, total_time, route_short_name))
                
    return graph

def Dijk_alg_bfs(graph, starting_station, destination_station):
    #initialize the priority queue with the starting station, the path taken, and the total travel time
    priority_queue = [(0, starting_station, [starting_station], [])] #the minimum is on the top, start with starting station
    shortest_times = {starting_station: 0} #keeping track of table
    visited = set() 
    
    while priority_queue:
        total_time, current_station, path, routes = heapq.heappop(priority_queue)
        
        #if we reach the destination station, return the path, total travel time, and routes
        if current_station == destination_station:
            return path, total_time, routes
        
        #mark the current station as visited
        if current_station not in visited:
            visited.add(current_station)
            
            #add all unvisited neighbors to the priority queue
            for neighbor, travel_time, route in graph[current_station]:
                new_total_time = total_time + travel_time
                if neighbor not in visited or new_total_time < shortest_times.get(neighbor, float('inf')): #or part is if the place is visted but theres a quicker time so it replaces the time and requeued with new unit
                    shortest_times[neighbor] = new_total_time
                    heapq.heappush(priority_queue, (new_total_time, neighbor, path + [neighbor], routes + [route])) #"path", we are adding the history
    
    #if no path is found, return None
    return None, None, None

file_path = 'final_subway_segments.csv'
#file_path = 'FINAL_SUBWAY_SEGMENTS_2.CSV'
#file_path = 'FINAL_SUBWAY_SEGMENTS_3.CSV'
subway_graph = parse_subway_csv(file_path)
starting_station = '96 St'
destination_station = 'Castle Hill Av'
path, total_time, routes = Dijk_alg_bfs(subway_graph, starting_station, destination_station)
if path:
    print(f"Path from {starting_station} to {destination_station}: {path} with total travel time: {total_time} minutes")
    print(f"Routes taken: {routes}")
else:
    print(f"No path found from {starting_station} to {destination_station}")