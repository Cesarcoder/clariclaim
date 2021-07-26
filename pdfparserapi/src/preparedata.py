import logging

class PrepareData(object):
    def __init__(self, config):
        self.logger = logging.getLogger('CCAI.PD')
        self.config = config
        self.build_field_mapping()

    def build_field_mapping(self):
        self.fm = {
            'E-mail:':'email',
            'Email:':'email',
            'Insured:':'insured',
            'Phone:':'phone',
            'Claim Number:':'claim_number',
            'Company:':'company',
            'Type of Loss:':'type_of_loss',
            'Estimate:':'estimate',
            'Estimator:':'estimator',
        }
    def prep_meta_fields(self, data):
        processed = {
            'claim_number':'',
            'company':'',
            'type_of_loss':'',
            'insured':'',
            'estimate':'',
            'estimator':'',
            'email':'',
            'phone':''
        }
        for ele in data:
            if ele in self.fm:
                processed[self.fm[ele]] = " ".join(data[ele])[:63]
        return processed



        