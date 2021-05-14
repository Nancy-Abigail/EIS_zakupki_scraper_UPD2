from lov import oktmo_IDS, days_2020, days_2019, days_2018, request_header, oktmo_to_city_name, oktmo_todo
from lxml import html
from orm import Contract, Client, Contractor, Item
from orm import new_session, Session
import threading
import re
import requests


def log_error(type: str, **kwargs):
    # Fill error log row
    row = '{'
    row += f'"type":"{type}"'
    for key, value in kwargs.items():
        row += f',"{key}":"{value}"'
    row += '}\n'

    # Add row to log file
    with open('error_log.txt', 'a+') as file:
        file.write(row)


def read_contract(general_contract_page: html.HtmlElement, contract_id: int, session: Session) -> Contract:

    # Read contract details
    contract_info_block = general_contract_page.xpath('//div[@class="cardMainInfo__section"]')
    contract_info_details = {}
    for object in contract_info_block:
        key = object.xpath('.//span[@class="cardMainInfo__title"]|.//div[@class="cardMainInfo__title"]')[0].text
        value = object.xpath('.//span[@class="cardMainInfo__content"]|.//div[@class="cardMainInfo__content"]')[
            0].text_content().strip(' \n')
        contract_info_details[key] = value

    # Get contract dates
    contract_date = contract_info_details['Заключение контракта']
    execution_date = contract_info_details['Срок исполнения']

    # Get contract price
    contract_price = general_contract_page.xpath('.//div[@class="price"]//span[@class="cardMainInfo__content cost"]')[0]. \
        text_content()
    contract_price = re.sub('[^0-9,]', '', contract_price)
    contract_price = re.sub(',', '.', contract_price)
    contract_price = float(contract_price)

    # Create contract and push it to DB
    contract = Contract(
        registry_number=contract_id,
        contract_date=contract_date,
        execution_date=execution_date,
        contract_price=contract_price
    )
    contract = contract.push(session)

    return contract


def read_client(general_contract_page: html.HtmlElement, contract: Contract, oktmo_code, session: Session):
    # Get container with client info
    client_info_container = get_container_by_name(general_contract_page, 'Информация о заказчике')

    client_info_general = client_info_container.xpath('.//section[@class="blockInfo__section section"]')
    client_info = {}

    for object in client_info_general:
        key = object.xpath('.//span[@class="section__title"]')[0].text_content()
        value = object.xpath('.//span[@class="section__info"]')[0].text_content()
        client_info[key] = value

    client_name = client_info['Полное наименование заказчика'].strip(' \n')
    client_inn = client_info['ИНН']
    client_city_oktmo = int(oktmo_code)

    # Create the client, add it to DB, connect it with the contract
    client = Client(inn=client_inn, name=client_name, city_oktmo=client_city_oktmo)
    client = client.push(session)
    contract.client = client

    return contract.client


def read_contractors(general_contract_page: html.HtmlElement, contract: Contract, session: Session):
    # Get container with client info
    contractors_info_container = get_container_by_name(general_contract_page, 'Информация о поставщиках')

    # Get headers of table
    keys_list = []
    key_blocks = contractors_info_container.xpath('.//thead//th[@class="tableBlock__col tableBlock__col_header"]')

    for key_block in key_blocks:
        key = key_block.text_content().strip(' \n')
        keys_list.append(key)

    # Get all contractors properties to lists
    contractors_info = []
    contractors_rows = contractors_info_container.xpath('.//tbody//tr[@class="tableBlock__row"]')

    for row in contractors_rows:  # Read row for each contractor
        contractor_info_list = []
        contractor_cells = row.xpath('./td')

        for cell in contractor_cells:  # Read all cells text and additional info if exists
            block = {'text': cell.text.strip(' \n')}
            additional_sections = cell.xpath('./section')

            for section in additional_sections:
                key = section.xpath('./span[@class="grey-main-light"]')[0].text_content().strip(' \n:')
                value = section.xpath('./span[@class!="grey-main-light" or not(@class)]')[0].text_content().strip(' \n')

                block[key] = value

            contractor_info_list.append(block)

        # Match table headers with contractors property blocks
        contractor_info_dict = dict(zip(keys_list, contractor_info_list))
        contractors_info.append(contractor_info_dict)

    # Create contractors, push them to db and link with contract
    contractors = []

    for contractor_info in contractors_info:
        contractor = Contractor()
        contractor.inn = int(contractor_info['Организация']['ИНН'])
        contractor.name = contractor_info['Организация']['text']
        contractor.full_address = contractor_info['Адрес места нахождения']['text']

        contractor = contractor.push(session)
        contractors.append(contractor)

    contract.contractors = contractors
    return contract.contractors


