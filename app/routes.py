from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import PeersForm, PeeringSearchForm, ReportForm, RouterForm, ExchangeForm
from app.models import Exchange, Peer, Router
from app.tables import Results, Results_IX, Results_Router, Results_ASN
from peering_calls import get_asn_ips

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    #ix = Exchange.query.all()
    search = PeeringSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('index.html', form=search)

@app.route('/add_router', methods=['GET', 'POST'])
def add_router():
    form = RouterForm(request.form)
    if form.validate_on_submit():
        flash("Added new Router")
        save_router(form, new=True)
        return redirect('/add_router')
    if request.method == "POST":
        router_results()
    return render_template('router.html', title="Routers", form=form)

@app.route('/router_results')
def router_results():
    all_routers = Router.query.all()
    table = Results_Router(all_routers)
    return render_template('router_results.html', title="All Routers", table=table)

@app.route('/exchange_results')
def exchange_results():
    all_exchanges = Exchange.query.all()
    table = Results_IX(all_exchanges)
    return render_template('exchange_results.html', title="All Exchanges", table=table)

@app.route('/results')
def search_results(search):
    search_string = search.data['search']
    #print(search.data['select'])
    #print(search.data['search'])
    if search.data['select'] == 'ASN':
        qry = Peer.query.filter_by(asn=search.data['search']).all()
        #lookup_table = Exchange.query.all()
        print(qry[0].ixlan)
        #table = Results(qry)
        res = []
        for i in qry:
            ix = Exchange.query.filter_by(ixlan_id=i.ixlan).first().exchange_name
            line = str(i.id) + "," + str(i.asn) + "," + i.name + "," + ix
            res.append(line)
        print(res)
        #table = Results_ASN(res)
        #return render_template('results.html', table=table, search=search)
        return render_template('results.html', res=res, search=search)
    if search.data['select'] == 'Exchange':
        #page = request.args.get('page', 1, type=int)
        qry = Exchange.query.filter(Exchange.exchange_name.ilike("%" + search.data['search'] + "%")).all()
        #qry = Exchange.query.filter(Exchange.exchange_name.ilike("%" + search.data['search'] + "%")).paginate(page, app.config['RESULTS_PER_PAGE'], False)
        #print(qry)
        #print(qry.items)
        table = Results_IX(qry)
        return render_template('results.html', table=table, search=search)
    if search.data['select'] == 'Company':
        qry = Peer.query.filter(Peer.name.ilike("%" + search.data['search'] + "%")).all()
        #print(qry)
        table = Results(qry)
        return render_template('results.html', table=table, search=search)
    if search.data['exchange'] is not '':
        ex_name_arr = search.data['exchange'].split(',')
        name = ex_name_arr[1]
        ixlan_id = ex_name_arr[2]
        page = request.args.get('page', 1, type=int)

        ix_peer_results = Peer.query.filter_by(ixlan=ixlan_id).all()
        #ix_peer_results = Peer.query.filter_by(ixlan=ixlan_id).paginate(page, app.config['RESULTS_PER_PAGE'], False)
        table = Results(ix_peer_results)
        #print(table.items)
        #print(table)

        return render_template('results.html', table=table, search=search)



def save_router(form, new=False):
    router = Router()
    router.router_name = form.router_name.data
    router.region = form.region.data

    if new:
        #print(router)
        db.session.add(router)

    db.session.commit()

def save_exchange_changes(exchange, form, new=False):
    exchange.exchange_name = form.exchange_name.data
    exchange.ixlan_id = form.ixlan_id.data
    exchange.router = form.router_id.data
    #print(exchange.exchange_name)
    #print(exchange.ixlan_id)
    #print(exchange.router)
    if new:
        db.session.add(exchange)
    db.session.commit()

def save_router_changes(router, form, new=False):
    router.router_name = form.router_name.data
    router.region = form.region.data

    if new:
        db.session.add(router)
    db.session.commit()


def save_changes(peer, form, new=False):
    # Save the changes to the database

    peer.name = form.name.data
    peer.asn = form.asn.data
    peer.policy = form.policy.data
    peer.ipv4prefixes = form.ipv4prefixes.data
    peer.ipv6prefixes = form.ipv6prefixes.data
    peer.region = form.region.data
    peer.as_set = form.as_set.data
    if form.Peered_IPv4.data == "True":
        peer.peered_IPv4 = 1
    else:
        peer.peered_IPv4 = 0
    if form.Peered_IPv6.data == "True":
        peer.peered_IPv6 = 1
    else:
        peer.peered_IPv6 = 0

    if new:
        # add the peer to the database
        db.session.add(peer)
    # commit the data to the database
    db.session.commit()
    print('Here I am:))))""')

@app.route('/peer_id/<int:id>', methods=['GET', 'POST'])
def edit(id):
    peer = Peer.query.filter_by(id=id).first()

    if peer:
        #print(peer)
        form = PeersForm(formdata=request.form, obj=peer)
        print(form)
        #if form.id == "generate":
            #return generate_config(peer, form)
        #if request.method == 'POST' and form.validate():
        if form.validate_on_submit():
            save_changes(peer, form)
            #return generate_config(peer, form)
            flash('Peer updated successfully!')
            return redirect('/')
        return render_template('edit_peer.html', form=form)
    else:
        return 'error loading #{id}'.format(id=id)

@app.route('/exchange_id/<int:id>', methods=['GET','POST'])
def edit_exchange(id):
    exchange = Exchange.query.filter_by(id=id).first()
    print(exchange)
    if exchange:
        form = ExchangeForm(formdata=request.form, obj=exchange)
        if form.validate_on_submit():
            print(exchange)
            print(form)
            save_exchange_changes(exchange, form)
            flash('Exchange updated successfully!')
            return redirect('/')
        return render_template('edit_exchange.html', form=form)
    else:
        return 'error loading #{id}'.format(id=id)

@app.route('/router_id/<int:id>', methods=['GET', 'POST'])
def edit_router(id):
    router = Router.query.filter_by(id=id).first()

    if router:
        form = RouterForm(formdata=request.form, obj=router)
        if form.validate_on_submit():
            save_router_changes(router, form)
            flash("Router updated successfully!")
            return redirect('/')
        return render_template('edit_router.html', form=form)
    else:
        return 'error loading #{id}'.format(id=id)

@app.route('/report', methods=['GET', 'POST'])
def report():
    form = ReportForm()
    if request.method == 'GET':
        return render_template('report.html', title='Existing Peering', form=form)
    return redirect('/')

@app.route('/config.html', methods=['GET', 'POST'])
def generate_config(peer, form):
    peer.name = form.name.data
    peer.asn = form.asn.data
    peer.region = form.region.data
    ipaddresses = get_asn_ips(peer.asn)
    peer.ipv4prefixes = form.ipv4prefixes.data
    peer.ipv6prefixes = form.ipv6prefixes.data

    configs_arr = []

    #print(peer.ixlan)
    #print(ipaddresses[0])
    exchange = Exchange.query.filter_by(ixlan_id=peer.ixlan).all()
    for line in exchange:
        print(line)
        for item in ipaddresses:
            #print(type(item))
            if line.exchange_name in item:
                print(line.exchange_name)
                print(item)
                #if request.method =='POST'
                configs_arr.append(item)

    return render_template('config.html', peer=peer, item=configs_arr)

    #for line in ipaddresses:
    #    if exchange.exchange_name in line[0]:
    #        print(exchange)
    #        print(line)


    #print(peer.name, peer.asn, peer.ixlan, peer.region, ipaddresses, peer.ipv4prefixes, peer.ipv6prefixes)
