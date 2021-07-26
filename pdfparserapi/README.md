## Local setup
1. Install Docker for desktop
2. Change to pdfparserapi directory
3. run the command `docker compose up`
4. Server will be exposed at port number 5051
5. From postman make a post request
6. `docker compose down` to bring down the server

## Request structure 
The request json should contain "pdf_path" variable set to the location of pdf to be parsed. This corresponds to absolute path within the container. Create appropriate volumes to achieve this. docker-compose.yaml maps the `pdfs` directory to `/pdfs` within the container.
```
{
    "pdf_path":"/path/to/pdf-file.pdf"
}

//Sample request
{
    "pdf_path":"/pdfs/Final Draft with_without Removal Depreciation.pdf"
}
```

## Response Structure
```
{
    "error": -1,
    "message": "success",
    "statusCode": 200
    "data": {
        // Cleaned up suitable to insert into db
        ...
    }
    "data_full":[   // Array containing data of each page
        {
            // Each page have form_elements and array of tables
            "form_element":{
                ...
            },
            "table":[
                {
                    ...
                },
                ...
                {

                }
            ]
        },
        {

        },
        ...
        {

        }
    ]
}
```

Various error status and its messages
- error=1, pdf_path not provided in request
- error=2, File not available at the path

## Config file
config/config.ini have following important configuration values
- [documentai]
  - project_id= helpful-way-320204
  - location = us (GCP processing location)
  - processor_id_text = 41d21f9c282cc242 (Processor ids, get from GCP DocumentAI page)
  - processor_id_form = 6edc6b52ac6b5543
  - credentials_json = /config/helpful-way-320204-1f6fc98f65d9.json (Service authentication file location)
- [db] // This section have DB related config. This is not used in the api version, but expected to be present with some dummy values.
  - host=127.0.0.1
  - port=3306
  - user=root
  - password=12345
  - db_name=cc_db