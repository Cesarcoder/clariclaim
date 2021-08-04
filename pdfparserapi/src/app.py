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
log_level = os.getenv('LOG_LEVEL', 'INFO')
init_logger('CCAI', log_level)
logger = logging.getLogger('CCAI')

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

    # Cleanup the ocr results
    prep = PrepareData(config)
    # Get key value pairs
    key_value_pairs_pp = prep.prep_meta_fields(content[0])
    # Get RCV
    key_value_pairs_pp['RCV'] = prep.get_total_amount(content)
    logger.verbose(key_value_pairs_pp)
    # pp.pprint(key_value_pairs_pp)
    # Get Tables
    tables = prep.get_tables(content)

    return jsonify(statusCode = 200, error=error, message=message, 
            data=key_value_pairs_pp, tables=tables, data_full=content)

if __name__ == '__main__':
    app.run(debug=False, port=5051, host="0.0.0.0")
