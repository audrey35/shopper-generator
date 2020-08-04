# Shopper Data Generator

## Installations
The Shopper Data Generator should be used with python 3.8.
Please install the required libraries using the [requirements.txt](requirements.txt) by running 
`pip install -r requirements.txt` in command line or terminal.

### Detailed instructions for PyCharm on a Mac
1. Open PyCharm
2. On the welcome screen, select "Get from Version Control".
3. Select "Repository URL" and Version Control should be set to "Git".
4. URL should be "https://github.ccs.neu.edu/simpsone/5500Project.git".
5. Directory should auto-populate once you provide the URL. Click "Clone" to create the project.
6. Click on "PyCharm", then "Preferences".
7. Click on "Project Interpreter".
8. Click on the gear icon to add a new interpreter.
9. Select "Virtualenv Environment", then "New environment".
10. Specify a location if needed. But the Base interpreter should be set to Python 3.8
11. Click OK to close the dialog and create the virtual environment.
12. Click OK to close the Preferences dialog.
13. Open the Terminal tab at the bottom of the screen.
14. The virtual environment you created should be activated. Indicated by `(venv)`.
14. Run the command `pip install -r requirements.txt` to install the required Python modules.

## How to run the Shopper Data Generator
### Generate a CSV of mock shopper data
1. In PyCharm, open the Terminal tab.
2. Run `python main.py generator --path shoppers.csv`
   - This command will generate a shoppers.csv file in the project folder containing this README.md file.
3. If you would like to specify a different configuration parameter than the default, or want to know what the default parameter values are, then run `python main.py generator --help` to see all of the optional parameters and their default values.

### Populate/Overwrite a MongoDB collection with mock shopper data
1. In PyCharm, open the Terminal tab.
2. Run `python main.py generator --collection shopper_data`
   - This command will populate a MongoDB database collection called shopper_data. If shopper_data already exists, then the contents will be overwritten.
3. If you would like to specify additional configuration parameters, or want to know what the default parameter values are, then run `python main.py generator --help` to see all of the optional parameters and their default values.

### Start the Shopper API
1. In PyCharm, open the Terminal tab.
2. Run `python main.py api`
3. Navigate to http://127.0.0.1:5000/
4. Swagger UI can be used to interact with the API.
   - Expand one of the controller
   - Click on a GET or POST method
   - Click Try it out
   - Fill in the values, then click Execute
   - The results are shown in the response section.