# noinspection PyBroadException
def read_items(target_of_order_page: html.HtmlElement, contract: Contract, session: Session):
    # Get items container
    items_container = target_of_order_page.xpath('//div[@class="container" and @id="contractSubjects"]')[0]

    # Get headers
    keys_list = []
    keys_blocks = items_container.xpath('.//table[@id="contract_subjects"]/thead/tr/th')[1:]

    for key_block in keys_blocks:
        key = key_block.text_content().strip(' \n')
        keys_list.append(key)

    # Get items data
    items_info = []
    items_rows = items_container.xpath('.//table[@id="contract_subjects"]/tbody/tr[@class="tableBlock__row "]')

    for item_row in items_rows:  # Read row for each item
        # Fill info from table
        item_blocks = item_row.xpath('./td')[1:]
        item_info = dict(zip(keys_list, item_blocks))

        items_info.append(item_info)

    # Clear items in contract before appending
    contract.clear_items(session)

    # Create items, add to database
    for item_info in items_info:
        item = Item()

        # Extract parameters
        item.contract_number = contract.registry_number
        item.okpd_code = int(
            re.findall(
                r'\([0-9]{2}(?:\.[0-9]+){1,3}\)',
                item_info['Позиции по КТРУ, ОКПД2'].text_content()
            )[-1][1:3]
        )
        item.name = re.sub(
            r'\([0-9]{2}(?:\.[0-9]+){1,3}\)',
            '',
            item_info['Позиции по КТРУ, ОКПД2'].text_content()
        ).strip(' \n')

        try:
            price = re.findall(
                '[0-9  ]+,[0-9]{2}',
                item_info['Сумма, ₽'].text_content().strip(' \n')
            )[0]
            price = re.sub('[  ]', '', price)
            price = re.sub(',', '.', price)
            item.price = float(price)

        except Exception as e:
            pass

        # Push item to DB
        _item = item.push(session)

    return contract.items


def get_container_by_name(general_contract_page: html.HtmlElement, name: str):
    containers_blocks = general_contract_page.xpath(
        '//div[@class="contentTabBoxBlock contractCard"]/div[@class="container"]')
    containers = {}

    # Get info containers
    for container in containers_blocks:
        container_name = container.xpath('./div/div/h2')[0].text_content()
        containers[container_name] = container

    # Find desired container and return
    desired_container = containers[name]
    return desired_container


def read_page(html_page: html.HtmlElement, oktmo_code):
    # get all elements
    elements = html_page.xpath('//div[@class="search-registry-entrys-block"]/div')

    # Iterate through all elements
    for element in elements:

        # If element is an object:
        if element.get('class') == 'search-registry-entry-block box-shadow-search-input':
            # Get object link and ID
            object_link = 'https://zakupki.gov.ru' + element.xpath('.//div[@class="registry-entry__header-mid__number"]/a')[0].get('href')
            object_id = int(re.findall('reestrNumber=[0-9]+', object_link)[0][13:])
            session = new_session()

            # Open general info page
            request = requests.get(object_link, headers=request_header)
            object_html_page = html.fromstring(request.content)

            # Get contract and client info
            contract = read_contract(object_html_page, object_id, session)
            read_client(object_html_page, contract, oktmo_code, session)

            # Get contractors info
            read_contractors(object_html_page, contract, session)

            # Open target of order page
            request = requests.get(
                f'https://zakupki.gov.ru/epz/contract/contractCard/payment-info-and-target-of-order.html?reestrNumber={object_id}',
                headers=request_header
            )
            target_of_order_page = html.fromstring(request.content)

            # Get contract items
            read_items(target_of_order_page, contract, session)

            # Commit changes and save session
            session.commit()
            session.close()


