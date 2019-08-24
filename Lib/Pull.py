import requests
import re
API_IP = '127.0.0.1'
# proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}


"""
Returns json

Examples:
Jdata = pull('Domains')
"""
def pull(endpoint):
    r = requests.get('http://'+API_IP+':1337/'+endpoint,  verify=False)
    data = r.json()
    return(data)

"""
This function takes an element (Which should be a list of a dic = {IP:value,ID:value,Ste:value,Data:value,Type:value})
and returns the value of Data (Data:value).

"""
def getDataFromJson(element):
    for key, value in element.items():
        if key == 'Data':
            return value
"""
The same as /\ /\ /\ /\

Gets the IP of who sent the data.
"""
def getIPFromJson(element):
    for key, value in element.items():
        if key == 'IP':
            return value

"""
The same as /\ /\ /\ /\

Gets the Site/URL of the POST req sent.
"""
def getSiteFromJson(element):
    for key, value in element.items():
        if key == 'Site':
            return value

"""
The same as /\ /\ /\ /\

Gets the type of the POST req sent.
"""
def getTypeFromJson(element):
    for key, value in element.items():
        if key == 'Type':
            return value

def getIt(url, cookies = '', headers = ''):
    headers = {'Authorization': 'Authorization'}
    cookies = {'enwiki_session': '17ab96bd8ffbe8ca58a78657a918558'}
    # , proxies=proxies
    proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
    r = requests.get(url, cookies=cookies,  headers=headers, verify=False)


def postIt(url, cookies = '', headers = ''):
    headers = {'Authorization': 'Authorization'}
    cookies = {'enwiki_session': '17ab96bd8ffbe8ca58a78657a918558'}
    data = ''
    r = requests.post(url, data, cookies=cookies,  headers=headers, verify=False)
    return r

#VMware_ESXI_Add_Admin('192.168.0.18')
def test_AddVM_User_Example():
    ip = '192.168.0.18'
    username = 'TestUUUUSER'
    password = 'Liverpool!1!1!'
    description = 'Description1'
    Execute_VMware_ESXI(ip,'Add_Admin', username, password, description)

if __name__ == '__main__':
    test_AddVM_User_Example('192.168.0.18')

