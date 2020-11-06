#from peering_calls import get_asn_ix, get_asn_ips, get_prefix_and_name
import requests
from urllib.request import HTTPError
import json
from app.models import Peer, Exchange
from app import db

def build_IX_table(asn):
    ixlan = {}
    try:
        obj = requests.get("https://peeringdb.com/api/netixlan?asn=%s" % asn)
        obj_dict = obj.json()
        for line in obj_dict["data"]:
            ixlan[line["ixlan_id"]] = line["name"]
        print(ixlan)
        for line in ixlan.items():
            ix = Exchange(ixlan_id=line[0], exchange_name=line[1])
            db.session.add(ix)
            db.session.commit()

    except HTTPError as e:
        print(e)
        return

def build_peers_table(asn):
    ixlan = {}
    try:
        obj = requests.get("https://peeringdb.com/api/netixlan?asn=%s" % asn)
        obj_dict = obj.json()
        for line in obj_dict["data"]:
            ixlan[line["ixlan_id"]] = line["name"]

        for ixlan_id_key in ixlan:
            ixlan_obj = requests.get("https://peeringdb.com/api/net?ixlan_id=%s" % str(ixlan_id_key))
            ixlan_object_dict = ixlan_obj.json()
            #print(ixlan_object_dict)
            for line in ixlan_object_dict["data"]:
                peer = Peer(ixlan=ixlan_id_key, asn=line["asn"], name=line["name"], policy=line["policy_general"], ipv4prefixes=line["info_prefixes4"], ipv6prefixes=line["info_prefixes6"], as_set=line["irr_as_set"], peered_IPv4=False, peered_IPv6=False, region="TBA")
                db.session.add(peer)
                db.session.commit()

    except HTTPError as e:
        print(e)
        return

