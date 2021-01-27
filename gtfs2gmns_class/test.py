# -*- coding: utf-8 -*-

import pandas as pd
from functions import *
from classes import *

stops = readtxt('../data/Oskaloosa/gtfs/stops')
routes = readtxt('../data/Oskaloosa/gtfs/routes')
trips = readtxt('../data/Oskaloosa/gtfs/trips')
stoptimes = readtxt('../data/Oskaloosa/gtfs/stop_times')


# osm_temp = get_osm()
osm = pd.read_csv('../data/Oskaloosa/osm/consolidated/node.csv')
G = Network()
G.build_node_list('osm', osm)
G.build_node_list('transit', stops)

node, node_osm, node_transit = G.get_node_csv()
print('nodes..')
link_csv_transit = get_transit_datalist(node_transit, routes, stoptimes, trips)


link_csv_osm = pd.read_csv('../data/Oskaloosa/osm/consolidated/link.csv', encoding='gbk')
link_csv_connect = get_connector_datalist(node_osm, node_transit)


G.build_link_list('transit', link_csv_transit)
print('transit link..')
G.build_link_list('osm', link_csv_osm)
print('osm link..')
G.build_link_list('connector', link_csv_connect)
print('connector link..')

l=len(G.node_list_transit)


G.link_list_transit_update()
final_link_csv = G.get_link_csv()
