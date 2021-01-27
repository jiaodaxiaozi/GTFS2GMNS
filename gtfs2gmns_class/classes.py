import numpy as np
import pandas as pd
from functions import *

class Node:
    def __init__(self, node_type):
        self.name = None
        self.geometry = None
        self.x = None
        self.y = None
        self.node_type = node_type
        self.ctrl_type = None
        self.zone_id = None
        self.osm_highway=None
        self.node_type = node_type
        self.node_id = 0

    def build_Node(self, node_id, name, x, y, geometry, node_type, ctrl_type, osm_highway):
        self.node_type = node_type
        self.name = name
        self.geometry= geometry
        self.x = x
        self.y = y
        self.node_id = node_id
        self.ctrl_type = ctrl_type
        self.osm_highway = osm_highway


class Link():
    
    def __init__(self):
        self.link_id = 0
        self.link_name = ''
        self.link_type_name = ''
        self.link_type = ''
        self.from_node = None
        self.to_node = None
        self.lanes = None
        self.free_speed = None
        self.length = 0.0
        self.shortest_length = 0.0
        self.link_geometry = None
        self.capacity = None
        self.shortest_link_nodes = None
        

    
    def build_link(self, link_id, link_name, link_type, link_type_name, from_node, to_node, lanes, free_speed, length, link_geometry, capacity):
        self.link_id = link_id
        self.link_name = link_name
        self.link_type = link_type
        self.link_type_name = link_type_name
        self.from_node = from_node
        self.to_node = to_node
        self.lanes = lanes
        self.free_speed = free_speed
        self.length = length
        self.link_geometry = link_geometry
        self.capacity = capacity
                
        
