import json

import fake_useragent
import requests
from os import system
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import lxml

url = "https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=9999&view=BTBiographyList"

ua = fake_useragent.UserAgent()
headers = {
    "User-Agent": ua.random
}


# Записываем страницу с членами совета в файл
def recording():
    req = requests.get(url, headers)
    page = req.content
    soup = BeautifulSoup(page, 'lxml')
    with open('members.html', 'w', encoding='utf-8') as file:
        file.write(str(soup))


# Запись страницы с ссылками на членов совета из html-файла
def html_to_href():
    hrefs = []
    # Запись файла с тегами а - ссылками на членов совета
    with open('members.html', encoding='utf-8') as file:
        page = BeautifulSoup(file, 'lxml')
    a_list = page.find_all('a')
    for a in a_list:
        hrefs.append(a.get('href'))
    # Запись файла с ссылками из тегов а
    with open('members.txt', 'w', encoding='utf-8') as file:
        for href in hrefs:
            file.write(f'{href}\n')


# Достаём необходимые данные по ссылкам из файла
def parser():
    with open('members.txt', encoding='utf-8') as file:
        a_list = file.read().split()
        data_dict = []
        counter = 0

        # Проходимся по каждой ссылке из txt - файла
        for a in a_list:
            req = requests.get(a, headers)
            page = req.content
            soup = BeautifulSoup(page, 'lxml')

            # Имя / Партия

            person = soup.find(class_='bt-biografie-name').find('h3').text.strip()
            person_name_company = person.split(',')
            person_name = person_name_company[0]
            person_company = person_name_company[1]

            # Социальные сети

            person_social = []
            social_links = soup.find(class_='bt-linkliste').find_all('a')
            for link in social_links:
                person_social.append(link.get('href'))

            # Объединяем всю информацию

            data = {
                'person_name': person_name,
                'person_company': person_company,
                'person_social': person_social
            }

            # Вывод счётчика в консоли

            counter += 1
            system('cls')
            print(f'Парсинг в процессе {counter}/{len(a_list)}')

            data_dict.append(data)

        # Записываем список с информацией в JSON - файл

        with open('members.json', 'w', encoding='utf-8') as file:
            json.dump(data_dict, file, indent=4)


def main():
    # recording()
    # html_to_href()
    parser()
    print('Парсинг успешно выполнен! Файл записан.')


if __name__ == '__main__':
    main()
