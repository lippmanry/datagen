# %%
#thank you george starcher for the collector class and example https://github.com/georgestarcher/Splunk-Class-httpevent
from splunk_http_event_collector import http_event_collector
from faker import Faker
import json
import logging
import sys
import os
from dotenv import load_dotenv
fake = Faker()
Faker.seed(13)

# %%
load_dotenv()
key = os.getenv('key')
host = os.getenv('host')


# %%
def datagen():

    for i in range(5):
        return{
            'hostname': fake.hostname(levels=0),
            'ipv4': fake.ipv4(),
            'fqdn': fake.domain_name(2),
            'mac_address': fake.mac_address(),
            'subnet': fake.ipv4(network=True, private='Public'),
            'username': fake.user_name(),
            'email': fake.company_email(),
            'manager_email':fake.company_email(),
            'country': fake.country(),
            'date': fake.iso8601(sep=' ')
        }

# %%
# init logging config, this would be job of your main code using this class.
logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S %z')


# Create event collector object, default SSL and HTTP Event Collector Port
http_event_collector_key = key
http_event_collector_host = host

writeevent = http_event_collector(http_event_collector_key, http_event_collector_host)

# perform a HEC reachable check
hec_reachable = writeevent.check_connectivity()
if not hec_reachable:
    sys.exit(1)

# %%
# Set to pop null fields.  Always a good idea
writeevent.popNullFields = True
# set logging to DEBUG for example
writeevent.log.setLevel(logging.DEBUG)

# Start event payload and add the metadata information
payload = {}
payload.update({"index":"asset"})
payload.update({"sourcetype":"json_no_timestamp"})
payload.update({"source":"UserData"})


# %%
for i in range(5000):
    event = datagen()
    event.update({"action":"success"})
    event.update({"event_type":"single"})
    event.update({"event_id":i})
    payload.update({"event":event})
    writeevent.sendEvent(payload)    


