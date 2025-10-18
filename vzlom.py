# @SuperDragon777

import urllib.request as king # он тут главный (типо король)
import socket # этот шедевр для локального айпи
import ssl # это для сертификатов, которые я ненавижу
from time import sleep as wait # типо чтобы подождать

def de_print(text, delay=0.07): # красивый принт
    for char in text:
        print(char, end='', flush=True)
        wait(delay)
    print()

def red(text):
    color = "\033[31m{}"
    output = color.format(text)
    return output

def no_style():
    color = "\033[0m{}"
    output = color.format("")
    print(output, end="")

def bold(text):
    color = "\033[1m{}"
    output = color.format(text)
    return output

def underline(text):
    color = "\033[4m{}"
    output = color.format(text)
    return output

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
        print("\n\n")
    else:
        de_print(bold(red("не удалось определить :(")), 0.05)
        print("\nВозможные причины:")
        print("• Ты, гений, выключил интернет")
        print("• SSL-сертификаты сегодня на каникулах")
        print("• Твой антивирус встал не с той ноги")
