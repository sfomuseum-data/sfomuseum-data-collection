#!/usr/bin/env python

# Don't hold on to this. It _will_ be replaced, shortly.
# (20200226/thisisaaronland)

import mapzen.whosonfirst.utils
import mapzen.whosonfirst.export

import re

"""
"John F. Kennedy International Airport (JFK)":[ 102534365 ]

"""

if __name__ == "__main__":

    depicts_label = "Boeing 747-400"
    depicts_id = [ 1159289915, 1159293593, 1159289873 ]

    p = r'.*' + re.escape(depicts_label) + '.*'
    pat = re.compile(p)

    data = "data"

    exporter = mapzen.whosonfirst.export.flatfile(data)

    crawl = mapzen.whosonfirst.utils.crawl(data, inflate=True)

    for feature in crawl:

        props = feature["properties"]

        wof_name = props["wof:name"]
        wof_id = props["wof:id"]
        
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
        
        depicts = props.get("wof:depicts", [])

        if depicts_id in depicts:
            continue

        depicts.append(depicts_id)
        props["wof:depicts"] = depicts
        feature["properties"] = props
        
        print exporter.export_feature(feature)
        
        
        
