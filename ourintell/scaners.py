import nmap
import json

from ourintell.models import ScanResult

from ourintell import db

def nmap_scan(address):
    nmScan = nmap.PortScanner()
    return nmScan.scan(address)


def scan(event):
    event_dict = event.asDict()

    if  "source.ip" in event_dict['event_data']:
        address = event_dict['event_data']["source.ip"]
    else:
        address = event_dict['event_data']["source.fqdn"]

    result = {}
    result.update(nmap_scan(address))

    formated_result = ScanResult(eventId = event.id, scan_data = json.dumps(result))
    db.session.add(formated_result)
    db.session.commit()
    