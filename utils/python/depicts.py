#!/usr/bin/env python

# Don't hold on to this. It _will_ be replaced, shortly.
# (20200226/thisisaaronland)

import mapzen.whosonfirst.utils
import mapzen.whosonfirst.export

import re

"""
	"John F. Kennedy International Airport (JFK)":[ 102534365 ],
        "Boeing 747-400": [ 1159289915, 1159293593, 1159289873 ],
        "Qantas Airways": [ 1159285043 ],
        "Sunset District": [ 1108830803, 85922583, 85688637, 85633793 ],
        "Richmond District": [ 1108830805, 85922583, 85688637, 85633793 ],
        "Presidio": [ 85865991, 85922583, 85688637, 85633793 ],
        "San Francisco International Airport (SFO)": [102527513],	
        "downtown San Francisco": [ 1108830801, 85688637, 85633793 ],
        "Oakland": [ 85921881, 85688637, 85633793 ],
        "Super Bay Hangar": [ 1477855969 ]
"""

if __name__ == "__main__":

    depicts_key = {
        "SFO Helicopter Airlines": [ 1159285141 ],
        "Sikorsky S-61": [ 1159291711] 
    }
    
    data = "data"

    exporter = mapzen.whosonfirst.export.flatfile(data)

    crawl = mapzen.whosonfirst.utils.crawl(data, inflate=True)

    for feature in crawl:

        props = feature["properties"]

        wof_name = props["wof:name"]
        wof_id = props["wof:id"]

        depicts = props.get("wof:depicts", [])
        updates = False
        
        for depicts_label, depicts_ids in depicts_key.items():
        
            p = r'.*' + re.escape(depicts_label) + '.*'
            pat = re.compile(p)
                        
            candidates = [
                "wof:name",
                "sfomuseum:label",
                "sfomuseum:description"
            ]

            match = False
        
            for k in candidates:
            
                v = props.get(k, None)

                if not v:
                    continue

                if not pat.match(v):
                    continue

                match = True
                break

            if not match:
                continue

            for id in depicts_ids:
                
                if id in depicts:
                    continue

                depicts.append(id)
                updates = True

        if not updates:
            continue
        
        props["wof:depicts"] = depicts
        feature["properties"] = props

        print "update", wof_name
        print exporter.export_feature(feature)
        
        
        
