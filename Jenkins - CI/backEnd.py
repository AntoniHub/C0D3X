import sys
import pprint
import requests
import firebase_admin
from faker import Faker
from firebase_admin import firestore
from firebase_admin import credentials


cred = credentials.Certificate(r"C:\AntonioRodriguezFarias\serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

fake = Faker('es_ES')
s = requests.session()


##########################
###     Campaigns      ###
##########################
print('\n**********  Antonio Rodriguez  **********')
# GET -> https://api-testing.arodriguezf.tech/campaigns/users
# POST -> https://api-testing.arodriguezf.tech/campaigns/users

# Get Campaigns
print('Starting -> Test')
r = s.get(
    'https://api-testing.arodriguezf.tech/campaigns/users/Z476h4SK0hr1Wx5Zat1l',
    # auth=TokenAuth('APY_KEY'),
    headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'x-api-key': 'API_KEY'}
)
if r.status_code == 200:
    print("-------------------------------------------------")
    print(str(r.request) + "  " + str(r.status_code) + " " + r.reason + " in " + str(r.elapsed))
    print("-------------------------------------------------")
else:
    print('[FAILED]  Ha devuelto -> {}'.format(r.status_code))
    sys.exit()


# POST -> https://api-testing.arodriguezf.tech/campaigns/users/Z488h4SK0hr1Wx5Sat6l
# Create Campaign
print('\nCreating Campaign')
r = s.post(
    'https://api-testing.arodriguezf.tech/campaigns/users/Z476h4SK0hr1Wx5Zat1l',
    headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'x-api-key': 'API_KEY'},
    json={
        "custom_name": "Coronavirus (Covid 19)",
        "campaign_type": "virus_campaigns_es",
        "destinations": [{
            "email": "abgrodriguezfarias@gmail.com",
            "first_name": "Antonio",
            "last_name": "Rodriguez",
            "position": ""
        }],
        "customization": {
            "company": "Prueba",
            "email": "abgrodriguezfarias@gmail.com"
        }
    }
)
if r.status_code == 200:
    print("-------------------------------------------------")
    print(str(r.request) + "  " + str(r.status_code) + " " + r.reason + " in " + str(r.elapsed))
    print("-------------------------------------------------")
else:
    print('[FAILED]  Ha devuelto -> {}'.format(r.status_code))
    sys.exit()


# Delete Campaign previously created
verify = db.collection(u'users').document(u'Z476h4SK0hr1Wx5Zat1l').collection('campaigns').get()
pp = pprint.PrettyPrinter(indent=4)
for x in verify:
    if x.exists:
        y = x.get('campaign_id')
        verify2 = db.collection(u'users').document(u'Z476h4SK0hr1Wx5Zat1l').collection('campaigns').document(
            '{}'.format(y)).get()
        if verify2.exists:
            """pp.pprint(verify2.to_dict())"""
            db.collection(u'users').document(u'Z476h4SK0hr1Wx5Zat1l').collection('campaigns').document(
                '{}'.format(y)).delete()
            """print('DELETED Campaign {}'.format(y))"""
            """print("    ---------------------")"""




#######################
######  CLIENTS  ######
#######################
print('\n\n**********  Clients  **********')
# POST -> https://api-testing.arodriguezf.tech/users/Z488h4SK0hr1Wx5Sat6l/members
# Create team_member
print('Starting -> Clients \n    Create team_member')
r = s.post(
    'https://api-testing.arodriguezf.tech/users/Z488h4SK0hr1Wx5Sat6l/members',
    headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'x-api-key': 'API_KEY'},
    json={
        "name": "Alejandro",
        "surname": "Farias",
        "email": "abgrodriguezfarias@gmail.com",
        "language": "es",
        "role": "employee"
    }
)
if r.status_code == 201:
    print("-------------------------------------------------")
    print(str(r.request) + "  " + str(r.status_code) + " " + r.reason + " in " + str(r.elapsed))
    print("-------------------------------------------------")
else:
    print('[FAILED]  Ha devuelto -> {}'.format(r.status_code))
    sys.exit()


# Delete team_member previously created
verify = db.collection(u'users').document(u'Z476h4SK0hr1Wx5Zat1l').collection(u'members').where(
    u'email', u'==', u'test_py@cyberguardiantesting.com').get()
pp = pprint.PrettyPrinter(indent=4)
for x in verify:
    if x.exists:
        id = x.id
        db.collection(u'users').document(u'Z476h4SK0hr1Wx5Zat1l').collection(u'members').document('{}'.format(id)).delete()
        """print('\n    Team Member -> {} was removed'.format(id))"""
        """print("----------------------------------------------------------------------------")"""


