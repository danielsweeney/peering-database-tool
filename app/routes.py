from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import PeersForm, PeeringSearchForm, ReportForm
from app.models import Exchange, Peer
from app.tables import Results, Results_IX

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    search = PeeringSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('index.html', form=search)

@app.route('/results')
def search_results(search):
    search_string = search.data['search']
    #print(search.data['select'])
    #print(search.data['search'])
    if search.data['select'] == 'ASN':
        qry = Peer.query.filter_by(asn=search.data['search']).all()
        table = Results(qry)
        return render_template('results.html', table=table, search=search)
    if search.data['select'] == 'Exchange':
        qry = Exchange.query.filter(Exchange.exchange_name.ilike("%" + search.data['search'] + "%")).all()
        print(qry)
        table = Results_IX(qry)
        return render_template('results.html', table=table, search=search)
    if search.data['select'] == 'Company':
        qry = Peer.query.filter(Peer.name.ilike("%" + search.data['search'] + "%")).all()
        print(qry)
        table = Results(qry)
        return render_template('results.html', table=table, search=search)
    if search.data['exchange'] is not '':
        ex_name_arr = search.data['exchange'].split(',')
        name = ex_name_arr[1]
        ixlan_id = ex_name_arr[2]

        ix_peer_results = Peer.query.filter_by(ixlan=ixlan_id).all()
        table = Results(ix_peer_results)

        return render_template('results.html', table=table, search=search)

@app.route('/edit_peer', methods=['GET', 'POST'])
def edit_peer():
    form = PeersForm()
    if form.validate_on_submit():
        flash('Added new Peer')
        #return redirect(url_for('exchanges'))
        return redirect("/edit_peer")
    return render_template('edit_peer.html', title='IX Peer', form=form)

def save_changes(peer, form, new=False):
    # Save the changes to the database

    peer.name = form.name.data
    peer.asn = form.asn.data
    peer.policy = form.policy.data
    peer.ipv4prefixes = form.ipv4prefixes.data
    peer.ipv6prefixes = form.ipv6prefixes.data
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
        if request.method == 'POST' and form.validate():
        #if form.validate_on_submit():
            # save edits
            print(peer)
            print(form)
            save_changes(peer, form)
            flash('Peer updated successfully!')
            return redirect('/')
        return render_template('edit_peer.html', form=form)
    else:
        return 'error loading #{id}'.format(id=id)

@app.route('/report', methods=['GET', 'POST'])
def report():
    form = ReportForm()
    if request.method == 'GET':
        return render_template('report.html', title='Existing Peering', form=form)
    return redirect('/')
