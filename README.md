# GTFS2GMNS

The General Transit Feed Specification [(GTFS)](https://gtfs.org/) defines a common format for public transportation schedules and associated geographic information. It is used by thousands of public transport providers. As a data conversion tool, gtfs2gmns, can directly convert the GTFS data to node, link, and agent files in the [GMNS](https://github.com/zephyr-data-specs/GMNS) format. 

In addition, this tool can merge the transit network into the road network which is obtain by Open Street Map via [OSM2GMNS](https://github.com/jiawei92/OSM2GMNS).

## Quick Start

### Download GTFS Data

On TransitFeed [homepage](https://transitfeeds.com/), users can browse and download official GTFS  feeds from around the world. Make sure that the following files are present, so that we can proceed.

* stop.txt
* route.txt
* trip.txt
* stop_times.txt

### Download OSM Data

On OpenStreetMap [homepage](https://www.openstreetmap.org/), click the `Export` button to enter Export mode. Before downloading, you may need to span and zoom in/out the map to make sure that your target area should cover the transit network area.

### Run Python Programming

1_gtfs2gmns.py

Convert GTFS Data to GMNS Format.

2_osm2gmns.py

Convert OSM Data to GMNS Format. In this tool, we only choose the `auto` network type. User can also obtain walk or bike mobility networks and the  detailed user guide about OSM2GMNS is [here](https://osm2gmns.readthedocs.io/en/latest/).

3_connector.py

Build the connector between the transit node and the road node.

4_trace2route.py 

Create the actual transit route through the shortest path [algorithm](https://github.com/jdlph/PATH4GMNS).

## Sample Networks

Users can visualize generated networks using [NeXTA](https://github.com/xzhou99/NeXTA-GMNS) or [QGIS](https://qgis.org/en/site/).

Oskaloosa Transit Network (red-transit node; black-transit network; brown-road network)

![Oskaloosa](https://github.com/xtHuang0927/GTFS2GMNS/blob/main/output/Oskaloosa/Oskaloosa.PNG)

Phoenix Transit Network (black-transit network)

![Oskaloosa](https://github.com/xtHuang0927/GTFS2GMNS/blob/main/output/Phoenix/Phoenix.PNG)