# POST -> https://api-testing.arodriguezf.tech/users/Z476h4SK0hr1Wx5Zat1l/tags
# Create TAG in teamMember: 40b5066a0e9111fb121af3883f6f60a9b98387506faf8
print('\nCreating TAG')
r = s.post(
    'https://api-testing.arodriguezf.tech/clients/Z476h4SK0hr1Wx5Zat1l/tags',
    headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'x-api-key': 'API_KEY'},
    json={
        "tag": "TAG_test",
        "color": "#FFFFFF",
        "members": [
            "40b5066a0e9111fb121af3883f6f60a9b98387506faf8"
        ]
    }
)
if r.status_code == 200:
    print("-------------------------------------------------")
    print(str(r.request) + "  " + str(r.status_code) + " " + r.reason + " in " + str(r.elapsed))
    print("-------------------------------------------------")
else:
    print('[FAILED]  Ha devuelto -> {}'.format(r.status_code))
    sys.exit()


verify2 = db.collection(u'users').document(u'Z476h4SK0hr1Wx5Zat1l').collection(u'members').document(
    '40b5066a0e9111fb121af3883f6f60a9b98387506faf8').get()
if verify2.exists:
    """print(verify2.to_dict())"""
    y = verify2.get('tags')
    TAG = y[2]


# PUT -> https://api-testing.arodriguezf.tech/users/Z488h4SK0hr1Wx5Sat6l/tags/d0i5RTFJBURFHJ3G64mK
# Update color TAG
print('\nUpdating color TAG')
r = s.put(
    'https://api-testing.arodriguezf.tech/users/Z476h4SK0hr1Wx5Zat1l/tags/d0i5RTFJBURFHJ3G64mK',
    headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'x-api-key': 'API_KEY'},
    json={
        "tag": "{}".format(TAG),
        "color": "{}".format(fake.safe_hex_color()),
        "members": [
            "40b5066a0e9111fb121af3883f6f60a9b98387506faf8"
        ]
    }
)
if r.status_code == 200:
    print("-------------------------------------------------")
    print(str(r.request) + "  " + str(r.status_code) + " " + r.reason + " in " + str(r.elapsed))
    print("-------------------------------------------------")
else:
    print('ERROR  -> {}'.format(r.status_code))
    sys.exit()


# PUT -> https://api-testing.arodriguezf.tech/users/Z476h4SK0hr1Wx5Zat1l/tags/members
# Update TAG for given members
print('\nUpdating TAG for given members')
r = s.put(
    'https://api-testing.arodriguezf.tech/users/Z476h4SK0hr1Wx5Zat1l/tags/members',
    headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'x-api-key': 'API_KEY'},
    json={
        "members": [
            "40b5066a0e9111fb121af3883f6f60a9b98387506faf8"
            ],
        "to_tag": [
            "{}".format(TAG)
            ]
    }
)
if r.status_code == 200:
    print("-------------------------------------------------")
    print(str(r.request) + "  " + str(r.status_code) + " " + r.reason + " in " + str(r.elapsed))
    print("-------------------------------------------------")
else:
    print('[FAILED]  Ha devuelto -> {}'.format(r.status_code))
    sys.exit()


# DELETE -> https://api-testing.arodriguezf.tech/clients/Z476h4SK0hr1Wx5Zat1l/tags/TAG
# Delete TAG previously created
print('\nDeleting TAG')
r = s.delete(
    'https://api-testing.arodriguezf.tech/users/Z476h4SK0hr1Wx5Zat1l/tags/{}'.format(TAG),
    headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'x-api-key': 'API_KEY'}
)
if r.status_code == 200:
    print("-------------------------------------------------")
    print(str(r.request) + "  " + str(r.status_code) + " " + r.reason + " in " + str(r.elapsed))
    print("-------------------------------------------------")
else:
    print('ERROR  -> {}'.format(r.status_code))
    sys.exit()




#######################
###  SUBSCRIPTIONS  ###
#######################
print('\n\n**********  Subscriptions  **********')
# GET -> https://api-testing.arodriguezf.tech/subscription?user=JN15NkDqqHlyNkSKk4T1&product=vip
# Get subscription client
print('Getting Subscriptions')
params = {
    'client': 'Z476h4SK0hr1Wx5Zat1l',
    'product': 'vip'
}
r = s.get(
    'https://api-testing.arodriguezf.tech/subscription',
    params=params,
    headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'x-api-key': 'API_KEY'}
)
if r.status_code == 200:
    print("-------------------------------------------------")
    print(str(r.request) + "  " + str(r.status_code) + " " + r.reason + " in " + str(r.elapsed))
    print("-------------------------------------------------")
else:
    print('[FAILED]  Ha devuelto -> {}'.format(r.status_code))
    sys.exit()


