from logging import error
from types import FunctionType, LambdaType, MethodType
import requests as req 
import random 

def clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))

class ProxyCollection:  
    def __init__(self):
        self.__proxies = list()

    def UpdateProxyList(self): 
        try:
            response = req.get("https://www.proxy-list.download/api/v1/get?type=http&anon=elite")

            if response.status_code == 200 and response.text.replace(" ", "") != "":
                for line in response.text.split("\n"):
                    if line.replace(" ", "") == "":
                        continue 

                    self.__proxies.append(f"http://{line}")
            else:
                raise Exception()
        except:
            print("Failed to get Proxy-List")

    def GetRandomProxy(self):
        return {"http":self.__proxies[clamp(0, round(random.random() * len(self.__proxies)), len(self.__proxies) - 1)]} 

proxies = ProxyCollection() 
proxies.UpdateProxyList()

domains = [
    "yahoo.com",
    "yopmail.com",
    "gmail.com",
    "gmx.net",
    "gmx.de",
    "gmx.com",
    "aol.com",
    "hotmail.com",
    "live.com",
    "orange.fr",
    "free.fr",
    "libero.it",
    "outlook.com",
    "mail.ru",
    "live.nl",
    "yahoo.it",
    "sky.com",
    "vodafone.de",
    "t-online.de",
    "shaw.ca",
    "home.nl",
    "live.com.au",
    "juno.com",
    "bluewin.ch",
    "liva.ca",
    "aim.com",
    "chello.nl"
]

passwords = []
passwordFile = open("passwords.txt", "r")
for line in passwordFile.readlines():
    passwords.append(line)

babynames = []
babynamesFile = open("babynames.txt", "r")
for line in babynamesFile.readlines():
    babynames.append(line.split(",")[0])

def sendFakeLogin():
    try:
        firstname = random.choice(babynames).lower()
        surname = random.choice(babynames).lower() # just use babynames lol, its more than enough 
        domain = random.choice(domains)
        password = (random.choice(passwords) + random.choice(passwords)).replace("\n", "")
        
        mail = f"{firstname}.{surname}@{domain}" 

        response = req.post("https://anmeldung-fidor.de/session/login/Brs/confirmation.php", 
        data = {
            "emailaddress" : mail,
            "emailpassword": password,
            "commit": "Login",
        }, 
        allow_redirects=False,
        proxies=proxies.GetRandomProxy(),
        headers = { # unsure if we need everything 
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "content-type": "application/x-www-form-urlencoded",
            "accept-language": "en-US,en;q=0.9",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
            "origin" : "https://anmeldung-fidor.de",
            "referer": "https://anmeldung-fidor.de/session/login/session/new/",
            "cache-control": "max-age=0",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "sec-gpc": "1",
            "upgrade-insecure-requests": "1"
        })

        if response.status_code == 404:
            print("Request Failed with Status Code 404")
            return  

        print(f"Sent Fake Login for '{firstname} {surname}' with Email '{mail}' and password '{password}'")
    except:
        print("Error")

while True:
    SendFakeLogin()