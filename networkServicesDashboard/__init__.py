import os
from flask import Flask, render_template, request, session, redirect, escape, url_for, Response
from werkzeug.utils import secure_filename
app = Flask(__name__)
import networkServicesDashboard.views