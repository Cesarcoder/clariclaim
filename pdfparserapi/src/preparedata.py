import logging
import pandas as pd

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
        self.company_map = {
            'Liberty Mutual Insurance': ['Liberty Mutual Insurance'],
            'Parker Loss Consultants': ['Parker Loss Consultants'],
            'United Service Adjustment': ['United Service Adjustment'],
            'Plymouth Rock Assurance': ['Plymouth Rock Plymouth Rock Assurance', 'Plymouth Rock Assurance', 'Plymouth Rock'],
            'Amica Mutual Insurance Company': ['Amica'],
            'MPIUA': ['MPIUA'],
            'Independent Claims Service, Inc': ['Independent Claims Service, Inc'],
            'New England Claims Service': ['New England Claims Service'],
            'MASS PROPERTY INSURANCE': ['MASS PROPERTY INSURANCE'],
            'MASS BAY MOVERS': ['MASS BAY MOVERS'],
            'TRAVELERS': ['TRAVELERSJ'],
            'AMERICAN NATIONAL': ['AMERICANNATIONAL'],
            'MAPFRE INSURANCE': ['MAPFRE | INSURANCE', 'MAPFRE'],
            'Colonial Adjustment, Inc.': ['Colonial Adjustment, Inc.'],
            'Insurance Adjustment Service, Inc.': ['Insurance Adjustment Service, Inc.'],
        }
        self.table_header_clean={'qty':'quantity',
            'quantity unit':'quantity',
            'price':'unit price',
        }
        
    def get_company(self, data):
        for comp_name in self.company_map:
            for comp_str in self.company_map[comp_name]:
                if comp_str in data:
                    return comp_name
        return ''
        
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
        for ele in data['form_element']:
            if ele in self.fm:
                if self.fm[ele] in processed:
                    processed[self.fm[ele]] = " ".join(data['form_element'][ele])

        # If company is empty look for paragraph to find the company
        if processed['company'] == '':
            processed['company'] = self.get_company(data['paragraph'])
        
        return processed

    def get_valid_number(self, number):
        number = number.replace(',', '')
        number = number.replace('$', '')
        number = float(number)
        return number

    def _is_valid_amount(self, number):
        try:
            number = self.get_valid_number(number)
        except:
            return False
        
        if number < 100.0:
            return False
        
        return True

    def _get_total_amount(self, data, field_type='RCV'):
        # As last page likely to have final amount
        # Loop from last page to first page
        amount_final = 0.0
        found_amount = 0
        for page in data[::-1]:
            amount = ''
            tables = page['table']
            # Loop tables in reverse order
            for table in tables[::-1]:
                if len(table) < 1:
                    continue
                # If RCV in final records of the table
                if field_type in table[-1]:
                    amount = table[-1][field_type]
                    self.logger.verbose('Field: {} Parsed amount table: {}'.format(field_type, amount))
                    if self._is_valid_amount(amount):
                        found_amount += 1
                        amount_final = max(amount_final, self.get_valid_number(amount))
                    elif 'Total' in page['form_element']:
                        amount = page['form_element']['Total'][0]
                        self.logger.verbose('Field: {} Parsed amount table: {}'.format(field_type, amount))
                        if self._is_valid_amount(amount):
                            found_amount += 1
                            amount_final = max(amount_final, self.get_valid_number(amount))
                elif 'Total' in page['form_element']:
                    amount = page['form_element']['Total'][0]
                    self.logger.verbose('Field: {} Parsed amount table: {}'.format(field_type, amount))
                    if self._is_valid_amount(amount):
                        found_amount += 1
                        amount_final = max(amount_final, self.get_valid_number(amount))
                # elif 'Replacement Cost Value' in page['form_element']:
                #     amount = page['form_element']['Replacement Cost Value'][0]
                #     amount = amount.replace('$', '')
                #     self.logger.verbose('Parsed amount RCV: {}'.format(amount))
                #     if self._is_valid_amount(amount):
                #         found_amount = True
                #         break


            # If amount is found break the page loop
            if found_amount > 5:
                break
            else:
                amount = ''
        
        if amount_final > 0:
            return amount_final
        
        return 0.0
        
    def get_total_amount(self, data, tables):
        
        rcv = self._get_total_amount(data, field_type='RCV')
        acv = self._get_total_amount(data, field_type='ACV')

        def _get_float(x):
            try:
                x = self.get_valid_number(x)
            except:
                return 0.0
            return x
        
        tables = pd.DataFrame(tables)
        table_amount = 0.0
        if 'rcv' in tables.columns:
            tables['RCV_float'] = tables['rcv'].apply(lambda x: _get_float(x))
            table_amount = tables['RCV_float'].max()
        
        self.logger.debug("RCV: {}, ACV: {} Table Amount: {}".format(rcv, acv, table_amount))
        amount_final = max(rcv, acv, table_amount)
        if amount_final > 0:
            return "{:.2f}".format(amount_final)
        else:
            return ''

    def jaccard_similarity(self, seta, setb):
        seta = set(seta)
        setb = set(setb)
        un = seta.union(setb)
        intersection = seta.intersection(setb)
        return len(intersection) / len(un)

    def get_tables(self, data):
        column_list = ['DESCRIPTION', 'QUANTITY', 'UNIT PRICE', 'TAX', 'O&P', 'RCV', 'DEPREC.', 'ACV']
        column_list = ['description', 'quantity', 'unit price', 'tax', 'o&p', 'rcv', 'deprec.', 'acv']
        result = []
        for page_no, page in enumerate(data, 1):
            tables = page['table']
            # Loop tables in reverse order
            for table_no, table in enumerate(tables, 1):
                if len(table) < 1:
                    continue
                table_df = pd.DataFrame(table)
                table_df.columns = table_df.columns.str.lower()
                table_df.rename(self.table_header_clean, axis='columns', inplace=True)
                jaccard_sim = self.jaccard_similarity(table_df.columns, column_list)
                if jaccard_sim >= 0.5:
                    table_df['page_no'] = page_no
                    table_df['table_no'] = table_no
                    result.append(table_df)
        if len(result) > 0:
            result = pd.concat(result)
            # Add columns, if standard ones are not present
            for column_name in column_list:
                if column_name not in result.columns:
                    result[column_name] = ''
            result = result[['page_no', 'table_no'] + column_list]
            result.fillna('', inplace=True)
            result = result.to_dict('records')
        return result
