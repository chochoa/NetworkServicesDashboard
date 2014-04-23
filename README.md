NetworkServicesDashboard
========================

Departmental dashboard for Network Services

This dashboard should currently be live at networkservices/ (networkservices.cisco.com). Documentation can be found at /help.

Should you wish to run this locally please clone the repository and install the dependencies listed in requirements.txt and then run the server:

    $ git clone git@github.com:RichLogan/NetworkServicesDashboard.git
    $ pip install -r requirements.txt
    $ python runServer.py

The application should be now running at http://0.0.0.0:80/ on a local development/debug server. To try a more Production-esque WebServer I highly reccomend using Gunicorn (should have already installed as a dependency):

    $ gunicorn networkServicesDashboard:app -b 0.0.0.0:80

Inside the /tools folder you will find a number of scripts that will help with deployment (SQL to create db tables, dumps to restore from, csv exports etc.) Please refer to the documentation at networkservices/help or inside the /docs folder for further guidance. */*/
