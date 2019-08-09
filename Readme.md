### Analyzer

Python script to find the Top n pages from your Google analytics account and write the response to a file/stdout in json/yaml format 

### How to run

+ Use virtualenv to create a virtual environment

  ```bash
  # Create a virtual env
  $ virtualenv venv

  # Activate virtual env
  $ source venv/bin/activate
  ```

+ Install dependencies using Pip

  ```bash
  $ pip install -r requirements.txt
  ```

+ Specify Google service account credentials file location

  Follow [these instructions](https://cloud.google.com/iam/docs/creating-managing-service-accounts#iam-service-accounts-create-console) to create a service account in Google console. Download the `key.json` file and specify the file location in `.env`.

+ Run the script
  ```bash
  $ python main.py 
  ```   
