import logging
from gcpocr import GcpOcr
from google.cloud import documentai_v1 as documentai

class GcpOcrForm(GcpOcr):
    def __init__(self, config, file_path):
        super().__init__(config, file_path)
        self.logger = logging.getLogger('CCAI.OcrFrom')
        opts = {}
        self.client = documentai.DocumentProcessorServiceClient(client_options=opts)

    def parse_pdf(self, page_no=0):
        image_content = self.get_pdf_page(page_no)
        
        name = f"projects/{self.config['project_id']}/locations/{self.config['location']}/processors/{self.config['processor_id_form']}"

        document = {"content": image_content, "mime_type": "application/pdf"}
        # Configure the process request
        request = {"name": name, "raw_document": document}

        result = self.client.process_document(request=request)
        self.document = result.document

        key_value_paris = self.get_key_value_pairs(document)
        return key_value_paris



