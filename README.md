## Custom Flask API Fronting Chat-GPT40-mini
The previous iteration of the repo that was parsing profiles more intelligently is preserved in the `/archived/` directory because Wes is in a rush and being lazy.

In the root of the project are 3 files:
  - api.py
  - gpt.py
  - parse_profiles.py

Running `python api.py` will start a Flask API on localhost:5000, containing a single POST route on `/search`. This endpoint takes a JSON payload with the shape `{"skills": "search terms here"}` and responds with the GPT-generated consultant recommendations in the shape `{"recommendations": "Here are the top 3 consultants who best fit the skill..."}`.

### REACH OUT TO WES OR PATRICK FOR OPENAI TOKEN AND AZURE DB PASSWORD
these will be added to the config.py file

### DB update (by patrick)
when executed, the parse_profiles file will load all of the files from the profiles/ directory into the consultants table in azure db.
then when the gpt.py file gets executed, it will query the database for profile data.

### considerations (by patrick)
Although this will most likely speed up the process a bit, I think we will still run into a lag because of the database connection every time.  I think using Azure's "Data API Builder" as an intermediate might be helpful.  I was learning about it at a sql conference, but haven't directly worked with it.  I think it needs to be using docker, which is how azure web apps are created, so it would be a v2 situation.

## here's where I say parsed a lot
Parserr.py is the file that parses the ppt files.  
To troubleshoot the parserr.py file, you can execute the preview_parsed_ppts.py file.  This will populate the parsed_data.json file with the parsed data.
if you execute the main.py file, it will send the parsed data to the azure sqldb.  
  the azure sql db server configurations are in the db_config.py file.  You can get the password from Wes while I'm OOO

