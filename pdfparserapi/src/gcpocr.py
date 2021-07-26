import logging
import os
from io import BytesIO
from PyPDF2 import PdfFileReader, PdfFileWriter
from abc import abstractmethod

class GcpOcr(object):
    def __init__(self, config, file_path):
        self.logger = logging.getLogger('CCAI.Ocr')
        self.config = config
        self.file_path = file_path
        
        
    def read_pdf(self):
        if os.path.exists(self.file_path):
            self.input_pdf = PdfFileReader(self.file_path)
            return True
        return False
    
    def get_page_count(self):
        return self.input_pdf.getNumPages()

    def get_pdf_page(self, page_no=0):
        if page_no > self.input_pdf.getNumPages():
            return None
        tmp = BytesIO()
        output = PdfFileWriter()
        output.addPage(self.input_pdf.getPage(page_no))
        output.write(tmp)
        image_content = tmp.getvalue()
        return image_content

    def _get_text(self, el, document):
        """Convert text offset indexes into text snippets."""
        response = ""
        # If a text segment spans several lines, it will
        # be stored in different text segments.
        for segment in el.text_anchor.text_segments:
            start_index = segment.start_index
            end_index = segment.end_index
            response += document.text[start_index:end_index]
        
        response = response.strip()
        response = response.replace('\n', '')
        return response

    def add_key_values(self, key_value_pairs, key_string, value_string):
        self.logger.debug("Key: {}, Value: {}".format(key_string, value_string))
        if key_string in key_value_pairs:
            key_value_pairs[key_string].append(value_string)
        else:
            key_value_pairs[key_string] = [value_string]

    def get_key_value_pairs(self):
        if self.document is None:
            self.logger.critical("Call 'parse_pdf' before calling get value")
            return

        key_value_pairs = {}
        for page in self.document.pages:
            for fields in page.form_fields:
                key_string = self._get_text(fields.field_name, self.document)
                value_string = self._get_text(fields.field_value, self.document)
                self.add_key_values(key_value_pairs, key_string, value_string)

        return key_value_pairs

    def get_form_elements(self):
        key_value_paris = self.get_key_value_pairs()
        return key_value_paris

    @abstractmethod
    def parse_pdf(self, page_no=0):
        raise NotImplementedError
        
    def parse_all_pages(self, process_tables=False):
        content = []
        page_count = self.get_page_count()
        for page_no in range(page_count):
            self.logger.debug("parsing page {}/{}".format(page_no + 1, page_count))
            self.parse_pdf(page_no)
            content_page = {
                'form_element':self.get_form_elements(),
                'table':[]
            }
            if process_tables:
                content_page['table'] = self.get_table_elements()
            content.append(content_page)
        return content


    

