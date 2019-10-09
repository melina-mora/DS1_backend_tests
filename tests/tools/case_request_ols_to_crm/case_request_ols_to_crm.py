import base64
import json
import quopri

from requests import get, post, patch, put
from requests_toolbelt.multipart.encoder import MultipartEncoder

import tools.case_request_ols_to_crm.case_request_login as helpers


def check_resp(resp):
    assert resp.status_code == 200, "error %s" % resp.__dict__


def text_to_encoded_words(text, charset, encoding):
    """
    text: text to be transmitted
    charset: the character set for text
    encoding: either 'q' for quoted-printable or 'b' for base64
    """
    byte_string = text.encode(charset)
    if encoding.lower() == 'b':
        encoded_text = base64.b64encode(byte_string)
    elif encoding.lower() == 'q':
        encoded_text = quopri.encodestring(byte_string)
    else:
        raise Exception("unsupported encoding")
    return "=?{charset}?{encoding}?{encoded_text}?=".format(
        charset=charset.upper(),
        encoding=encoding.upper(),
        encoded_text=encoded_text.decode('ascii'))


def prepare_payload(headers, document_name):
    m = MultipartEncoder(
        fields={
            "documentDetail": json.dumps({"fileName": document_name}),
            "file": (document_name, open(document_name, 'rb'), 'application/pdf')
        },  # boundary="33b4531a79be4b278de5f5688fab7701"
    )
    headers["Content-Type"] = m.content_type
    return headers, m


url = "https://uscldcnxapmd01.azure-api.net"
headers = helpers.login(url, "S1.CustInf01.MX@mailinator.com", "TestS1cxg0")
print(headers)
customer_id = 3991
jobsite_id = 819  # 157  # 157
type_id = 1
has_document = True

# print("contactCode='%s'"%contact["contactCode"])
payload = {"customer": {"customerId": customer_id}}
resp = post(url=url + "/v1/csm/cases", headers=headers, json=payload)
check_resp(resp)

case_id = resp.json()["caseId"]
# print("case_id=%s" % case_id)

# print("patch description")
payload = {"caseDesc": "Ols description Meli"}
resp = patch(url="%s/v1/csm/cases/%s/descriptions" % (url, case_id), headers=headers, json=payload)
check_resp(resp)

# print("patch caseTitle")
payload = {"caseTitle": "Ols title Meli"}
resp = patch(url="%s/v1/csm/cases/%s/titles" % (url, case_id), headers=headers, json=payload)
check_resp(resp)

# print("patch casetype")
resp = patch(url="%s/v1/csm/cases/%s/casetypes/%s" % (url, case_id, type_id), headers=headers)
check_resp(resp)

if jobsite_id:
    print("patch jobsite")
    resp = patch(url="%s/v1/csm/cases/%s/jobsites/%s" % (url, case_id, jobsite_id), headers=headers)
    check_resp(resp)

print("put contacts")
# resp = get(url="%s/v1/csm/cases/%s/contacts" % (url, case_id), headers=headers)
# check_resp(resp)
# print(json.dumps(resp.json(),indent=4))
# contact=resp.json()["contacts"][4]
# contact_id = contact["contactId"]
# print(len(resp.json()["contacts"]))
# print("contactId=%s" % contact_id)
resp = get(url="%s/v1/csm/cases/%s/contacts" % (url, case_id), headers=headers)
check_resp(resp)
# print(json.dumps(resp.json(),indent=4))
contact = resp.json()["contacts"][1]
contact_id = contact["contactId"]
print("contact_id=%s" % contact_id)
payload = {"caseContacts": [{"contact": {"contactId": contact_id}}]}

resp = put(url="%s/v1/csm/cases/%s/casecontacts" % (url, case_id), headers=headers, json=payload)
check_resp(resp)

if jobsite_id:
    print("put businesslines")
    resp = get(url="%s/v1/csm/cases/%s/businesslines" % (url, case_id), headers=headers)
    check_resp(resp)

    businessline_id = resp.json()["businessLines"][0]["businessLineId"]
    print("businessline_id=%s" % businessline_id)
    payload = {"caseBusinessLines": [{"businessLine": {"businessLineId": businessline_id}}]}

    resp = put(url="%s/v1/csm/cases/%s/casebusinesslines" % (url, case_id), headers=headers, json=payload)
    check_resp(resp)

if has_document:
    headers, m = prepare_payload(headers, "response.pdf")
    print(headers)
    resp = post(url="%s/v1/csm/cases/%s/casedocuments" % (url, case_id), data=m.to_string(), headers=headers)
    check_resp(resp)
    headers["Content-Type"] = "application/json"

patch(url="%s/v1/csm/cases/%s/requested" % (url, case_id), headers=headers)
check_resp(resp)
print("case_id=%s" % case_id)
exit(0)
# print("ok")
