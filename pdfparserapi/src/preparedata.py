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

    def _is_valid_amount(self, number):
        try:
            number = number.replace(',', '')
            number = float(number)
        except:
            return False
        if number < 100.0:
            return False

        return True

    def get_total_amount(self, data):
        # As last page likely to have final amount
        # Loop from last page to first page
        amount = ''
        found_amount = False
        for page in data[::-1]:
            tables = page['table']
            # Loop tables in reverse order
            for table in tables[::-1]:
                if len(table) < 1:
                    continue
                # If RCV in final records of the table
                if 'RCV' in table[-1]:
                    amount = table[-1]['RCV']
                    amount = amount.replace('$', '')
                    self.logger.verbose('Parsed amount: {}'.format(amount))
                    if self._is_float(amount):
                        found_amount = True
                        break
                    elif 'Total' in page['form_element']:
                        amount = page['form_element']['Total'][0]
                        amount = amount.replace('$', '')
                        self.logger.verbose('Parsed amount: {}'.format(amount))
                        if self._is_float(amount):
                            found_amount = True
                            break
                elif 'Total' in page['form_element']:
                    amount = page['form_element']['Total'][0]
                    amount = amount.replace('$', '')
                    if self._is_float(amount):
                        found_amount = True
                        break
                elif 'Replacement Cost Value' in page['form_element']:
                    amount = page['form_element']['Replacement Cost Value'][0]
                    amount = amount.replace('$', '')
                    if self._is_float(amount):
                        found_amount = True
                        break


            # If amount is found break the page loop
            if found_amount:
                break
        
        return amount.replace(',', '')



        