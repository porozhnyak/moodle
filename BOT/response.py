import requests
from fake_useragent import UserAgent
import time
from bs4 import BeautifulSoup
import datetime
import GetLessonsLink
# from config_act import user_login, user_passwor


URL = "https://distant.donnuet.ru" 
log_url = URL+"/login/index.php"
profile_link = "https://distant.donnuet.ru/my/"


#Заголовки
ua = UserAgent()
rand_ua = ua.random
headers = {
    "User-Agent": rand_ua
}


session = requests.Session()
session2 = requests.Session()

today = datetime.datetime.today().isoweekday()# Выводит номер дня недели (1-Понедельник ... 7-Воскресенье)
TimeNow = datetime.datetime.today().strftime('%H:%M')

def login(user_login, user_password):
    session.headers.update(headers)

    res = session.get(log_url)
    soup = BeautifulSoup(res.content, 'html.parser')

    data = {
        'anchor': '',
        'logintoken': soup.find('input', {"name": "logintoken"}).get("value"),
        "username" : user_login,
        "password" : user_password,
    }
    
    session.post(log_url, data=data, headers=headers)
    

 

def profile():

    cookies_dict = [
        {"domain": key.domain, "name": key.name, "path": key.path, "value": key.value}
        for key in session.cookies
    ]

    for cookies in cookies_dict:
        session2.cookies.set(**cookies)

    profile_response = session2.get(profile_link, headers=headers)


    # f = open('results.html', 'w', encoding='utf8')
    # f.write(profile.text)
    # f.close()

    return profile_response

def get_profile(user_login, user_password):
    try:
        
        session = login(user_login, user_password)
        # prof = profile()
        profile_response = profile()
        
        soup = BeautifulSoup(profile_response.text, 'html.parser')
        unlog = soup.find('span', class_ = 'login') #Переменная отвечающая за вход в систему, если есть, то бот не вошёл в систему
        log = soup.find('span', class_ = "usertext mr-1").text


        return f"Твой аккаунт {log}?"
    except Exception as e:
        return f"Ошибка логина: {e}"
            
def resless(): #запросы на уроки
    try:
        # today = datetime.datetime.today().isoweekday()# Выводит номер дня недели (1-Понедельник ... 7-Воскресенье)
        # TimeNow = datetime.datetime.today().strftime('%H:%M')


        link = GetLessonsLink.GetLessonsLink(today, TimeNow)
        res =  session2.get(link, headers=headers)

        if link is None:
            pass
        else: 
            res

        soup = BeautifulSoup(res.text, 'html.parser')
        name_course = soup.find('div', class_ = 'page-header-headings').text
        name_user = soup.find('span', class_ = 'usertext mr-1').text


 
        return f"Бот-аккаунт {name_user} на курсе : {name_course} "
        # return name_user
    except:
        pass
    # except Exception as e:
    #     if e is not None:
    #         return f'Ошибка: {e}'
    #     else:   
    #         pass

    




# def req_answ():
#     get_profile(user_login, user_password)
#     print(resless())

# req_answ()