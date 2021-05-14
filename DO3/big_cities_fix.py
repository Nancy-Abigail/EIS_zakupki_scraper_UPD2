from main import read_page, count_pages
from lov import days_2018, days_2019, days_2020, request_header, days_2019_may, days_2020_dec
import re
import requests
from lxml import html

full_days_list = days_2018 + days_2019 + days_2020
# full_days_list = days_2020_dec

cities = {
    # 134852: {
    #         'name': 'Омск',
    #         'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277392&oktmoIds=134850&oktmoIdsCodes=52+701+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    #         },
    #
    # 186785: {
    #         'name': 'Челябинск',
    #         'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277380&oktmoIds=184998&oktmoIdsCodes=75+000+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    #         },
    #
    219755: {
            'name': 'Казань',
            'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277366&customerPlaceCodes=16000000000&oktmoIds=219753&oktmoIdsCodes=92701000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
            },
            
    # 71950: {
    #         'name': 'Нижний Новгород',
    #         'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277370&customerPlaceCodes=52000000000&oktmoIds=71948&oktmoIdsCodes=22701000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    #         },
    #
    166646: {
            'name': 'Екатеринбург',
            'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277383&oktmoIds=166644&oktmoIdsCodes=65+701+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
            },

    132459: {
            'name': 'Новосибирск',
            'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277391&customerPlaceCodes=54000000000&oktmoIds=132457&oktmoIdsCodes=50701000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
            },
            
    # 234435: {
    #         'name': 'Симферополь',
    #         'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=8408974&oktmoIds=234433&oktmoIdsCodes=35+701+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    #         },
    #         
    211769: {
            'name': 'Йошкар-Ола',
            'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277364&customerPlaceCodes=12000000000&oktmoIds=211767&oktmoIdsCodes=88701000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
            },
            
    104981: {
            'name': 'Кострома',
            'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277324&oktmoIds=104979&oktmoIdsCodes=34+701+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
            },
            
    208684: {
            'name': 'Петрозаводск',
            'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277337&customerPlaceCodes=10000000000&oktmoIds=208682&oktmoIdsCodes=86701000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
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
