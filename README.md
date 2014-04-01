NetworkServicesDashboard
========================

Departmental dashboard for Network Services

This dashboard should currently be live at networkservices/ (networkservices.cisco.com). Documentation can be found at /help.

Should you wish to run this locally please instal the dependencies listed in requirements.txt and then run the following from the project's root directory:

$ python runServer.py

The application should be now running at http://127.0.0.1:5000/

Inside the /tools folder you will find a number of scripts that will help with deployment (SQL to create db tables, dumps to restore from, csv exports etc.) Please refer to the documentation at networkservices/help or inside the /docs folder for further guidance. 