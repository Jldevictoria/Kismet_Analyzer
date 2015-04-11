#!/usr/bin/python
# Joseph DeVictoria - ECEN 490 - April 2015
# This script will take in a kismet .gpsxml file and spit out heatmap data.

import sys, simplekml

# Packet class used to hold all the information of individual kismet packets.
class Packet(object):
    bssid = 0
    source = 0
    time_sec = 0
    time_usec = 0
    lat = 0
    lon = 0
    spd = 0
    heading = 0
    fix = 0
    alt = 0
    signal_dbm = 0
    noise_dbm = 0
    def __str__(self):
        dataprint =  "bssid: " + str(self.bssid) + " "
        dataprint += "source: " + str(self.source) + " "
        dataprint += "time-sec: " + str(self.time_sec) + " "
        dataprint += "time-usec: " + str(self.time_usec) + " "
        dataprint += "lat: " + str(self.lat) + " "
        dataprint += "lon: " + str(self.lon) + " "
        dataprint += "spd: " + str(self.spd) + " "
        dataprint += "heading: " + str(self.heading) + " "
        dataprint += "fix: " + str(self.fix) + " "
        dataprint += "alt: " + str(self.alt) + " "
        dataprint += "signal-dbm: " + str(self.signal_dbm) + " "
        dataprint += "noise_dbm: " + str(self.noise_dbm) + " "
        return dataprint

# Router class that stores important location information for each bssid.
class Router(object):
    bssid = 0
    packet_count = 0
    lat_ave = 0 
    lon_ave = 0
    alt_ave = 0
    signal_dbm_ave = 0
    noise_dbm_ave = 0
    def __str__(self):
        dataprint =  "bssid: " + str(self.bssid) + "\n"
        dataprint += "packet_count: " + str(self.packet_count) + "\n"
        dataprint += "lat_ave: " + str(self.lat_ave) + "\n"
        dataprint += "lon_ave: " + str(self.lon_ave) + "\n"
        dataprint += "alt_ave: " + str(self.alt_ave) + "\n"
        dataprint += "signal_dbm_ave: " + str(self.signal_dbm_ave) + "\n"
        dataprint += "noise_dbm_ave: " + str(self.noise_dbm_ave) + "\n"
        return dataprint

# Intoductory information.
print "---------------------------------------------"
print "- Kismet Data Analyzer."
print "- Analyzing file: " + str(sys.argv[1])
print "---------------------------------------------"

# Read in data from input file into an array of packets.
data = open(str(sys.argv[1]), 'r')
packets = []
for line in data:
    sublines = line.split()
    pack = Packet()
    for chunk in sublines:
        valuepair = chunk.split('=')
        if len(valuepair) > 1:
            if valuepair[0] == 'bssid':
                pack.bssid = \
                valuepair[1].replace("\"", "").replace("/>", "")
            if valuepair[0] == 'source':
                pack.source = \
                valuepair[1].replace("\"", "").replace("/>", "")
            if valuepair[0] == 'time-sec':
                pack.time_sec = \
                valuepair[1].replace("\"", "").replace("/>", "")
            if valuepair[0] == 'time-usec':
                pack.time_usec = \
                valuepair[1].replace("\"", "").replace("/>", "")
            if valuepair[0] == 'lat':
                pack.lat = \
                float(valuepair[1].replace("\"", "").replace("/>", ""))
            if valuepair[0] == 'lon':
                pack.lon = \
                float(valuepair[1].replace("\"", "").replace("/>", ""))
            if valuepair[0] == 'spd':
                pack.spd = \
                float(valuepair[1].replace("\"", "").replace("/>", ""))
            if valuepair[0] == 'heading':
                pack.heading = \
                float(valuepair[1].replace("\"", "").replace("/>", ""))
            if valuepair[0] == 'fix':
                pack.fix = \
                float(valuepair[1].replace("\"", "").replace("/>", ""))
            if valuepair[0] == 'alt':
                pack.alt = \
                float(valuepair[1].replace("\"", "").replace("/>", ""))
            if valuepair[0] == 'signal_dbm':
                pack.signal_dbm = \
                int(valuepair[1].replace("\"", "").replace("/>", ""))
            if valuepair[0] == 'noise_dbm':
                pack.noise_dbm = \
                int(valuepair[1].replace("\"", "").replace("/>", ""))
    packets.append(pack)

# Separate packets by source
known_bssids = []
packet_sources = []
for pack in packets:
    if pack.bssid in known_bssids:
        pind = known_bssids.index(pack.bssid)
        packet_sources[pind].append(pack)
    else:
        known_bssids.append(pack.bssid)
        packet_sources.append([])
        pind = known_bssids.index(pack.bssid)
        packet_sources[pind].append(pack)

# Build individual router information
routers = []
for src in packet_sources:
    cur = Router() 
    for pack in src:
        cur.packet_count += 1
        cur.lat_ave += pack.lat
        cur.lon_ave += pack.lon
        cur.alt_ave += pack.alt
        cur.signal_dbm_ave += pack.signal_dbm
        cur.noise_dbm_ave += pack.noise_dbm
    cur.bssid = src[0].bssid
    cur.lat_ave = cur.lat_ave / len(src)
    cur.lon_ave = cur.lon_ave / len(src)
    cur.alt_ave = cur.alt_ave / len(src)
    cur.signal_dbm_ave = cur.signal_dbm_ave / len(src)
    cur.noise_dbm_ave = cur.noise_dbm_ave / len(src)
    routers.append(cur)

# Sort the list of routers by packet count.
routers = sorted(routers, key=lambda router: router.packet_count)

# Create KML file based off of gps locations.
kml = simplekml.Kml()
for src in routers:
    kml.newpoint(name=(str(src.bssid) + " " + str(src.signal_dbm_ave) \
                          + " " + str(src.packet_count)), \
                          coords=[(str(src.lon_ave), str(src.lat_ave))])
if len(sys.argv) > 2:
    kml.save(str(sys.argv[2]))
else:
    kml.save("testk.kml")
