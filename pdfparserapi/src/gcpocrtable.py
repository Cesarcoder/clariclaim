import logging
from google.cloud import documentai_v1beta2 as documentai
from gcpocr import GcpOcr

class GcpOcrTable(GcpOcr):
    def __init__(self, config, file_path):
        super().__init__(config, file_path)
        
        self.logger = logging.getLogger('CCAI.OcrTable')
        self.document = None
        self. client = documentai.DocumentUnderstandingServiceClient()

    def parse_pdf(self, page_no=0):
        image_content = self.get_pdf_page(page_no)

        input_config = documentai.types.InputConfig(contents=image_content, mime_type="application/pdf")
        parent = "projects/{}/locations/us".format(self.config['project_id'])

        # Improve table parsing results by providing bounding boxes
        # specifying where the box appears in the document (optional)
        table_bound_hints = [
            documentai.types.TableBoundHint(
                page_number=1,
                bounding_box=documentai.types.BoundingPoly(
                    # Define a polygon around tables to detect
                    # Each vertice coordinate must be a number between 0 and 1
                    normalized_vertices=[
                        # Top left
                        documentai.types.geometry.NormalizedVertex(x=0, y=0),
                        # Top right
                        documentai.types.geometry.NormalizedVertex(x=1, y=0),
                        # Bottom right
                        documentai.types.geometry.NormalizedVertex(x=1, y=1),
                        # Bottom left
                        documentai.types.geometry.NormalizedVertex(x=0, y=1),
                    ]
                ),
            )
        ]

        # Setting enabled=True enables form extraction
        table_extraction_params = documentai.types.TableExtractionParams(
            enabled=True, table_bound_hints=table_bound_hints
        )

        request = documentai.types.ProcessDocumentRequest(
            parent=parent,
            input_config=input_config,
            table_extraction_params=table_extraction_params,
        )

        self.document = self.client.process_document(request=request)
        
    def get_table_data(self, table):
        column_header = {}
        row_values = []
        for row_num, row in enumerate(table.header_rows):
            for col_idx, cell in enumerate(row.cells):
                text = self._get_text(cell.layout, self.document)
                if row_num == 0:
                    if text == '':
                        text = 'Column-{}'.format(col_idx)
                    column_header[col_idx] = text
                else:
                    column_header[col_idx] = column_header[col_idx] + text
        
        for row_num, row in enumerate(table.body_rows):
            current_row = {}
            for col_idx, cell in enumerate(row.cells):
                text = self._get_text(cell.layout, self.document)
                current_row[column_header[col_idx]] = text
            row_values.append(current_row)
        return row_values

    def get_table_elements(self):
        if self.document is None:
            self.logger.critical("Call 'parse_pdf' before calling get value")
            return

        table_data = []
        for page in self.document.pages:
            for _, table in enumerate(page.tables):
                table_data.append(self.get_table_data(table))
        return table_data
        