# POST -> https://api-testing.arodriguezf.tech/subscription
# Create subscription
print('\nCreating Subscriptions')
params = {
    'client': 'Z476h4SK0hr1Wx5Zat1l',
    'product': 'vip',
    'stripeId': 'sub_1kw1WCBPoyyxSIcSr2I46SOZ',
    'stripeCustomer': 'cus_phQLkUqlUwKzyO',
    'stripeSession': "",
    'endDate': '2037-01-02T15:04:05Z'
}
r = s.post(
    'https://api-testing.arodriguezf.tech/subscription',
    params=params,
    headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'x-api-key': 'API_KEY'}
)
if r.status_code == 200:
    print("-------------------------------------------------")
    print(str(r.request) + "  " + str(r.status_code) + " " + r.reason + " in " + str(r.elapsed))
    print("-------------------------------------------------")
else:
    print('[FAILED]  Ha devuelto -> {}'.format(r.status_code))
    sys.exit()




#################
###  Reports  ###
#################
print('\n\n**********  Reports  **********')
# GET -> https://api-testing.arodriguezf.tech/reporting/example.com
# Get report [SCORING]
print('Getting report')
params = {
    'email_at': 'abgrodriguezfarias@gmail.com'
}
r = s.get(
    'https://api-testing.arodriguezf.tech/reporting/arodriguezf.com',
    params=params,
    headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'x-api-key': 'API_KEY'}
)
if r.status_code == 200:
    print("-------------------------------------------------")
    print(str(r.request) + "  " + str(r.status_code) + " " + r.reason + " in " + str(r.elapsed))
    print("-------------------------------------------------")
else:
    print('[FAILED]  Ha devuelto -> {}'.format(r.status_code))
    sys.exit()


# GET -> https://api-testing.arodriguezf.tech/reporting/example.es
# Get report [WEB]
print('\nGetting report')
params = {
    'email_at': 'abgrodriguezfarias@gmail.com'
}
r = s.get(
    'https://api-testing.arodriguezf.tech/webreporting/arodriguezf.es',
    params=params,
    headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'x-api-key': 'API_KEY'}
)
if r.status_code == 200:
    print("-------------------------------------------------")
    print(str(r.request) + "  " + str(r.status_code) + " " + r.reason + " in " + str(r.elapsed))
    print("-------------------------------------------------")
else:
    print('[FAILED]  Ha devuelto -> {}'.format(r.status_code))
    sys.exit()




########################
###  Security Scans  ###
########################
print('\n\n**********  Security Scans  **********')
# POST -> https://api-testing.arodriguezf.tech/scaners
# Scan WEB domain
print('Scanning domain')
params ={
    'domain': 'example.es'
}
r = s.post(
    'https://api-testing.arodriguezf.tech/scaners',
    params=params,
    headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'x-api-key': 'API_KEY'}
)
if r.status_code == 202:
    print("-------------------------------------------------")
    print(str(r.request) + "  " + str(r.status_code) + " " + r.reason + " in " + str(r.elapsed))
    print("-------------------------------------------------")
else:
    print('[FAILED]  Ha devuelto -> {}'.format(r.status_code))
    sys.exit()


# POST -> https://api-testing.arodriguezf.tech/scaners/@arodriguezf.com
# Scan WEB domain
print('\nScanning domain')
r = s.post(
    'https://api-testing.arodriguezf.tech/scaners/@arodriguezf.com',
    headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'x-api-key': 'API_KEY'}
)
if r.status_code == 202:
    print("-------------------------------------------------")
    print(str(r.request) + "  " + str(r.status_code) + " " + r.reason + " in " + str(r.elapsed))
    print("-------------------------------------------------")
else:
    print('[FAILED]  Ha devuelto -> {}'.format(r.status_code))
    sys.exit()




##################
###  Breaches  ###
##################
print('\n\n**********  Breaches  **********')
# POST -> https://api-testing.arodriguezf.tech/breach/dismisses
# Scan WEB domain
print('Breaches - Dismiss')
params = {
    'email': 'abgrodriguezfarias@gmail.com',
    'client': 'pXXVQgmvbouNe1qHsUjy',
    'breach': 'stub breach',
    'date': '2036-01-02T15:04:05Z'
}
r = s.post(
    'https://api-testing.arodriguezf.tech/breach/dismisses',
    params=params,
    headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'x-api-key': 'API_KEY'}
)
if r.status_code == 200:
    print("-------------------------------------------------")
    print(str(r.request) + "  " + str(r.status_code) + " " + r.reason + " in " + str(r.elapsed))
    print("-------------------------------------------------")
else:
    print('[FAILED]  Ha devuelto -> {}'.format(r.status_code))
    sys.exit()
