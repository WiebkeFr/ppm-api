import json
import pprint
import string

import xmltodict

subscription = """
  <subscriptions xmlns="http://riddl.org/ns/common-patterns/notifications-producer/2.0">
    <subscription xmlns="http://riddl.org/ns/common-patterns/notifications-producer/2.0" id="_student" url="https://lehre.bpm.in.tum.de/ports/9009/api/log">
      <topic id="state">
      <event>change</event>
      </topic>
      <topic id="activity">
      <event>calling</event>
      <event>failed</event>
      <event>done</event>
      </topic>
    </subscription>
  </subscriptions>
"""


def add_subscription(xml: string):
    xml_as_json = xmltodict.parse(xml)
    subscription_as_json = xmltodict.parse(subscription)

    pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(json.dumps(xml_as_json))

    xml_as_json["testset"]["subscriptions"] = subscription_as_json["subscriptions"]

    # pp.pprint(json.dumps(xml_as_json))
    # pp.pprint(json.dumps(subscription_as_json))

    # print(xmltodict.unparse(xmltodict.parse(xml), pretty=True))
    return xmltodict.unparse(xml_as_json)
