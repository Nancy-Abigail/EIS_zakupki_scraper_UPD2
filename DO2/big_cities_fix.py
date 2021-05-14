from main import read_page, count_pages
from lov import days_2018, days_2019, days_2020, request_header, days_2019_may, days_2020_dec
import re
import requests
from lxml import html

full_days_list = days_2018 + days_2019 + days_2020
# full_days_list = days_2020_dec

cities = {
    # 39403: {
    #         'name': 'Благовещенск',
    #         'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277403&oktmoIds=39401&oktmoIdsCodes=10+701+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    #         },
    # 
    # 206584: {
    #         'name': 'Нальчик',
    #         'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277351&customerPlaceCodes=07000000000&oktmoIds=206582&oktmoIdsCodes=83701000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    #         },
    # 
    # 209763: {
    #         'name': 'Сыктывкар',
    #         'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277338&oktmoIds=209761&oktmoIdsCodes=87+701+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    #         },
    # 
    # 55499: {
    #         'name': 'Волгоград',
    #         'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277356&oktmoIds=55497&oktmoIdsCodes=18+701+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    #         },

    66976: {
            'name': 'Воронеж',
            'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277321&oktmoIds=66974&oktmoIdsCodes=20+701+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
            },
            
    146914: {
            'name': 'Пермь',
            'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277321&oktmoIds=66974&oktmoIdsCodes=20+701+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
            },
            
    34710: {
            'name': 'Красноярск',
            'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277398&customerPlaceCodes=24000000000&oktmoIds=34708&oktmoIdsCodes=04701000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
            },
            
    201707: {
            'name': 'Уфа',
            'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277363&oktmoIds=201705&oktmoIdsCodes=80+701+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
            },
            
    159821: {
            'name': 'Ростов-на-Дону',
            'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277357&oktmoIds=156617&oktmoIdsCodes=60+000+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
            },
            
    106979: {
            'name': 'Самара',
            'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277374&customerPlaceCodes=63000000000&oktmoIds=106977&oktmoIdsCodes=36701000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
            },

}


# noinspection PyBroadException
def read_all_cities():
    for city_oktmo in cities.keys():
        for day in full_days_list:
            try:
                read_all_pages(city_oktmo, day)
            except Exception as e:
                print(f'Error at: Read all pages, oktmo={city_oktmo}, day={day}: {e}')

            try:
                print(
                    f'Day done! City: {cities[city_oktmo]["name"]}, day: {day}'
                )
            except:
                pass


def read_all_pages(city_oktmo, day):
    link = get_link(city_oktmo, day, page=1)
    request = requests.get(link, headers=request_header)
    html_page = html.fromstring(request.content)

    try:
        # Read first page
        read_page(html_page, city_oktmo)
    except Exception as e:
        print(f'Exception at oktmo={city_oktmo}, day={day}, page={1}:', e)

    # Check if there are other pages and read them
    pages_amount = count_pages(html_page)

    for page in range(2, pages_amount + 1):
        link = get_link(city_oktmo, day, page)
        request = requests.get(link, headers=request_header)
        html_page = html.fromstring(request.content)

        try:
            read_page(html_page, city_oktmo)
        except Exception  as e:
            print(f'Exception at oktmo={city_oktmo}, day={day}, page={page}:', e)


def get_link(city_oktmo, day, page):
    link = cities[city_oktmo]['link']
    link = re.sub(r'contractDateFrom=[0-9.]{10}', f'contractDateFrom={day}', link, 1)
    link = re.sub(r'contractDateTo=[0-9.]{10}', f'contractDateTo={day}', link, 1)
    link = re.sub(r'executionDateStart=[0-9.]{10}', f'executionDateStart=01.01.{day[-4:]}', link, 1)
    link = re.sub(r'executionDateEnd=[0-9.]{10}', f'executionDateEnd=31.12.{day[-4:]}', link, 1)
    link = re.sub(r'pageNumber=[0-9]+', f'pageNumber={page}', link, 1)

    print(link)

    return link


if __name__ == '__main__':
    read_all_cities()
