from main import read_page, count_pages
from lov import days_2018, days_2019, days_2020, request_header, days_2019_may, days_2020_dec
import re
import requests
from lxml import html

full_days_list = days_2018 + days_2019 + days_2020
# full_days_list = days_2020_dec

cities = {
    # 224198: {
    #         'name': 'Грозный',
    #         'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277358&oktmoIds=224196&oktmoIdsCodes=96+701+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    #         },
    #
    # 176330: {
    #         'name': 'Тамбов',
    #         'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277331&customerPlaceCodes=68000000000&oktmoIds=176328&oktmoIdsCodes=68701000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    #         },
    #
    # 125781: {
    #         'name': 'Мурманск',
    #         'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277343&oktmoIds=125779&oktmoIdsCodes=47+701+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    #         },
    #
    # 228135: {
    #         'name': 'Якутск',
    #         'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277400&customerPlaceCodes=14000000000&oktmoIds=228135&oktmoIdsCodes=98701000001&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    #         },
    #
    # 214296: {
    #         'name': 'Владикавказ',
    #         'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277359&oktmoIds=214294&oktmoIdsCodes=90+701+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    #         },
    #
    # 213833: {
    #         'name': 'Саранск',
    #         'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277365&customerPlaceCodes=13000000000&oktmoIds=213831&oktmoIdsCodes=89701000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    #         },
    #
    # 64218: {
    #         'name': 'Вологда',
    #         'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277340&oktmoIds=64216&oktmoIdsCodes=19+701+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    #         },
    #
    # 141284: {
    #         'name': 'Орёл',
    #         'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277328&customerPlaceCodes=57000000000&oktmoIds=141282&oktmoIdsCodes=54701000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    #         },
    #
    # 109191: {
    #         'name': 'Курган',
    #         'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277378&oktmoIds=107028&oktmoIdsCodes=37+000+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    #         },
    #
    # 174062: {
    #         'name': 'Смоленск',
    #         'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277330&customerPlaceCodes=67000000000&oktmoIds=174060&oktmoIdsCodes=66701000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    #         },
    #
    183375: {
        'name': 'Ханты-Мансийск',
        'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277381&oktmoIds=183373&oktmoIdsCodes=71+871+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    },

    125614: {
        'name': 'Химки',
        'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277327&oktmoIds=125612&oktmoIdsCodes=46+783+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    },

    31720: {
        'name': 'Новороссийск',
        'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277353&oktmoIds=31718&oktmoIdsCodes=03+720+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    },

    183386: {
        'name': 'Нижневартовск',
        'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277381&customerPlaceCodes=86000000000&oktmoIds=183386&oktmoIdsCodes=71875000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    },

    201767: {
        'name': 'Стерлитамак',
        'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277363&customerPlaceCodes=02000000000&oktmoIds=201765&oktmoIdsCodes=80745000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    },

    125568: {
        'name': 'Подольск',
        'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277327&customerPlaceCodes=50000000000&oktmoIds=125566&oktmoIdsCodes=46760000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    },

    64222: {
        'name': 'Череповец',
        'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277340&oktmoIds=64220&oktmoIdsCodes=19+730+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    },

    55502: {
        'name': 'Волжский',
        'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&selectedContractDataChanges=ANY&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277356&customerPlaceCodes=34000000000&oktmoIds=55496&oktmoIdsCodes=18+700+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&countryRegIdNameHidden=%7B%7D&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
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
