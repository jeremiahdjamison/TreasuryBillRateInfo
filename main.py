import requests
import matplotlib.pyplot as plt
from datetime import datetime

if __name__ == '__main__':
    print("Treasury Bill Rate Information")
    BASE_REST_API_PATH = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od'
    ENDPOINT_API_PATH = '/avg_interest_rates'

    EARLIEST_DATE = '2021-01-01'
    FILTER_API_PATH = '?filter='
    RECORD_DATE_FILTER = 'record_date:gt:' + EARLIEST_DATE + ','
    SECURITY_DESC_FILTER = 'security_desc:eq:Treasury Bills,'
    FILTER = FILTER_API_PATH + RECORD_DATE_FILTER + SECURITY_DESC_FILTER

    REST_PATH = BASE_REST_API_PATH + ENDPOINT_API_PATH + FILTER
    print(REST_PATH)

    response = requests.get(REST_PATH)

    dates = []
    rates = []
    if "data" in response.json():
        for entry in response.json()["data"]:
            print(entry)
            entryDate = entry["record_date"]
            date1 = datetime.strptime(entryDate, '%Y-%m-%d')
            dates.append(date1.date())
            rates.append(float(entry["avg_interest_rate_amt"]))
    plt.plot_date(dates, rates, '-o')

    for x, y in zip(dates, rates):
        plt.annotate("{:.3%}".format(y/100), (x, y), textcoords="offset points", xytext=(0, 10), ha='center')

    plt.show()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
