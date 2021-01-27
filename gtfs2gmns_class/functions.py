import datetime
import numpy as np
import pandas as pd
import math
import ctypes
from sys import platform
import os
# import osm2gmns as og


def get_osm(dirr='osm_road/map.osm', outdir='osm_results', outdir1='osm_results/consolidated'):
    net = og.getNetFromOSMFile(dirr, network_type=('auto'),default_lanes=True,default_speed=True)
    og.consolidateComplexIntersections(net)
    og.outputNetToCSV(net, output_folder=outdir)
    
    net = og.getNetFromCSV(outdir)
    og.consolidateComplexIntersections(net)
    og.outputNetToCSV(net, output_folder=outdir1)


#read files
def readtxt(filename):
    Filepath = filename +'.txt'
    data = []
    with open(Filepath, 'r') as f:
        for line in f.readlines():
            data.append(line.split('\n')[0].split(','))
    df_data = pd.DataFrame(data[1:], columns=data[0])
    return df_data

#distance
def LLs2Dist(lon1, lat1, lon2, lat2): #WGS84 transfer coordinate system to distance(mile) #xy
    R = 6371
    dLat = (float(lat2) - float(lat1)) * math.pi / 180.0
    dLon = (float(lon2) - float(lon1)) * math.pi / 180.0
    a = math.sin(float(dLat )/ 2) * math.sin(float(dLat)/2) + math.cos(float(lat1) * math.pi / 180.0) * math.cos(float(lat2) * math.pi / 180.0) * math.sin(float(dLon)/2) * math.sin(float(dLon)/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    dist = R * c 
    return dist

#time
def convert_time_sequence(time_sequence): #change format: 13:22:00 --> 1322:00
    time = []
    for i in np.unique(time_sequence):
        i=i.replace(':', '', 1)
        time.append(i)
    return time

def time_convert(input_time): #time format in GTFS is not standard, need convert: 25:00:00 --> 01:00:00
    hour = int(input_time[:-5])
    hour = hour%24
    output_time = str(hour)+input_time[-5:]
    return output_time

def time_calculate(time1,time2): #calculate the time delta
    time_a = datetime.datetime.strptime(time1, '%H%M:%S')
    time_b = datetime.datetime.strptime(time2, '%H%M:%S')
    flag = (time_b<time_a)
    active_time = (time_b-time_a).total_seconds()/60 + 1440*flag #min
    return active_time

def time(time1,time2): 
    time_a = time_convert(time1)
    time_b = time_convert(time2)
    delta = time_calculate(time_a,time_b)
    return delta



def get_transit_datalist(node_csv, df_routes, df_stoptimes, df_trips):
    
    node_csv = node_csv.rename(columns={'name':'stop_id'})
    combined_route = df_trips.merge(df_routes,on='route_id',how='left')
    combined_stop = df_stoptimes.merge(node_csv,on='stop_id',how='left' )
    combined_trip = combined_stop.merge(df_trips,on='trip_id',how='left')
    dataList_route = {}
    gp = combined_route.groupby('trip_id')
    for key, form in gp:
        dataList_route[key] = {
            'route_id': form['route_id'].values[0],
            'route_id_short_name': form['route_long_name'].values[0]
            }
        
    dataList_trip = {}
    gp = combined_trip.groupby('trip_id')
    
    for key, form in gp:
        temp = form['arrival_time']
        temp = convert_time_sequence(temp)
        dataList_trip[key] = {
            'route_id': form['route_id'].values[0],
            'from_node_id': form['node_id'].values[0],
            'to_node_id': form['node_id'].values[-1],
            'node_sequence': form['node_id'].tolist(),
            'time_sequence': temp
            }
        link_list = []
        node_x = node_csv['x_coord'].tolist()
        node_y = node_csv['y_coord'].tolist()
        node_id_list = node_csv['node_id'].tolist()
        
    for key in dataList_trip.keys(): 

        active_node_sequence_size = len(dataList_trip[key]['node_sequence'])
        for i in range(active_node_sequence_size-1):
            route_index = dataList_trip[key]['route_id']
            active_from_node_id = dataList_trip[key]['node_sequence'][i]
            active_to_node_id = dataList_trip[key]['node_sequence'][i+1]
            active_from_node_idx = node_id_list.index(active_from_node_id)
            active_to_node_idx = node_id_list.index(active_to_node_id)
            
            from_node_id_x = node_x[active_from_node_idx] ###
            from_node_id_y = node_y[active_from_node_idx]
            to_node_id_x = node_x[active_to_node_idx]
            to_node_id_y = node_y[active_to_node_idx]
            
            active_distance = LLs2Dist(from_node_id_x,from_node_id_y,to_node_id_x,to_node_id_y)
            active_geometry = 'LINESTRING (' + str(from_node_id_x)+' '+str(from_node_id_y)+', '+str(to_node_id_x)+' '+str(to_node_id_y)+')'
            
            link_list.append([route_index,active_from_node_id,active_to_node_id,active_distance,active_geometry])
    link_csv = pd.DataFrame(link_list, columns=['name','from_node_id','to_node_id','length','geometry']).drop_duplicates()   
    link_csv['link_type'] = 99
    link_csv['lanes'] = 1
    link_csv['free_speed'] = 60
    link_csv['capacity'] = 100
        
    return link_csv


def createConnector(dataList, from_node_id, to_node_id):
    link = []
    from_node_id_x = dataList[from_node_id]['x_coord']
    from_node_id_y = dataList[from_node_id]['y_coord']
    to_node_id_x = dataList[to_node_id]['x_coord']
    to_node_id_y = dataList[to_node_id]['y_coord']
    length = LLs2Dist(from_node_id_x,from_node_id_y,to_node_id_x,to_node_id_y)
    geometry = 'LINESTRING (' + str(from_node_id_x)+' '+str(from_node_id_y)+', '+str(to_node_id_x)+' '+str(to_node_id_y)+')'
        
    link = [from_node_id,to_node_id,length,geometry]
    return link


def get_connector_datalist(road_node, bus_node):
    combined = pd.concat([bus_node,road_node],axis=0)
    dataList_stop = {}
    gp = bus_node.groupby('node_id')
    for key, form in gp:
        dataList_stop[key] = {
            'x_coord': form['x_coord'].values[0],
            'y_coord': form['y_coord'].values[0]
            }
    
    dataList_node = {}
    gp = road_node.groupby('node_id')
    for key, form in gp:
        dataList_node[key] = {
            'x_coord': form['x_coord'].values[0],
            'y_coord': form['y_coord'].values[0]
            }
    
    dataList = {}
    gp = combined.groupby('node_id')
    for key, form in gp:
        dataList[key] = {
            'x_coord': form['x_coord'].values[0],
            'y_coord': form['y_coord'].values[0]
            }
    
    
    coord_list = []
    for key in dataList_node.keys(): 
        coord_list.append((dataList_node[key]['x_coord'],dataList_node[key]['y_coord']))
    
    coord_array = np.array(coord_list)
    coord_array = coord_array.astype(np.float)
    link_list = []
    
    
    for key in dataList_stop.keys(): 
        
        coord = np.array((dataList_stop[key]['x_coord'],dataList_stop[key]['y_coord']))
        coord = coord.astype(np.float)
        coord_diff = coord_array - coord
        coord_diff_square = np.power(coord_diff,2)
        coord_diff_sum_square = coord_diff_square.sum(axis=1)
        distance = np.sqrt(coord_diff_sum_square)
        idx = np.argmin(distance)
        active_node = road_node['node_id'].iloc[idx]
        active_link1 = createConnector(dataList, active_node, key)
        active_link2= createConnector(dataList, key, active_node)
        link_list.append(active_link1)
        link_list.append(active_link2)
    
    connector_csv = pd.DataFrame()
    connector_csv = pd.DataFrame(link_list, columns=['from_node_id','to_node_id','length','geometry']).drop_duplicates()    
    
    connector_csv['osm_way_id'] = None
    connector_csv['name'] = None
    connector_csv['facility_type'] = None
    connector_csv['link_type'] = 20
    connector_csv['link_type_name'] = 'connector'
    connector_csv['lanes'] = 1
    connector_csv['free_speed'] = 29
    connector_csv['capacity'] = None
    connector_csv['allowed_uses'] = 'auto'
    connector_csv['from_biway'] = 1
    
    return connector_csv
        
    
    
def get_dll_init():
    _pkg_path = os.path.abspath(__file__)

    if platform.startswith('win32'):
        _dll_file = os.path.join(os.path.dirname(_pkg_path), './bin/path_engine.dll')
    elif platform.startswith('linux'):
        _dll_file = os.path.join(os.path.dirname(_pkg_path), './bin/path_engine.so')
    elif platform.startswith('darwin'):
        _dll_file = os.path.join(os.path.dirname(_pkg_path), './bin/path_engine.dylib')
    else:
        raise Exception('Please build the shared library compatible to your OS\
                        using source files in engine_cpp!')
    
    _cdll = ctypes.cdll.LoadLibrary(_dll_file)
    
    # set up the argument types for the shortest path function in dll.
    _cdll.shortest_path.argtypes = [
        ctypes.c_int, 
        ctypes.c_int, 
        np.ctypeslib.ndpointer(dtype=np.int32),
        np.ctypeslib.ndpointer(dtype=np.int32),
        np.ctypeslib.ndpointer(dtype=np.int32),
        np.ctypeslib.ndpointer(dtype=np.int32),
        np.ctypeslib.ndpointer(dtype=np.int32), 
        np.ctypeslib.ndpointer(dtype=np.float64),   
        np.ctypeslib.ndpointer(dtype=np.float64),                                    
        np.ctypeslib.ndpointer(dtype=np.int32),
        np.ctypeslib.ndpointer(dtype=np.int32),
        np.ctypeslib.ndpointer(dtype=np.int32),
    ]
    return _cdll



def _optimal_label_correcting_CAPI(node_size,
                        from_node_no_array,
                        to_node_no_array,
                        first_link_from,
                        last_link_from,
                        sorted_link_no_array, 
                        link_cost_array,
                        node_label_cost,
                        node_predecessor,
                        link_predecessor,
                        queue_next, origin_node_id, _cdll, internal_node_seq_no_dict):
    """ input : origin_node,destination_node,departure_time
        output : the shortest path
    """
    
    origin_node_no = internal_node_seq_no_dict[origin_node_id]
            
    _cdll.shortest_path(origin_node_no,
                        node_size,
                        from_node_no_array,
                        to_node_no_array,
                        first_link_from,
                        last_link_from,
                        sorted_link_no_array, 
                        link_cost_array,
                        node_label_cost,
                        node_predecessor,
                        link_predecessor,
                        queue_next)


def single_source_shortest_path(node_size,
                        from_node_no_array,
                        to_node_no_array,
                        first_link_from,
                        last_link_from,
                        sorted_link_no_array, 
                        link_cost_array,
                        node_label_cost,
                        node_predecessor,
                        link_predecessor,
                        queue_next, origin_node_id, _cdll, internal_node_seq_no_dict):

    _optimal_label_correcting_CAPI(node_size,
                        from_node_no_array,
                        to_node_no_array,
                        first_link_from,
                        last_link_from,
                        sorted_link_no_array, 
                        link_cost_array,
                        node_label_cost,
                        node_predecessor,
                        link_predecessor,
                        queue_next, origin_node_id, _cdll, internal_node_seq_no_dict)
    

def output_path_sequence(internal_node_seq_no_dict, node_predecessor, external_node_id_dict, link_predecessor, from_node_id, to_node_id):
    """ output shortest path in terms of node sequence or link sequence
    
    Note that this function returns GENERATOR rather than list.
    """
    path = []
    current_node_seq_no = internal_node_seq_no_dict[to_node_id]

    while current_node_seq_no >= 0:  
        path.append(current_node_seq_no)
        current_node_seq_no = node_predecessor[current_node_seq_no]
        # reverse the sequence
    for node_seq_no in reversed(path):
        yield external_node_id_dict[node_seq_no]



def find_shortest_path(internal_node_seq_no_dict, from_node_id, to_node_id, node_size, from_node_no_array, to_node_no_array, first_link_from,last_link_from,
                        sorted_link_no_array, 
                        link_cost_array,
                        node_label_cost,
                        node_predecessor,
                        link_predecessor,
                        queue_next, origin_node_id, external_node_id_dict,_cdll , seq_type='node'):
    if from_node_id not in internal_node_seq_no_dict.keys():
        raise Exception(f"Node ID: {from_node_id} not in the network")
    if to_node_id not in internal_node_seq_no_dict.keys():
        raise Exception(f"Node ID: {to_node_id} not in the network")

    single_source_shortest_path(node_size,
                        from_node_no_array,
                        to_node_no_array,
                        first_link_from,
                        last_link_from,
                        sorted_link_no_array, 
                        link_cost_array,
                        node_label_cost,
                        node_predecessor,
                        link_predecessor,
                        queue_next, origin_node_id, _cdll, internal_node_seq_no_dict)

    return list(output_path_sequence(internal_node_seq_no_dict, node_predecessor, external_node_id_dict, link_predecessor, from_node_id, to_node_id))
