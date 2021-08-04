import argparse
import configparser
import os
import logging
import pprint
import pandas as pd
import uuid
import json

# Custom modules
from mylogger import init_logger
# from dbops import DBOps
from preparedata import PrepareData
from gcpocrtable import GcpOcrTable


class ParsePdf(object):
    def __init__(self, config_path):
        # Initialize logger and Orchestrator
        log_level = os.getenv('LOG_LEVEL', 'INFO')
        init_logger('CCAI', log_level)
        self.logger = logging.getLogger('CCAI')
        self.config = self.build_config(config_path)

        self.logger.info('Setting credential env variables')
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.config['credentials_json']
        print(self.config)

        # self.db = DBOps(self.config, setup=False)
        self.prep = PrepareData(self.config)
    
    def build_config(self, config_path):
        self.logger.info("Config Path: {}".format(config_path))
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
        self.logger.debug("Parsing {}".format(file_path))
        gcp_ocr = GcpOcrTable(self.config, file_path)
        file_availability = gcp_ocr.read_pdf()
        if not file_availability:
            error = 2
            message = 'File not available at {}'.format(file_path)
            self.logger.error(message)
            return error, message

        num_pages = gcp_ocr.get_page_count()
        self.logger.debug("Pdf have {} page(s)".format(num_pages))
        
        content = gcp_ocr.parse_all_pages(process_tables=True)
        self.logger.verbose(content)

        key_value_pairs_pp = self.prep.prep_meta_fields(content[0]['form_element'])
        self.logger.verbose(key_value_pairs_pp)

        return content

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

    # =================================================================
    # Single file parsing
    file_path = 'pdfs/Adjusters Figures - Final.pdf'
    file_path = 'pdfs/Bateman Company DW Estimate.pdf'
    file_path = 'pdfs/Final Draft with_without Removal Depreciation.pdf'
    file_path = 'pdfs/Fanning S_G Dwelling Estimate.pdf'
    parse_pdf.process_file(file_path, 0)


    
        
