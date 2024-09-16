## Custom Flask API Fronting Chat-GPT40-mini
The previous iteration of the repo that was parsing profiles more intelligently is preserved in the `/archived/` directory because Wes is in a rush and being lazy.

In the root of the project are 3 files:
  - api.py
  - gpt.py
  - parse_profiles.py

Running `python api.py` will start a Flask API on localhost:5000, containing a single POST route on `/search`. This endpoint takes a JSON payload with the shape `{"skills": "search terms here"}` and responds with the GPT-generated consultant recommendations in the shape `{"recommendations": "Here are the top 3 consultants who best fit the skill..."}`.

### Things to be improved
The consultant profiles are being parsed and loaded into the prompt context fresh with each request. While this allows us to ensure that the response has the most up-to-date content from the files, it is significantly slowing down the response. Merging Patrick's DB-loading and querying from the DB would definitely be a better long-term solution; unfortunately Wes is out of time.

## here's where I say parsed a lot
Parserr.py is the file that parses the ppt files.  
To troubleshoot the parserr.py file, you can execute the preview_parsed_ppts.py file.  This will populate the parsed_data.json file with the parsed data.
if you execute the main.py file, it will send the parsed data to the azure sqldb.  
  the azure sql db server configurations are in the db_config.py file.  You can get the password from Wes while I'm OOO

