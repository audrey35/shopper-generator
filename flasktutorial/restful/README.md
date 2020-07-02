# Building RESTFUL APIs with Flask

[LinkedIn Learning course](https://www.linkedin.com/learning/building-restful-apis-with-flask)

## How to setup the program
1. Install Postman
2. Install flask and flask-mongoengine (not available in conda)
- `conda install -c anaconda flask`
- `/anaconda/envs/env_name/bin/pip install flask-mongoengine`
3. Add a run configuration
- Open 'Edit Run/Debug configurations' dialog (the drop-down used to select which file to run in PyCharm) and click Edit Configurations
- Click the plus sign (Add new configuration)
- Give a name to the run configuration (i.e., Run Shopper API)
- Set Target type to Script path
- Target should be set to the app.py file (.../flasktutorial/restful/app.py)
- FLASK_ENV should be set to development
- FLASK_DEBUG should be checked
- Click Apply, then OK
4. Select "Run Shopper API" from the run configurations and run it.
5. Copy the URL provided in the Run tab, which should be http://127.0.0.1:5000/
5. Open Postman
- Close the splash screen (no need to login)
- Click the plus sign to see the page with Send button on it.
- Paste the copied URL into Postman where it says "Enter request URL"
- Press Send button

## How to run the program
Assumes flask server is running and you have provided the server url to Postman.
