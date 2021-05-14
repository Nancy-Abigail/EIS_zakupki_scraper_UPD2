from main import read_page, count_pages
from lov import days_2018, days_2019, days_2020, request_header, days_2019_may, days_2020_dec
import re
import requests
from lxml import html

full_days_list = days_2018 + days_2019 + days_2020
# full_days_list = days_2020_dec

cities = {
    # 94124: {
    #         'name': 'Калуга',
    #         'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277323&oktmoIds=94122&oktmoIdsCodes=29+701+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    #         },
    #
    # 188578: {
    #         'name': 'Чита',
    #         'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277394&oktmoIds=188576&oktmoIdsCodes=76+701+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    #         },
    #
    # 43839: {
    #         'name': 'Архангельск',
    #         'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277339&oktmoIds=43837&oktmoIdsCodes=11+701+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    #         },
    #
    # 53050: {
    #         'name': 'Владимир',
    #         'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277320&customerPlaceCodes=33000000000&oktmoIds=53048&oktmoIdsCodes=17701000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    #         },
    #
    # 46831: {
    #         'name': 'Белгород',
    #         'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277318&oktmoIds=46829&oktmoIdsCodes=14+701+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    #         },
    #
    # 50273: {
    #         'name': 'Брянск',
    #         'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277319&customerPlaceCodes=32000000000&oktmoIds=50271&oktmoIdsCodes=15701000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    #         },
    #
    # 76091: {
    #         'name': 'Иваново',
    #         'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277322&oktmoIds=76089&oktmoIdsCodes=24+701+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    #         },
    #
    # 90329: {
    #         'name': 'Тверь',
    #         'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277332&customerPlaceCodes=69000000000&oktmoIds=90327&oktmoIdsCodes=28701000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    #         },
    #
    # 37196: {
    #         'name': 'Ставрополь',
    #         'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277354&oktmoIds=37194&oktmoIdsCodes=07+701+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    #         },
    #
    202996: {
            'name': 'Улан-Удэ',
            'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277397&customerPlaceCodes=03000000000&oktmoIds=202994&oktmoIdsCodes=81701000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
            },

    183618: {
        'name': 'Салехард',
        'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277382&oktmoIds=183616&oktmoIdsCodes=71+951+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    },

    188767: {
        'name': 'Анадырь',
        'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277408&customerPlaceCodes=87000000000&oktmoIds=188765&oktmoIdsCodes=77701000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    },

    78625: {
        'name': 'Магас',
        'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277350&oktmoIds=78623&oktmoIdsCodes=26+701+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    },

    43966: {
        'name': 'Нарьян-Мар',
        'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&oktmoIds=43966&oktmoIdsCodes=11851000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    },

    207051: {
        'name': 'Горно-Алтайск',
        'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&oktmoIds=207049&oktmoIdsCodes=84+701+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    },

    228334: {
        'name': 'Биробиджан',
        'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277407&oktmoIds=228332&oktmoIdsCodes=99+701+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    },

    118718: {
        'name': 'Магадан',
        'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277405&oktmoIds=118716&oktmoIdsCodes=44+701+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    },

    114100: {
        'name': 'Гатчина',
        'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277342&customerPlaceCodes=47000000000&oktmoIds=114100&oktmoIdsCodes=41618101&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
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
