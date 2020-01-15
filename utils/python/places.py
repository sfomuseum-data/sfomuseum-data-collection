#!/usr/bin/env python

import json
import pprint

import mapzen.whosonfirst.utils
import mapzen.whosonfirst.uri
import mapzen.whosonfirst.export
import requests

places = {}

def get_place(candidates):

    for placetype, place in candidates.items():

        feature = places.get(place, None)

        if feature:

            if feature == -1:
                return None

            return feature

        params = {
            "term": place,
            "placetype": placetype
        }

        url = "https://millsfield.sfomuseum.org/places/api/search"
        rsp = requests.get(url, params=params)

        if rsp.status_code != 200:
            continue

        try:
            data = json.loads(rsp.content)
        except Exception, e:
            continue

        if len(data) != 1:
            continue

        pl = data[0]
        id = pl["id"]

        rel_path = mapzen.whosonfirst.uri.id2relpath(id)
        url = "https://data.whosonfirst.org/%s" % rel_path 

        rsp = requests.get(url)

        if rsp.status_code != 200:
            continue
            
        try:
            f = json.loads(rsp.content)
            places[place] = f
            return f
        except Exception, e:
            continue

    return None


if __name__ == "__main__":

    data = "data"

    crawl = mapzen.whosonfirst.utils.crawl(data, inflate=True)
    exporter = mapzen.whosonfirst.export.flatfile(data)

    for feature in crawl:

        props = feature["properties"]
        country = props.get("sfomuseum:country", None)
        continent = props.get("sfomuseum:continent", None)

        if not country and not continent:
            continue

        candidates = {}

        if country:
            candidates["country"] = country

        if continent:
            candidates["continent"] = continent

        place = get_place(candidates)

        if not place:
            continue

        pl_props = place["properties"]
        pl_country = pl_props["wof:country"]
        pl_hierarchy = pl_props["wof:hierarchy"]

        props["wof:country"] = pl_country
        props["iso:country"] = pl_country

        for h in pl_hierarchy:
            props["wof:hierarchy"].append(h)

        feature["properties"] = props
        print exporter.export_feature(feature)
