from flask import Flask, render_template, request, session, redirect, escape, url_for, Response
from functools import wraps
from contextlib import closing
import urllib
import urllib2
import siteSetup
import subprocess
import newrelic.agent

newrelic.agent.initialize('../newrelic.ini')
app = Flask(__name__)
app.config['DEBUG'] = True

import networkServicesDashboard.views