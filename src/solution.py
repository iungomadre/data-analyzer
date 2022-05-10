import argparse
from CSVParser import CSVParser
from DataRetriever import DataRetriever
import icu

###########
# configure
MANDATORY_FIELDS = [
    'Street',
    'Zip',
    'City',
    'Last Check-In Date',
    'Company'
]
REGION = 'es'
#############

ALPHABET_SORT_KEY = icu.Collator.createInstance(icu.Locale(f'{REGION}.UTF-8')).getSortKey


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Analyze your company's data")
    parser.add_argument("file_name", type=str, help="name of CSV file containing company's data")
    args = parser.parse_args()

    header, data = CSVParser(args.file_name, MANDATORY_FIELDS).parse_file()
    retriever = DataRetriever(data)

    # EARLIEST CHECK-IN DATE
    earliest_checkin_customer = retriever.get_chosen_date_rows(header.index('Last Check-In Date'), min, REGION)

    # LATEST CHECK-IN DATE
    latest_checkin_customer = retriever.get_chosen_date_rows(header.index('Last Check-In Date'), max, REGION)

    # FULL NAMES
    customer_full_names = sorted(retriever.get_concatenated_fields([
        header.index('First Name'),
        header.index('Last Name')
    ], delimiter=' '), key=ALPHABET_SORT_KEY)

    # JOBS
    jobs = sorted(retriever.get_unique_fields(header.index('Job')), key=ALPHABET_SORT_KEY)

    # print data
    print(f'Earliest Check-In Date: {earliest_checkin_customer}')
    print(f'Latest Check-In Date: {latest_checkin_customer}')
    print(f'Customer full names: {customer_full_names}')
    print(f'Jobs: {jobs}')
