from flask import render_template, request, redirect, session, Markup
from . import application
import pandas as pd
from urllib.request import urlopen
from app.centrality import Centrality
import requests
import json
import urllib
import tempfile
import os
import uuid


@application.route('/')
@application.route('/index')
def index():
    return redirect('/form')

@application.route('/form')
def my_form():
    return render_template('index.html')
