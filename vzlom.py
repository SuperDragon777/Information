# @SuperDragon777

import urllib.request as king # он тут главный (типо король)
import socket # этот шедевр для локального айпи
import ssl # это для сертификатов, которые я ненавижу
from time import sleep as wait # типо чтобы подождать
import json # его пригласили чтоб с json работал

def de_print(text, delay=0.07): # красивый принт
    for char in text:
        print(char, end='', flush=True)
        wait(delay)
    print()

def red(text): # красный текст
    color = "\033[31m{}"
    output = color.format(text)
    return output

def no_style(): # обычный текст
    color = "\033[0m{}"
    output = color.format("")
    print(output, end="")

def bold(text): # жирный текст
    color = "\033[1m{}"
    output = color.format(text)
    return output

def underline(text): # подчеркнутый текст
    color = "\033[4m{}"
    output = color.format(text)
    return output

def important(text): # красный + жирный
    text = bold(text)
    text = red(text)
    return(text)

def get_location_info(ip):
    def get_ip_info(ip):
        socket.inet_aton(ip)
        url = f"http://ipapi.co/{ip}/json/"
            
        with king.urlopen(url) as response:
            data = json.loads(response.read().decode())
            
        return data
    
    data = get_ip_info(ip) # получаю данные
    
    info_lines = [ # задаю каждую линия
        f"Cтрана - {important(data.get('country_name', 'Неизвестно'))}",
        f"Код страны - {important(data.get('country_code', 'Неизвестно'))}",
        f"Город - {important(data.get('city', 'Неизвестно'))}",
        f"Регион - {important(data.get('region', 'Неизвестно'))}",
        f"Провайдер - {important(data.get('org', 'Неизвестно'))}",
        f"Часовой пояс - {important(data.get('timezone', 'Неизвестно'))}",
        f"Широта - {important(data.get('latitude', 'Неизвестно'))}",
        f"Долгота - {important(data.get('longitude', 'Неизвестно'))}"
    ]
    
    for line in info_lines: # печатаю каждую линия
        de_print(line, 0.04)
        no_style()

def get_public_ip(): 
    http_services = [
        'http://api.ipify.org',
        'http://ident.me', 
        'http://checkip.amazonaws.com',
        'http://icanhazip.com',
        'http://ifconfig.me/ip'
    ]
    
    for attempt, service in enumerate(http_services, 1):  # начинаю с 1
        try:
            de_print(f"попытка определения {attempt} из {len(http_services)}", 0.05)
            # print(f"service - {service}")
            with king.urlopen(service, timeout=5) as response:
                ip = response.read().decode('utf-8').strip()
                if is_valid_ip(ip):
                    return ip, service # возвращаю данные
        except Exception: # чтобы не было ошибки
            de_print(bold(red("Неудачно")), 0.05)
            no_style()
            continue
    
    """ дальше полное безумие с сертификатами """
    https_services = [
        'https://api.ipify.org',
        'https://ident.me',
        'https://checkip.amazonaws.com'
    ]
    
    ssl_context = ssl.create_default_context() # создаю пример ssl
    ssl_context.check_hostname = False # говорю не делать проверку соответствия
    ssl_context.verify_mode = ssl.CERT_NONE # режим проверки: не проверять
    
    for attempt, service in enumerate(https_services, 1):  # начинаю с 1
        try:
            de_print(f"попытка определения {attempt} из {len(https_services)}", 0.05)
            # print(f"service - {service}")
            with king.urlopen(service, timeout=5, context=ssl_context) as response:
                ip = response.read().decode('utf-8').strip()
                if is_valid_ip(ip):
                    return ip, service + " (без проверки ненавистного сертификата SSL)" # возвращаю данные
        except Exception: # чтобы не было ошибки
            de_print(bold(red("Неудачно")), 0.05)
            no_style()
            continue
    
    return None, None
    """ безумие с сертификатами закончилось, ура """
    
def is_valid_ip(ip): # проверка на то что это айпи, а не хитро замаскированный арбуз
    try:
        parts = ip.split('.')
        if len(parts) != 4: # типо 4 части
            return False
        for part in parts:
            num = int(part)
            if num < 0 or num > 255: # вы когда-то видели такой айпи: 999.999.999.999
                return False
        return True
    except:
        return False # если все же арбуз

def get_local_ip():
    try:
        # создаю временное соединение
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("ya.ru", 80))
            return s.getsockname()[0]
    except:
        return "не удалось определить :("

if __name__ == "__main__":
    no_style()
    print("\n")
    print((underline(" ") * 50))
    no_style()
    de_print("определяю локальный айпи...", 0.07)
    no_style()
    wait(1)
    
    
    local_ip = get_local_ip()
    de_print("твой локальный айпи:", 0.05)
    no_style()
    de_print(bold(red(f"{local_ip}")), 0.05)
    no_style()
    
    
    de_print("\nопределяю публичный айпи...", 0.07)
    wait(1)
    public_ip, source = get_public_ip()
    
    if public_ip:
        de_print(f"твой публичный айпи:", 0.05)
        de_print(bold(red(f"{public_ip}")), 0.05)
        no_style()
        de_print(f"определил с помощью: {source}", 0.05)
        print(underline(" " * 50))
        no_style()
        print("\n")
        get_location_info(public_ip)
        print(underline(" " * 50))
        no_style()
        print("\n\n")
        
    else:
        de_print(bold(red("не удалось определить :(")), 0.05)
        print("\nВозможные причины:")
        print("• Ты, гений, выключил интернет")
        print("• SSL-сертификаты сегодня на каникулах")
        print("• Твой антивирус встал не с той ноги")
