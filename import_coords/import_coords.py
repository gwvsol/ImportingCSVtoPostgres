import os
import logging
from csv import DictReader

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

file_csv = os.environ.get('POSTGRES_DUMP_CSV')


def import_coords(file_csv=file_csv):
    # open file in read mode
    with open(file_csv, 'r') as read_obj:
        # pass the file object to DictReader() to get the DictReader object
        csv_dict_reader = DictReader(read_obj)
        # iterate over each line as a ordered dictionary
        try:
            for row in csv_dict_reader:
                # row variable is a dictionary that represents a row in csv
                logging.info(row)
        except KeyboardInterrupt as err:
            pass
            #logging.exception(f'[DUMP IMPORT] Unexpected exception {err}')

try:
    logging.info("[DUMP IMPORT] Start")
    import_coords(file_csv=file_csv)
except (KeyboardInterrupt, OSError) as err:
    logging.exception(f'[DUMP IMPORT] Unexpected exception {err}')
finally:
    logging.info("[DUMP IMPORT] Done")