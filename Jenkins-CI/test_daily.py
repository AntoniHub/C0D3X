import sys
import json
import pprint
import unittest
import requests
import firebase_admin
from faker import Faker
from decouple import config
from firebase_admin import firestore
from firebase_admin import credentials
from html_reporter import HTMLTestRunner

"""
with open("serviceAccountKey.json") as serviceAccountKey:
    serviceAccountKey = json.load(serviceAccountKey)

cred = credentials.Certificate(serviceAccountKey)
firebase_admin.initialize_app(cred)
db = firestore.client()"""

API_KEY = config('API_KEY')

fake = Faker('es_ES')
s = requests.session()


class TestPhishingAPI(unittest.TestCase):
    def test_01_obtainCampaign(self):
        print('\n**********  Phishing Campaigns  **********')
        print('Starting -> Phishing Campaigns')
        r = s.get(
            'https://testing-api.cyberguardian.tech/campaigns/client/Z488h4SK0hr1Wx5Sat6l',
            # auth=TokenAuth(f'{APY_KEY}'),
            headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'x-api-key': '{}'.format(API_KEY)}
        )
        # self.assertEqual(r.status_code, 200)
        if r.status_code == 200:
            print("-------------------------------------------------")
            print(str(r.request) + "  " + str(r.status_code) + " " + r.reason + " in " + str(r.elapsed))
            print("-------------------------------------------------")
        else:
            print('[FAILED]  Ha devuelto -> {}'.format(r.status_code))
            sys.exit()


if __name__ == '__main__':
    # Generate report after execution
    runner = HTMLTestRunner(
        report_filepath="daily_test.html",
        title="Cyber Guardian",
        description="Endpoints CyberGuardian",
        open_in_browser=False    # Open browser after execution
    )
    # Execute unittest
    unittest.main(testRunner=runner)
    # unittest.main()
