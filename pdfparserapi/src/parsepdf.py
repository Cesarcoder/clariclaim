import argparse
import configparser
from importlib import reload
import logging
import os
import pprint
import pandas as pd
import uuid

# Custom modules
from dbops import DBOps
from preparedata import PrepareData
from gcpocrtable import GcpOcrTable

class ParsePdf(object):
    def __init__(self, config_path):
        # Initialize logger and Orchestrator
        self.init_logger()
        self.config = self.build_config(config_path)

        logger.info('Setting credential env variables')
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.config['credentials_json']
        print(self.config)

        # self.db = DBOps(self.config, setup=False)
        self.prep = PrepareData(self.config)
        
    def get_logger(self, logLevel):
        """
            Initializes the logger
            Check specified log file exist, if not create the directory and file
            Add both file and console handlers
            Arguments
            logLevel: Log level for both file and console
        """

        # Logging
        reload(logging)
        # from https://docs.python.org/2/howto/logging-cookbook.html
        global logger
        logger = logging.getLogger('CCAI')
        logger.setLevel(logging.DEBUG)
        # Log formatter
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s', "%Y-%m-%d %H:%M:%S")
        
        # Logging to console
        ch = logging.StreamHandler()
        ch.setLevel(logLevel)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(ch)
        return logger

    def init_logger(self):
        # Read Log level
        # Declare predefined set of log levels
        # Check user provided the optional log level parameter, 
        # If so check if its part of predefined list, else fall back to the 
        # default of INFO
        log_levels = {'CRITICAL':50, 'ERROR':40, 'WARNING':30, 'INFO':20, 'DEBUG':10, 'NOTSET':0}
        # If environment variable is not set, log at debug level, if incorrect value is set
        # log at info level
        log_level = os.getenv('LOG_LEVEL', 'DEBUG')
        if log_level not in log_levels:
            log_level = 'INFO'
        logLevelNumeric = log_levels[log_level]
        logger = self.get_logger(logLevelNumeric)
        logger.critical("Using log level {0}. [This message is raised at CRITICAL level so that this is visible at all log levels]".format(log_level))

    def build_config(self, config_path):
        logger.info("Config Path: {}".format(config_path))
        parser = configparser.ConfigParser()
        parser.read(config_path)
        config = {
            'project_id':parser['documentai']['project_id'],
            'location':parser['documentai']['location'],
            'processor_id_text':parser['documentai']['processor_id_text'],
            'processor_id_form':parser['documentai']['processor_id_form'],
            'credentials_json':parser['documentai']['credentials_json'],
            'db_host':parser['db']['host'],
            'db_port':parser['db']['port'],
            'db_user':parser['db']['user'],
            'db_password':parser['db']['password'],
            'db_db_name':parser['db']['db_name']
        }
        return config

    def process_file(self, file_path):

        logger.debug("Parsing {}".format(file_path))
        gcp_ocr = GcpOcrTable(self.config, file_path)
        file_availability = gcp_ocr.read_pdf()
        if not file_availability:
            error = 2
            message = 'File not available at {}'.format(file_path)
            logger.error(message)
            return error, message

        num_pages = gcp_ocr.get_page_count()
        logger.debug("Pdf have {} page(s)".format(num_pages))
        
        content = gcp_ocr.parse_all_pages(process_tables=True)
        logger.debug(content)

        key_value_pairs_pp = self.prep.prep_meta_fields(content[0]['form_element'])
        logger.debug(key_value_pairs_pp)

        # # Old version
        # document_id = str(uuid.uuid1())
        
        # self.gcp_ocr.parse_pdf(file_path, page_no=1)
        # key_value_pairs = self.gcp_ocr.get_form_elements()
        # pp = pprint.PrettyPrinter(indent=2)
        # pp.pprint(key_value_pairs)

        # self.gcp_ocr.parse_pdf(file_path, page_no=4)
        # table_data = self.gcp_ocr.get_table_elements()
        # for table in table_data:
        #     print(pd.DataFrame(table))

        # key_value_pairs_pp = self.prep.prep_meta_fields(key_value_pairs, document_id)
        # self.db.insert_record(key_value_pairs_pp)
        # pp.pprint(key_value_pairs_pp)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="GCP Document AI OCR")
    parser.add_argument('-c', action='store', dest='config_path', default='config/config-local.ini', help='Config file path')
    args = parser.parse_args()

    parse_pdf = ParsePdf(args.config_path)

    file_path = 'pdfs/Adjusters Figures - Final.pdf'
    # file_path = 'pdfs/Bateman Company DW Estimate.pdf'
    file_path = 'pdfs/Final Draft with_without Removal Depreciation.pdf'
    # file_path = 'pdfs/Fanning S_G Dwelling Estimate.pdf'

    parse_pdf.process_file(file_path)
    
