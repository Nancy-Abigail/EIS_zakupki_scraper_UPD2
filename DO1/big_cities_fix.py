from main import read_page, count_pages
from lov import days_2018, days_2019, days_2020, request_header, days_2019_may, days_2020_dec
import re
import requests
from lxml import html

full_days_list = days_2018 + days_2019 + days_2020
# full_days_list = days_2020_dec

cities = {
    # 207573: {
    #     'name': 'Элиста',
    #     'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277360&customerPlaceCodes=08000000000&oktmoIds=207573&oktmoIdsCodes=85701000001&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    # },
    # 220199: {
    #     'name': 'Кызыл',
    #     'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277386&oktmoIds=220197&oktmoIdsCodes=93+701+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    # },
    # 214651: {
    #     'name': 'Черкесск',
    #     'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277352&customerPlaceCodes=09000000000&oktmoIds=214651&oktmoIdsCodes=91701000001&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    # },
    # 195390: {
    #     'name': 'Майкоп',
    #     'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277349&oktmoIds=195388&oktmoIdsCodes=79+701+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    # },
    # 245830: {
    #     'name': 'Красногорск',
    #     'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277327&customerPlaceCodes=50000000000&oktmoIds=245828&oktmoIdsCodes=46744000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    # },
    # 223336: {
    #     'name': 'Абакан',
    #     'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277387&customerPlaceCodes=19000000000&oktmoIds=223334&oktmoIdsCodes=95701000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    # },
    # 94349: {
    #     'name': 'Петропавловск-Камчатский',
    #     'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277404&customerPlaceCodes=41000000000&oktmoIds=94347&oktmoIdsCodes=30701000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    # },
    # 166085: {
    #     'name': 'Южно-Сахалинск',
    #     'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277406&customerPlaceCodes=65000000000&oktmoIds=166083&oktmoIdsCodes=64701000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    # },
    # 156613: {
    #     'name': 'Псков',
    #     'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277344&oktmoIds=156611&oktmoIdsCodes=58+701+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    # },
    # 129910: {
    #     'name': 'Великий Новгород',
    #     'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277346&oktmoIds=129908&oktmoIdsCodes=49+701+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    # },
    186853: {
        'name': 'Магнитогорск',
        'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277380&oktmoIds=186851&oktmoIdsCodes=75+738+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    },
    125357: {
        'name': 'Балашиха',
        'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277327&oktmoIds=125355&oktmoIdsCodes=46+704+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    },
    219758: {
        'name': 'Набережные Челны',
        'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277366&oktmoIds=219756&oktmoIdsCodes=92+730+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    },
    95999: {
        'name': 'Новокузнецк',
        'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277390&customerPlaceCodes=42000000000&oktmoIds=95997&oktmoIdsCodes=32731000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    },
    107023: {
        'name': 'Тольятти',
        'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277374&oktmoIds=107021&oktmoIdsCodes=36+740+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    },
    183391: {
        'name': 'Сургут',
        'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277381&oktmoIds=183389&oktmoIdsCodes=71+876+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    },
    168130: {
        'name': 'Нижний Тагил',
        'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277383&oktmoIds=168128&oktmoIdsCodes=65+751+000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
    },
    31747: {
        'name': 'Сочи',
        'link': 'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&customerPlace=5277353&customerPlaceCodes=23000000000&oktmoIds=31745&oktmoIdsCodes=03726000&contractDateFrom=01.01.2018&contractDateTo=01.01.2019&executionDateStart=01.01.2018&executionDateEnd=31.12.2018&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false'
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
