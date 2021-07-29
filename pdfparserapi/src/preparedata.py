import logging

class PrepareData(object):
    def __init__(self, config):
        self.logger = logging.getLogger('CCAI.PD')
        self.config = config
        self.build_field_mapping()

    def build_field_mapping(self):
        self.fm = {
            'Business:':'business',
            'Cell:':'cell',
            'Cellular:':'cell',
            'Phone:':'cell',
            'Claim Number:':'claim_number',
            'Claim Rep.:':'claim_rep',
            'Company:':'company',
            'Insurance Company :':'company',
            'Date Est. Completed:':'date_completed',
            'Date Completed:':'date_completed',
            'Date Contacted:':'date_contacted',
            'Date Entered:':'date_entered',
            'Date Inspected:':'date_inspected',
            'Date of Loss:':'date_of_loss',
            'Date Received:':'date_received',
            'E-mail:':'email',
            'Email:':'email',
            'Estimate:':'estimate',
            'Estimator:':'estimator',
            'Fax:':'fax',
            'FAX':'fax',
            'Home:':'home',
            'Insured:':'insured',
            'Policy Number:':'policy_number',
            'Price List:':'price_list',
            'Property:':'property',
            'Type of Loss:':'type_of_loss',
        }
        
    def prep_meta_fields(self, data):
        processed = {
            'claim_number':'',
            'policy_number':'',
            'company':'',
            'type_of_loss':'',
            'insured':'',
            'estimate':'',
            'estimator':'',
            'email':'',
            'phone':'',
            'business':'',
        }
        for ele in data:
            if ele in self.fm:
                if self.fm[ele] in processed:
                    processed[self.fm[ele]] = " ".join(data[ele])
        return processed



        