import requests
import sys
import matplotlib.pyplot as plt
from datetime import datetime

# Results before this date will be filtered out
EARLIEST_DATE = '2021-01-01'

RESPONSE_CODE_OK = 200

DEBUG = False
FAULT_INJECTION_TABLE = [
    ("FAULT_INJECTION_BAD_REST_STATUS", False),
    ("FAULT_INJECTION_NO_DATA_IN_RESPONSE", False)
]


def is_fault_enabled(fault):
    if any(fault in key and val is True for key, val in FAULT_INJECTION_TABLE):
        print("Injecting Fault: ", fault)
        return True
    else:
        return False


if __name__ == '__main__':
    print("Treasury Bill Rate Information")
    BASE_REST_API_PATH = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/accounting/od'
    ENDPOINT_API_PATH = '/avg_interest_rates'

    FILTER_API_PATH = '?filter='
    RECORD_DATE_FILTER = 'record_date:gt:' + EARLIEST_DATE + ','
    SECURITY_DESC_FILTER = 'security_desc:eq:Treasury Bills,'
    FILTER = FILTER_API_PATH + RECORD_DATE_FILTER + SECURITY_DESC_FILTER

    REST_PATH = BASE_REST_API_PATH + ENDPOINT_API_PATH + FILTER
    print(REST_PATH)

    response = requests.get(REST_PATH)
    if DEBUG:
        print("response info:")
        print("response.text:")
        print(response.text)
        print(response.status_code)

    if is_fault_enabled("FAULT_INJECTION_BAD_REST_STATUS"):
        response.status_code = 404

    if response.status_code != RESPONSE_CODE_OK:
        print("Bad response code: ", response.status_code)
        sys.exit(response.status_code)

    json_response_data = response.json()

    if "data" not in json_response_data or is_fault_enabled("FAULT_INJECTION_NO_DATA_IN_RESPONSE"):
        print("No data in request")
        sys.exit("No data in request")

    if len(json_response_data["data"]) == 0:
        print("No entries returned in response data")
        sys.exit("No entries return in response data")

    dates = []
    rates = []
    for entry in json_response_data["data"]:
        if DEBUG:
            print(entry)
        entryDate = entry["record_date"]
        date1 = datetime.strptime(entryDate, '%Y-%m-%d')
        dates.append(date1.date())
        rates.append(float(entry["avg_interest_rate_amt"]))

    plt.plot_date(dates, rates, '-o')

    for x, y in zip(dates, rates):
        plt.annotate("{:.3%}".format(y / 100), (x, y), textcoords="offset points", xytext=(0, 10), ha='center')

    plt.show()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
