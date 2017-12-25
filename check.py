import requests
import getpass
import time
import random
from bs4 import BeautifulSoup
# pylint: disable=C0103

session = requests.Session()

def login(payload):
    """print welcome message"""
    memText = session.post('https://std.regis.ku.ac.th/_Login.php', data=payload)
    soup = BeautifulSoup(memText.text, 'lxml')
    name = soup.find('tr', id='3')
    if len(name) == 0:
        print("login fail")
        return False
    
    name = name.findAll('td')[1].contents[0]
    print("Welcome " + name + ".")
    return True

def get_ku20():
    """get grade data"""
    attr = {'mode':'KU20'}
    headers = {'Referer': 'https://std.regis.ku.ac.th/_Student_Registration.php',
               'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101'}
    regis = session.get('https://std.regis.ku.ac.th/_Student_RptKu.php?', params=attr,
                        headers=headers)
    soup = BeautifulSoup(regis.text, 'lxml')
    return soup.findAll('table')[3]

def main():
    """main"""
    usr = input('input your id: ')
    pw = getpass.getpass('password: ')
    payload = {'form_username':usr, 'form_password':pw, 'zone':'0'}
    
    if not login(payload):
        return
    
    first = get_ku20()
    # check for update
    while True:
        # random refresh time
        for x in range(random.randint(300, 600), 0, -1):
            if x % 60 == 0:
                print('remain.. {0} minute(s) until next update'.format(int(x / 60)))
            time.sleep(1)
            
        now = get_ku20()
        
        td = now.findAll('td', class_='head_sm')
        if len(td) == 0:
            print("program ended")
            return
        if now != first:
            print("grade updated!")
            break
        else:
            print("keep calm")

if __name__ == "__main__":
    main()
