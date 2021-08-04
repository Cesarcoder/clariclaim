import os
import json
import pandas as pd
os.environ["LOG_LEVEL"] = "VERBOSE"
# os.environ["LOG_LEVEL"] = "DEBUG"

from parsepdf import ParsePdf
parse_pdf = ParsePdf('config/config-local.ini')


# # =================================================================
# # Single file parsing
# file_path = 'pdfs/Adjusters Figures - Final.pdf'
# file_path = 'pdfs/Bateman Company DW Estimate.pdf'
# file_path = 'pdfs/Final Draft with_without Removal Depreciation.pdf'
# file_path = 'pdfs/Fanning S_G Dwelling Estimate.pdf'
# parse_pdf.process_file(file_path)


# input_path = 'claims_uploaded_7-23'
# output_path = 'json_dump'

# =================================================================
# File preparation
# processed_file = []
# for file_path in sorted(os.listdir(input_path)):
#     if not file_path.endswith(('.pdf', '.PDF')):
#         continue
#     logger.info("Processing: {}".format(file_path))
#     processed_file.append({
#         'file_path':file_path,
#         'processed':False
#     })
# processed_file = pd.DataFrame(processed_file)
# processed_file.to_csv("processed_file.csv", index=False)

# =================================================================
# processed_file = pd.read_csv("processed_file.csv")
# for idx, row in processed_file.iterrows():
#     if row['processed']:
#         continue
#     file_path = row['file_path']
#     file_name_ext = os.path.basename(file_path)
#     file_name = os.path.splitext(file_name_ext)[0]
#     file_name = file_name + ".json"
#     content = parse_pdf.process_file(os.path.join(input_path, file_path))        
#     with open(os.path.join(output_path, file_name), 'w', encoding='utf-8') as f:
#         json.dump(content, f, ensure_ascii=False, indent=4)
#     processed_file.loc[idx, 'processed'] = True
#     processed_file.to_csv("processed_file.csv", index=False)


# =================================================================
json_dump_path = 'Data/json_dump/'
final_value = pd.read_excel('Data/Final Value.xlsx', sheet_name='Sheet1', engine='openpyxl')
final_value['Prediction'] = ''
for idx, row in final_value.iterrows():
    file_name = row['File Name']
    if not file_name.endswith('.json'):
        continue
    f = open(os.path.join(json_dump_path, file_name), encoding="utf8")
    data = json.load(f)

    # amount = parse_pdf.prep.get_total_amount(data)
    # final_value.loc[idx, 'Prediction'] = amount
    # print(file_name, '\t', row['RCV'], '\t', amount)
    
    # company = parse_pdf.prep.prep_meta_fields(data[0])
    # print(file_name, company['company'])

    tabels = parse_pdf.prep.get_tables(data)
    # print(tabels)
    # break 
    # if file_name == 'Shattuck revised.json':
    #     import pdb
    #     pdb.set_trace()
final_value.to_csv('Data/final_value.csv', index=False)

    
        
