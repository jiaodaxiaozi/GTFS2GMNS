import osm2gmns as og

net = og.getNetFromOSMFile('../data/Oskaloosa/osm/map.osm',network_type=('auto','walk','bike'), default_lanes=True, default_speed=True)
og.outputNetToCSV(net, output_folder='../data/Oskaloosa/osm')


net = og.getNetFromCSV('../data/Oskaloosa/osm')
og.consolidateComplexIntersections(net)
og.outputNetToCSV(net, output_folder='../data/Oskaloosa/osm/consolidated')