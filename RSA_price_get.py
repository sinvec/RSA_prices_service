import requests

RSA_API = {
    'get_rf_subject_ids':
        'https://prices.autoins.ru/priceAutoPublicCheck/api/rf_subject/date?versionDate={}',
    'get_oem_ids':
        'https://prices.autoins.ru/priceAutoPublicCheck/api/oem/date?versionDate={}',
    'get_price_url':
        'https://prices.autoins.ru/priceAutoPublicCheck/api/spareprice'
}

def RSA_price_get(
    report_date,
    catalog_number,
    rf_subject,
    car_brand
):

    # получаем справочник субъектов РФ
    get_rf_subject_ids_result = requests.get(RSA_API['get_rf_subject_ids'].format(report_date))
    subjects = {row['subjectName']: row['subjectRF'] for row in get_rf_subject_ids_result.json()}

    # получаем cписок марок автомобилей
    get_oem_ids_result = requests.get(RSA_API['get_oem_ids'].format(report_date))
    brands = {row['name']: row['id'] for row in get_oem_ids_result.json()}

    # получаем цены на запчасть
    request_data = {
        'oemId': brands[car_brand],
        'subjectRF': subjects[rf_subject],
        'versionDate': report_date,
        'partNumber1': catalog_number
    }
    get_price_url_result = requests.post(RSA_API['get_price_url'], json = request_data)
    spare_info = get_price_url_result.json()['repairPartDtoList'][0]

    if spare_info['found']:
        return {
            'spare_name': spare_info['spareName'],
            'reg_coef': spare_info['regCoef'],
            'spare_price': spare_info['sparePrice'],
            'base_cost': spare_info['baseCost']
        }

# Пример испозования:
# RSA_price_get('21.10.2023', '034115417', 'Свердловская область', 'Audi')
# Результат:
# {'spare_name': 'деталь', 'reg_coef': '1.05000', 'spare_price': '20232.21', 'base_cost': '19268.77'}