def count_pages(html_page: html.HtmlElement) -> int:
    max_page = 0
    # noinspection PyBroadException
    try:
        paginator = html_page.xpath('//div[@class="paginator align-self-center m-0"]')[0]
        page_elements = paginator.xpath('.//a[@class="page__link"]')
        for page_element in page_elements:
            page_number = int(page_element.get('data-pagenumber'))
            if page_number > max_page:
                max_page = page_number
    except Exception as e:
        print('count_pages_error:', e)
        raise Exception(e)

    return max_page


def read_all_pages(oktmo_code, day):
    # get page
    request = requests.get('https://zakupki.gov.ru/epz/contract/search/results.html?searchString=&morphology=on&savedSearchSettingsIdHidden=setting_contract_kn4ozkm5&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&selectedContractDataChanges=ANY&contractInputNameDefenseOrderNumber=&contractInputNameContractNumber=&contractPriceFrom=&rightPriceRurFrom=&contractPriceTo=&rightPriceRurTo=&priceToUnitGWS=&contractCurrencyID=-1&advanceFrom=&advanceTo=&advancePercentFrom=&advancePercentTo=&nonBudgetCodesList=&budgetLevelsIdHidden=&budgetLevelsIdNameHidden=%7B%7D&budgetName=&customerIdOrg=&customerFz94id=&customerTitle=&customerPlace=&customerPlaceCodes='f''
                           f'&oktmoIds={oktmo_code}&custLev=&headAgency=&headAgencySelectedRoots=&uniquePositionNumber='
                           f'&contractDateFrom={day}'
                           f'&contractDateTo={day}'
                           f'&executionDateStart=01.01.{day[-4:]}'
                           f'&executionDateEnd=31.12.{day[-4:]}'
                           f'&publishDateFrom=&publishDateTo=&updateDateFrom=&updateDateTo=&classifiersMpItemIds=&classifiersMpItemVersionId=&classifiersMpGroupId=&orderNumber=&placingWayList=&selectedLaws=&summingUpDateStart=&summingUpDateEnd=&bgRegistryNumber=&reestrNumberElectronicForm=&cIKZInputNameYear=&cIKZInputNameIkz=&cIKZInputNameNumPZ=&cIKZInputNameNumPGZ=&cIKZInputNameOkpd2=&cIKZInputNameKvr=&bankSupport=&singleCustomerReason=&singleCustomerReasonCodes=&documentRequisites=&okdpIds=&okdpIdsCodes=&goodsDescription=&okpdIds=&okpdIdsCodes=&okpd2Ids=&okpd2IdsCodes=&ktruCodeNameList=&ktruSelectedChcs=&ktruSelectedChcsNames=&ktruSelectedCharItemVersionIdList=&ktruSelectedRubricatorIdList=&ktruSelectedRubricatorName=&clItemsHiddenId=&clGroupHiddenId=&ktruSelectedPageNum=&goodsCountStart=&goodsCountEnd=&unitPriceStart=&unitPriceEnd=&totalProductsPriceByCodeStart=&totalProductsPriceByCodeEnd=&contractYearPriceStart=&contractYearPriceEnd=&contractTotalYearPriceStart=&contractTotalYearPriceEnd=&kbkNewHead=&kbkNewSection=&kbkNewItem=&kbkNewType=&supplierTitle=&contractSubcontractor=&supplierAddress=&supplierPostalAddress=&supplierStatusCodes=&countryRegIdHidden=&countryRegIdNameHidden=%7B%7D&certificateNumber=&manufacturerName=&mnnFarmNameIdMap=&tradeFarmNameIdMap=&medFormIdMap=&farmDosageIdMap=&sortBy=PUBLISH_DATE&pageNumber=1&sortDirection=true&recordsPerPage=_50&showLotsInfoHidden=false%20and%20False%20',
                           headers=request_header)
    html_page = html.fromstring(request.content)

    try:
        # Read first page
        read_page(html_page, oktmo_code)
    except Exception as e:
        print(f'Exception at oktmo={oktmo_code}, day={day}, page={1}:', e)
        log_error(type='read_page', oktmo_code=oktmo_code, day=day, page=1)

    # Check if there are other pages and read them
    pages_amount = count_pages(html_page)

    for page in range(2, pages_amount + 1):
        request = requests.get(
            'https://zakupki.gov.ru/epz/contract/search/results.html?searchString=&morphology=on&savedSearchSettingsIdHidden=setting_contract_kn4ozkm5&fz44=on&fz94=on&contractStageList_0=on&contractStageList_1=on&contractStageList=0%2C1&selectedContractDataChanges=ANY&contractInputNameDefenseOrderNumber=&contractInputNameContractNumber=&contractPriceFrom=&rightPriceRurFrom=&contractPriceTo=&rightPriceRurTo=&priceToUnitGWS=&contractCurrencyID=-1&advanceFrom=&advanceTo=&advancePercentFrom=&advancePercentTo=&nonBudgetCodesList=&budgetLevelsIdHidden=&budgetLevelsIdNameHidden=%7B%7D&budgetName=&customerIdOrg=&customerFz94id=&customerTitle=&customerPlace=&customerPlaceCodes='f''
            f'&oktmoIds={oktmo_code}&custLev=&headAgency=&headAgencySelectedRoots=&uniquePositionNumber='
            f'&contractDateFrom={day}'
            f'&contractDateTo={day}'
            f'&executionDateStart=01.01.{day[-4:]}'
            f'&executionDateEnd=31.12.{day[-4:]}'
            f'&publishDateFrom=&publishDateTo=&updateDateFrom=&updateDateTo=&classifiersMpItemIds=&classifiersMpItemVersionId=&classifiersMpGroupId=&orderNumber=&placingWayList=&selectedLaws=&summingUpDateStart=&summingUpDateEnd=&bgRegistryNumber=&reestrNumberElectronicForm=&cIKZInputNameYear=&cIKZInputNameIkz=&cIKZInputNameNumPZ=&cIKZInputNameNumPGZ=&cIKZInputNameOkpd2=&cIKZInputNameKvr=&bankSupport=&singleCustomerReason=&singleCustomerReasonCodes=&documentRequisites=&okdpIds=&okdpIdsCodes=&goodsDescription=&okpdIds=&okpdIdsCodes=&okpd2Ids=&okpd2IdsCodes=&ktruCodeNameList=&ktruSelectedChcs=&ktruSelectedChcsNames=&ktruSelectedCharItemVersionIdList=&ktruSelectedRubricatorIdList=&ktruSelectedRubricatorName=&clItemsHiddenId=&clGroupHiddenId=&ktruSelectedPageNum=&goodsCountStart=&goodsCountEnd=&unitPriceStart=&unitPriceEnd=&totalProductsPriceByCodeStart=&totalProductsPriceByCodeEnd=&contractYearPriceStart=&contractYearPriceEnd=&contractTotalYearPriceStart=&contractTotalYearPriceEnd=&kbkNewHead=&kbkNewSection=&kbkNewItem=&kbkNewType=&supplierTitle=&contractSubcontractor=&supplierAddress=&supplierPostalAddress=&supplierStatusCodes=&countryRegIdHidden=&countryRegIdNameHidden=%7B%7D&certificateNumber=&manufacturerName=&mnnFarmNameIdMap=&tradeFarmNameIdMap=&medFormIdMap=&farmDosageIdMap=&sortBy=PUBLISH_DATE'
            f'&pageNumber={page}&sortDirection=true&recordsPerPage=_50&showLotsInfoHidden=false%20and%20False%20',
            headers=request_header
        )

        try:
            html_page = html.fromstring(request.content)
            read_page(html_page, oktmo_code)
        except Exception  as e:
            print(f'Exception at oktmo={oktmo_code}, day={day}, page={page}:', e)
            log_error(type='read_page', oktmo_code=oktmo_code, day=day, page=page)


def run_all_cities():
    all_days = days_2018 + days_2019 + days_2020
    for oktmo_code in oktmo_todo:
        for day in all_days:
            try:
                read_all_pages(oktmo_code, day)
            except Exception as e:
                print(f'Read all pages, oktmo={oktmo_code}, day={day}')
                log_error(type='read_all_pages', oktmo_code=oktmo_code, day=day)

            try:
                print(
                    f'Day done! City: {oktmo_to_city_name[oktmo_code]} (№{oktmo_IDS.index(oktmo_code)+1}), day: {day}'
                )
            except:
                pass


if __name__ == '__main__':
    # run_city_year('207573', days_2018)
    run_all_cities()
