from flask_table import Table, Col, BoolCol, LinkCol

class Results(Table):
    classes = ['table', 'table-striped', 'table-bordered', 'table-condensed']
    id = Col('id', show=False)
    #id = Col('id')
    asn = Col('ASN')
    name = Col('Company')
    policy = Col('Policy', show=False)
    ipv4prefixes = Col('IPv4 Max Prefix')
    ipv6prefixes = Col('IPv6 Max Prefix')
    as_set = Col('AS-SET')
    peered_IPv4 = BoolCol('IPv4 Peered')
    peered_IPv6 = BoolCol('IPv6 Peered')
    region = Col('Region')
    ixlan = Col('ixlan_id', show=False)
    edit = LinkCol('edit', 'edit', url_kwargs=dict(id='id'))
    #ixlan = Col('ixlan_id')
    #peered = BoolCol('Peered', yes_display='Yes', no_display='No')

class Results_ASN(Table):
    classes = ['table', 'table-striped', 'table-bordered', 'table-condensed']
    id = Col('id', show=False)
    #asn = Col('ASN')
    #1 = Col('ASN')
    #company = Col('Company')
    #2 = Col('Company')
    #peered_IPv4 = BoolCol('IPv4 Peered')
    #peered_IPv6 = BoolCol('IPv6 Peered')
    #region = Col('Region')
    #ix = Col('Exchange')
    #3 = Col('Exchange')
    #edit = LinkCol('edit', 'edit', url_kwargs=dict(id='id'))

class Results_IX(Table):
    classes = ['table', 'table-striped', 'table-bordered', 'table-condensed']
    id = Col('id', show=True)
    exchange_name = Col('Exchange')
    ixlan_id = Col('ixlan_ID')
    router = Col('router_ID', show=True)
    #Peers = LinkCol('peers', 'peers', url_kwargs=dict(id='id'))
    edit = LinkCol('edit', 'edit_exchange', url_kwargs=dict(id='id'))

class Results_Router(Table):
    classes = ['table', 'table-striped', 'table-bordered', 'table-condensed']
    id = Col('id', show=True)
    router_name = Col('Router')
    region = Col('Region')
    edit = LinkCol('edit', 'edit_router', url_kwargs=dict(id='id'))

