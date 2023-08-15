import json
import pprint
import string

import xmltodict

subscription = """
  <subscriptions xmlns="http://riddl.org/ns/common-patterns/notifications-producer/2.0">
    <subscription xmlns="http://riddl.org/ns/common-patterns/notifications-producer/2.0" id="_student" url="https://lehre.bpm.in.tum.de/ports/9999/api/upload/log">
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


def add_subscription(xml: string, id: string):
    xml_as_json = xmltodict.parse(xml)
    subscription_as_json = xmltodict.parse(subscription)

    xml_as_json["testset"]["subscriptions"] = subscription_as_json["subscriptions"]
    xml_as_json["testset"]["attributes"]["info"] = id
    return xmltodict.unparse(xml_as_json)
