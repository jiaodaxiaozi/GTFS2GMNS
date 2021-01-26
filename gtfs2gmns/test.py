import os

os.system('python ./1_gtfs2gmns.py')
# os.system('python ./2_osm2gmns.py') # if already obtain osm/gmns data, do not need this line
os.system('python ./3_connector.py')
os.system('python ./4_trace2route.py')

print('done')