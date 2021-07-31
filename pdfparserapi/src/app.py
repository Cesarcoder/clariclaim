import os
import logging
import configparser
import pprint

from flask import Flask, request, jsonify

from mylogger import init_logger
from preparedata import PrepareData
from gcpocrtable import GcpOcrTable

app = Flask(__name__, instance_relative_config=True)

CONFIG_PATH = '/config/config.ini'
config = None

# Initialize logger
init_logger('CCAI', 'DEBUG')
logger = logging.getLogger()

def build_config(config_path):
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

@app.before_first_request
def initialize():
    logger.info('Initializing PDF Parser api')
    global config
    config = build_config(CONFIG_PATH)
    print(config)

    logger.info('Setting credential env variables')
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config['credentials_json']
    
@app.route("/", methods = ["POST"])
def homepage():
    error = -1
    message = 'success'

    data = request.json
    if 'pdf_path' not in data:
        error = 1
        message = 'pdf_path not provided in request'
        logger.error(message)
        return jsonify(statusCode = 200, error=error, message=message)

    pdf_path = data["pdf_path"]
    logger.debug("Parsing {}".format(pdf_path))

    gcp_ocr = GcpOcrTable(config, pdf_path)
    file_availability = gcp_ocr.read_pdf()
    if not file_availability:
        error = 2
        message = 'File not available at {}'.format(pdf_path)
        logger.error(message)
        return jsonify(statusCode = 200, error=error, message=message)

    num_pages = gcp_ocr.get_page_count()
    logger.debug("Pdf have {} page(s)".format(num_pages))
    
    content = gcp_ocr.parse_all_pages(process_tables=True)
    logger.debug(content)

    prep = PrepareData(config)
    key_value_pairs_pp = prep.prep_meta_fields(content[0]['form_element'])
    logger.debug(key_value_pairs_pp)

    # gcp_ocr.parse_pdf(page_no=0)
    # key_value_pairs = gcp_ocr.get_form_elements()
    # pp = pprint.PrettyPrinter(indent=2)
    # pp.pprint(key_value_pairs)
    # logger.debug(key_value_pairs)

    # self.gcp_ocr.parse_pdf(file_path, page_no=4)
    # table_data = self.gcp_ocr.get_table_elements()
    # for table in table_data:
    #     print(pd.DataFrame(table))

    
    # self.db.insert_record(key_value_pairs_pp)
    # pp.pprint(key_value_pairs_pp)


    # document_id = str(uuid.uuid1())

    
    

    return jsonify(statusCode = 200, error=error, message=message, data=key_value_pairs_pp, data_full=content)

if __name__ == '__main__':
    app.run(debug=False, port=5051, host="0.0.0.0")
