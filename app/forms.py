from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Optional
from app.models import Exchange

class PeersForm(FlaskForm):
    policy_choices = [
            ('Open', 'Open'),
            ('Selective', 'Selective'),
            ('Restrictive', 'Restrictive')
            ]
    ip_peered = [
            ('True', 'True'),
            ('False', 'False')
            ]
    region_choices = [
            ('North America','North America'),
            ('Europe', 'Europe'),
            ('Asia', 'Asia')
            ]
    name = StringField('Company', validators=[DataRequired()])
    asn = IntegerField('AS Number', validators=[DataRequired()])
    #policy = StringField('Policy', validators=[DataRequired()])
    policy = SelectField('Policy', choices=policy_choices)
    ipv4prefixes = IntegerField('IPv4 Prefixes', validators=[DataRequired()])
    ipv6prefixes = IntegerField('IPv6 Prefixes', validators=[DataRequired()])
    as_set = StringField('AS-SET', validators=[DataRequired()])
    #Peered_IPv4 = BooleanField('Peered_IPv4', validators=[DataRequired()])
    Peered_IPv4 = SelectField('Peered IPv4', choices=ip_peered)
    region = SelectField('Region', choices=region_choices)
    #Peered_IPv6 = BooleanField('Peered_IPv6', validators=[DataRequired()])
    Peered_IPv6 = SelectField('Peered IPv6', choices=ip_peered)
    ixlan = IntegerField('IXLAN ID', validators=[Optional()])
    submit = SubmitField('Update Peer Details')
    generate = SubmitField('Generate Config')

class ExchangeForm(FlaskForm):
    exchange_name = StringField('Name')
    ixlan_id = IntegerField('Exchange ID - PeeringDB ixlan_ID')
    router_id = IntegerField('Local Database Router ID')
    submit = SubmitField('Update')

class PeeringSearchForm(FlaskForm):
    choices =[
            ('Exchange', 'Exchange'),
            ('ASN', 'ASN'),
            ('Company', 'Company')
            ]
    ix = Exchange.query.all()
    #print(ix)
    select = SelectField('Search Peering Information:', choices=choices)
    exchange = SelectField('Pick an Exchange: ', choices=ix)
    #search = StringField('')
    search = StringField('Search')

class RouterForm(FlaskForm):
    router_name = StringField('Router', validators=[DataRequired()])
    region = StringField('Region', validators=[DataRequired()])
    submit = SubmitField('Add Router')
    submit_search = SubmitField('List Routers')

class ReportForm(FlaskForm):
    submit_ipv4 = SubmitField('Get Existing IPv4 Report')
    submit_ipv6 = SubmitField('Get Existing IPv6 Report')
    traffic_report = SubmitField('Traffic Reports')
