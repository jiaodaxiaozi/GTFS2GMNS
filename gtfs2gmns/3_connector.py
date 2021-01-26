import math
import numpy as np
import pandas as pd

# WGS84 transfer coordinate system to distance: meter
def LLs2Dist(lon1, lat1, lon2, lat2):
    R = 6371
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0
    a = math.sin(dLat / 2) * math.sin(dLat/2) + math.cos(lat1 * math.pi / 180.0) * math.cos(lat2 * math.pi / 180.0) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    dist = R * c
    return dist


def createConnector(from_node_id, to_node_id):
    link = []
    from_node_id_x = dataList[from_node_id]['x_coord']
    from_node_id_y = dataList[from_node_id]['y_coord']
    to_node_id_x = dataList[to_node_id]['x_coord']
    to_node_id_y = dataList[to_node_id]['y_coord']
    length = LLs2Dist(from_node_id_x,from_node_id_y,to_node_id_x,to_node_id_y)
    geometry = 'LINESTRING (' + str(from_node_id_x)+' '+str(from_node_id_y)+', '+str(to_node_id_x)+' '+str(to_node_id_y)+')'
        
    link = [from_node_id,to_node_id,length,geometry]
    return link

print('reading gmns data...')
node_transit = pd.read_csv('../output/Oskaloosa/node_transit.csv') # transit node
node_road = pd.read_csv('../data/Oskaloosa/osm/consolidated/node.csv', encoding='gbk')

node_combine = pd.DataFrame()
node_combine['node_id']= node_road['node_id'].tolist() + node_transit['node_id'].tolist()
node_combine['name']= node_road['name'].tolist() + node_transit['name'].tolist()
node_combine['x_coord']= node_road['x_coord'].tolist() + node_transit['x_coord'].tolist()
node_combine['y_coord'] = node_road['y_coord'].tolist() + node_transit['y_coord'].tolist()
node_combine['node_type']= node_road['node_type'].tolist() + node_transit['node_type'].tolist()
node_combine['zone_id']= node_road['zone_id'].tolist() + node_transit['zone_id'].tolist()

node_combine.to_csv('../output/Oskaloosa/node.csv', index=False)

link_road = pd.read_csv('../data/Oskaloosa/osm/consolidated/link.csv', encoding='gbk')
link_road = link_road.drop(['link_id', 'osm_way_id', 'allowed_uses', 'from_biway'], axis=1)

dataList_stop = {}
gp = node_transit.groupby('node_id')
for key, form in gp:
    dataList_stop[key] = {
        'x_coord': form['x_coord'].values[0],
        'y_coord': form['y_coord'].values[0]
        }

dataList_node = {}
gp = node_road.groupby('node_id')
for key, form in gp:
    dataList_node[key] = {
        'x_coord': form['x_coord'].values[0],
        'y_coord': form['y_coord'].values[0]
        }

dataList = {}
gp = node_combine.groupby('node_id')
for key, form in gp:
    dataList[key] = {
        'x_coord': form['x_coord'].values[0],
        'y_coord': form['y_coord'].values[0]
        }


coord_list = []
for key in dataList_node.keys(): 
    a = dataList_node[key]['x_coord']
    b = dataList_node[key]['y_coord']
    coord_list.append((dataList_node[key]['x_coord'],dataList_node[key]['y_coord']))
coord_array = np.array(coord_list)


print('building connector...')
link_list = []

for key in dataList_stop.keys(): 
    coord = np.array((dataList_stop[key]['x_coord'],dataList_stop[key]['y_coord']))
    coord_diff = coord_array - coord
    coord_diff_square = np.power(coord_diff,2)
    coord_diff_sum_square = coord_diff_square.sum(axis=1)
    distance = np.sqrt(coord_diff_sum_square)
    idx = np.argmin(distance)
    active_node = node_road['node_id'].iloc[idx]
    active_link1 = createConnector(active_node, key)
    active_link2= createConnector(key, active_node)
    link_list.append(active_link1)
    link_list.append(active_link2)


connector_csv = pd.DataFrame()
connector_csv = pd.DataFrame(link_list, columns=['from_node_id','to_node_id','length','geometry']).drop_duplicates()    


connector_csv['name'] = None
connector_csv['link_type'] = 20
connector_csv['link_type_name'] = 'connector'
connector_csv['dir_flag'] = 1
connector_csv['lanes'] = 1
connector_csv['free_speed'] = 29
connector_csv['capacity'] = None
    

combined_link = pd.concat([link_road,connector_csv], axis=0, ignore_index=True)

combined_link.index.name = 'link_id'
combined_link.index += 1

combined_link.to_csv('../output/Oskaloosa/link_osm_connector.csv')