class Network():
    def __init__(self):
        self.link_list_transit = None
        self.link_list_osm = None
        self.node_list_osm = None
        self.node_list_transit = None
        self.link_list_connector = None
    
    
    def build_node_list(self, node_type, data_input):
        node_list=[]

        if (node_type == 'transit'):
            
            for i in range(len(data_input)):
                N = Node(node_type)
                name = data_input['stop_id'].iloc[i]
                x = data_input['stop_lon'].iloc[i]
                y = data_input['stop_lat'].iloc[i]
                geometry = "POINT (" + x + " " +y +")"
                N.build_Node(i+100001, name, x, y, geometry, node_type, None, None)
                node_list.append(N)
            
            self.node_list_transit = node_list
                
        if (node_type == 'osm'):
            for i in range(len(data_input)):
                N = Node(node_type)
                node_id = data_input['node_id'].iloc[i]
                name = data_input['name'].iloc[i]
                x = data_input['x_coord'].iloc[i]
                y = data_input['y_coord'].iloc[i]
                geometry = "POINT (" + str(x) + " " +str(y) +")"
                ctrl_type = data_input['ctrl_type'].iloc[i]
                osm_highway = data_input['osm_highway'].iloc[i]
                N.build_Node(node_id, name, x, y, geometry, node_type, ctrl_type, osm_highway)
                node_list.append(N)
                
            self.node_list_osm = node_list
            
                
        
    def get_node_csv(self):

        node_csv_transit = pd.DataFrame()
        node_csv_osm = pd.DataFrame()
        
        if (self.node_list_osm != None):
            name = []
            x = []
            y = []
            node_type = []
            ctrl_type = []
            zone_id = []
            geometry = []
            node_id = []
            for i in range(len(self.node_list_osm)):
                
                N = self.node_list_osm[i]
                name.append(N.name)
                x.append(N.x)
                y.append(N.y)
                node_type.append(N.node_type)
                ctrl_type.append(N.ctrl_type)
                zone_id.append(N.zone_id)
                geometry.append(N.geometry)
                node_id.append(N.node_id)
    
            node_csv_osm['node_id'] = node_id
            node_csv_osm['name'] = name  
            node_csv_osm['x_coord'] = x
            node_csv_osm['y_coord'] = y
            node_csv_osm['node_type'] = node_type
            node_csv_osm['ctrl_type'] = ctrl_type
            node_csv_osm['zone_id'] = zone_id
            node_csv_osm['geometry'] = geometry
        
        if (self.node_list_transit != None):
            name = []
            x = []
            y = []
            node_type = []
            ctrl_type = []
            zone_id = []
            geometry = []
            node_id = []

            for i in range(len(self.node_list_transit)):
                
                N = self.node_list_transit[i]
                name.append(N.name)
                x.append(N.x)
                y.append(N.y)
                node_type.append(N.node_type)
                ctrl_type.append(N.ctrl_type)
                zone_id.append(N.zone_id)
                geometry.append(N.geometry)
                node_id.append(N.node_id)
    
            node_csv_transit['node_id'] = node_id
            node_csv_transit['name'] = name  
            node_csv_transit['x_coord'] = x
            node_csv_transit['y_coord'] = y
            node_csv_transit['node_type'] = node_type
            node_csv_transit['ctrl_type'] = ctrl_type
            node_csv_transit['zone_id'] = zone_id
            node_csv_transit['geometry'] = geometry

        node_csv = pd.concat([node_csv_transit, node_csv_osm])
        
        node_csv.to_csv('node.csv', index = False) 
        return node_csv, node_csv_osm, node_csv_transit
        
    
    def build_link_list(self, link_type, data_input):
        link_list_t = []
        link_list_o = []
        link_list_c = []


        if (link_type == 'transit'):

            for j in range(len(data_input)):
                link_name = data_input['name'].iloc[j]
                link_type = data_input['link_type'].iloc[j]
                from_node = data_input['from_node_id'].iloc[j]
                to_node = data_input['to_node_id'].iloc[j]
                lanes = data_input['lanes'].iloc[j]
                length = data_input['length'].iloc[j]
                link_geometry = data_input['geometry'].iloc[j]
                capacity = data_input['capacity'].iloc[j]
                free_speed = data_input['free_speed'].iloc[j]
                L = Link()
                L.build_link(j+100001, link_name, link_type, 'transit', from_node, to_node, lanes, free_speed, length, link_geometry, capacity )
                link_list_t.append(L)
                    
            self.link_list_transit = link_list_t

        if (link_type == 'osm'):
            for i in range(len(data_input)):
                link_id = data_input['link_id'].iloc[i]
                link_name = data_input['name'].iloc[i]
                link_type_name = data_input['link_type_name'].iloc[i]
                link_type = data_input['link_type'].iloc[i]
                from_node = data_input['from_node_id'].iloc[i]
                to_node = data_input['to_node_id'].iloc[i]
                lanes = data_input['lanes'].iloc[i]
                free_speed = data_input['free_speed'].iloc[i]
                length = data_input['length'].iloc[i]
                link_geometry = data_input['geometry'].iloc[i]
                capacity = data_input['capacity'].iloc[i]
                L = Link()
                L.build_link(link_id, link_name, link_type, link_type_name,from_node, to_node, lanes, free_speed, length, link_geometry, capacity )
                link_list_o.append(L)
                
            self.link_list_osm = link_list_o
            
            
        if (link_type == 'connector'):
            for k in range(len(data_input)):
                link_name = data_input['name'].iloc[k]
                link_type = data_input['link_type'].iloc[k]
                from_node = data_input['from_node_id'].iloc[k]
                to_node = data_input['to_node_id'].iloc[k]
                lanes = data_input['lanes'].iloc[k]
                free_speed = data_input['free_speed'].iloc[k]
                length = data_input['length'].iloc[k]
                link_geometry = data_input['geometry'].iloc[k]
                capacity = data_input['capacity'].iloc[k]
                L = Link()
                L.build_link(k+10000001, link_name, link_type, 'connector',from_node, to_node, lanes, free_speed, length, link_geometry, capacity )
                link_list_c.append(L)
                
            self.link_list_connector = link_list_c
       
    
    
    def get_shortest_path(self, N_origin, N_destination):
        
        origin = N_origin
        dest = N_destination
        transit_links = self.link_list_transit
        transit_nodes = self.node_list_transit
        osm_links = self.link_list_osm
        osm_nodes = self.node_list_osm
        connector_links = self.link_list_connector
        
        node_size = len(osm_nodes)
        node_size = len(transit_nodes)+node_size
        node_combine = transit_nodes + osm_nodes
        link_size = len(osm_links) + len(connector_links)
        link_combine = connector_links + osm_links
        link_length = []
        link_list = []
        node_list = []
        internal_node_seq_no_dict = {}
        external_node_id_dict = {}
        
        for i in range(node_size):
            node_list.append(node_combine[i].node_id)
                
        
        for i in range(link_size):
            link_list.append(link_combine[i].link_id)
            link_length.append(link_combine[i].length)
            
        external_node_id = node_list
        node_seq_no = 0
        
        for i in range(node_size):
            internal_node_seq_no_dict[external_node_id[i]] = node_seq_no
            external_node_id_dict[node_seq_no] = external_node_id[i]
            node_seq_no += 1
        
        from_node_no_array = []
        to_node_no_array = []
        for i in range(link_size):
            from_node_id = link_combine[i].from_node
            to_node_id = link_combine[i].to_node
            a = internal_node_seq_no_dict[from_node_id]
            from_node_no_array.append(a)
            b = internal_node_seq_no_dict[to_node_id]
            to_node_no_array.append(b)
        
        for link in transit_links:
            from_node_id = link.from_node
            to_node_id = link.to_node
            
        node_predecessor = np.full(node_size, -1, np.int32)
        link_predecessor = np.full(node_size, -1, np.int32)

        
        from_node_no_array = np.array(from_node_no_array, np.int32)
        to_node_no_array = np.array(to_node_no_array, np.int32)
        
        # initialize others as numpy arrays directly
        queue_next = np.full(node_size, 0, np.int32)
        first_link_from = np.full(node_size, -1, np.int32)
        last_link_from = np.full(node_size, -1, np.int32)
        sorted_link_no_array = np.full(link_size, -1,np.int32)
        
        # count the size of outgoing links for each node
        outgoing_link_size = [0] * node_size
        for link in range(len(link_list)):
            outgoing_link_size[from_node_no_array[link]] += 1
        
        cumulative_count = 0
        for i in range(node_size):
            first_link_from[i] = cumulative_count
            last_link_from[i] = (
                first_link_from[i] + outgoing_link_size[i]
            )
            cumulative_count += outgoing_link_size[i]
        
        # reset the counter # need to construct sorted_link_no_vector
        # we are converting a 2 dimensional dynamic array to a fixed size 
        # one-dimisonal array, with the link size 
        for i in range(node_size):
            outgoing_link_size[i] = 0
        
        # count again the current size of outgoing links for each node
        for j in range(len(link_list)):
            # fetch the curent from node seq no of this link
            from_node_seq_no = from_node_no_array[j]
            # j is the link sequence no in the original link block
            k = (first_link_from[from_node_seq_no] 
                 + outgoing_link_size[from_node_seq_no])
            sorted_link_no_array[k] = j
            # continue to count, increase by 1
            outgoing_link_size[from_node_no_array[j]] += 1
        
        # self._count += 1
        MAX_LABEL_COST = 10000
        link_cost = link_length
        link_cost_array = np.array(link_cost, np.float64)
        node_label_cost = np.full(node_size, MAX_LABEL_COST,np.float64)
        _cdll = get_dll_init()
        
        result = find_shortest_path(internal_node_seq_no_dict, origin, dest, node_size,
                                    from_node_no_array, to_node_no_array, first_link_from,last_link_from,
                                    sorted_link_no_array, 
                                    link_cost_array,
                                    node_label_cost,
                                    node_predecessor,
                                    link_predecessor,
                                    queue_next, origin, external_node_id_dict, _cdll, seq_type='node')

        Node_list_out = []

        for node_id in result:
            
            idx = node_list.index(node_id)
            N = node_combine[idx]
            Node_list_out.append(N)

        return result, Node_list_out
    
    
    def find_link_from_node(self, link_list, from_node, to_node):
        links = link_list
        active_link = None
        from_node_id = from_node.node_id
        to_node_id = to_node.node_id
        for link in links:
            from_id = link.from_node
            to_id = link.to_node
            if (from_id == from_node_id) and (to_id == to_node_id):
                active_link = link
                break
        if (active_link == None):
            print(' shortest link does not find...')
        
        return active_link
     
           
    def get_link_length(self, link_list):
        length = 0
        for link in link_list:
            length = float(link.length) + length
        
        return length
    
    
    def build_link_from_node_list(self, type_link_list, node_list):
        
        link_list=[]
        for i in range(len(node_list)-1):
            from_id= node_list[i]
            to_id= node_list[i+1]
            link = self.find_link_from_node(type_link_list, from_id, to_id)
            link_list.append(link)
        
        return link_list

    
    def link_list_transit_update(self):
          link_list = self.link_list_transit
          link_list_all = self.link_list_transit + self.link_list_osm + self.link_list_connector 
          
          for link in link_list:

              origin = link.from_node
              destination = link.to_node
             
              result, node_list = self.get_shortest_path(origin, destination)
              if(len(node_list) == 1):
                  continue
              
              link.shortest_link_nodes = node_list
              geometry = ''
              
              for node_id in node_list:

                  if (node_id == node_list[-1]):
                      geometry = geometry + str(node_id.x)+' '+str(node_id.y)
                  else:
                      geometry = geometry + str(node_id.x)+' '+str(node_id.y)+', '

              geometry = 'LINESTRING (' + geometry+ ')'
              link.link_geometry = geometry
              length_list = self.build_link_from_node_list(link_list_all, node_list)
              link.shortest_links = length_list
              length_new = self.get_link_length(length_list)
              link.length = length_new

    
    def get_link_csv(self):
        link_id = []
        name = []
        link_type_name = []
        link_type = []
        from_node = []
        to_node = []
        length = []
        link_geometry = []
        link_lanes = []
        capacity = []
        shortest_length = []
        free_speed = []
        link_list_all = self.link_list_transit + self.link_list_osm + self.link_list_connector 
        link_list_t = self.link_list_transit
        link_list_road = self.link_list_osm + self.link_list_connector 
        
        for link in link_list_all:

            link_id.append(link.link_id)
            name.append(link.link_name)
            link_type_name.append(link.link_type_name)
            link_type.append(link.link_type)
            from_node.append(link.from_node)
            to_node.append(link.to_node)
            length.append(link.length)
            link_geometry.append(link.link_geometry)
            link_lanes.append(link.lanes)
            capacity.append(link.capacity)
            shortest_length.append(link.shortest_length)
            free_speed.append(link.free_speed)
            
        link_csv = pd.DataFrame()
        link_csv['link_id'] = link_id
        link_csv['name'] = name
        link_csv['from_node'] = from_node
        link_csv['to_node'] = to_node
        link_csv['link_type_name'] = link_type_name
        link_csv['link_type'] = link_type
        link_csv['length'] = length
        link_csv['link_geometry'] = link_geometry
        link_csv['lanes'] = link_lanes
        link_csv['free_speed'] = free_speed
        link_csv['capacity'] = capacity 

        link_csv.to_csv('link.csv', index = False)   
        
        link_id = []
        name = []
        link_type_name=[]
        link_type=[]
        from_node=[]
        to_node=[]
        length=[]
        link_geometry=[]
        link_lanes=[]
        capacity = []
        shortest_length = []
        free_speed = []
        for link in link_list_t:

            link_id.append(link.link_id)
            name.append(link.link_name)
            link_type_name.append(link.link_type_name)
            link_type.append(link.link_type)
            from_node.append(link.from_node)
            to_node.append(link.to_node)
            length.append(link.length)
            link_geometry.append(link.link_geometry)
            link_lanes.append(link.lanes)
            capacity.append(link.capacity)
            shortest_length.append(link.shortest_length)
            free_speed.append(link.free_speed)
            
        link_csv_t = pd.DataFrame()
        link_csv_t['link_id'] = link_id
        link_csv_t['name'] = name
        link_csv_t['from_node'] = from_node
        link_csv_t['to_node'] = to_node
        link_csv_t['link_type_name'] = link_type_name
        link_csv_t['link_type'] = link_type
        link_csv_t['length'] = length
        link_csv_t['link_geometry'] = link_geometry
        link_csv_t['lanes'] = link_lanes
        link_csv_t['free_speed'] = free_speed
        link_csv_t['capacity'] = capacity
        # link_csv_t.to_csv('link_transit.csv', index = False)   
        
        
        link_id = []
        name = []
        link_type_name = []
        link_type = []
        from_node = []
        to_node = []
        length = []
        link_geometry = []
        link_lanes = []
        capacity = []
        shortest_length = []
        free_speed = []
        for link in link_list_road:

            link_id.append(link.link_id)
            name.append(link.link_name)
            link_type_name.append(link.link_type_name)
            link_type.append(link.link_type)
            from_node.append(link.from_node)
            to_node.append(link.to_node)
            length.append(link.length)
            link_geometry.append(link.link_geometry)
            link_lanes.append(link.lanes)
            capacity.append(link.capacity)
            shortest_length.append(link.shortest_length)
            free_speed.append(link.free_speed)
            
        link_csv_r = pd.DataFrame()
        link_csv_r['link_id'] = link_id
        link_csv_r['name'] = name
        link_csv_r['from_node'] = from_node
        link_csv_r['to_node'] = to_node
        link_csv_r['link_type_name'] = link_type_name
        link_csv_r['link_type'] = link_type
        link_csv_r['length'] = length
        link_csv_r['link_geometry'] = link_geometry
        link_csv_r['lanes'] = link_lanes
        link_csv_r['free_speed'] = free_speed
        link_csv_r['capacity'] = capacity
        
        # link_csv_r.to_csv('link_road.csv', index = False)   
        
        return link_csv, link_csv_t, link_csv_r
