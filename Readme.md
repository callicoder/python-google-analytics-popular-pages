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

  Note: You'll also need to enable Google analytics APIs.

+ Add Google Analytics VIEW_ID in environment
  Follow these steps to get the VIEW_ID for your analytics account:

  * Sign in to Google Analytics.
  * Click Admin, and navigate to View.
  * In the VIEW column, click View Settings.
  * You'll find View ID in Basic Settings.


+ Run the script
  ```bash
  $ python main.py 
  ```   
