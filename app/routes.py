from flask import render_template, request, redirect, session, Markup
from . import app
import pandas as pd
from urllib.request import urlopen
from app.centrality import Centrality
import requests
import json
import urllib
import tempfile
import os
import uuid


@app.route('/')
@app.route('/index')
def index():
    return redirect('/form')

@app.route('/form')
def my_form():
    return render_template('index.html')

@app.route('/form', methods=['POST'])
def my_form_post():
    #iat_mode = 'false'
    #text = request.form['text']
    #iat_mode = request.form['iat_mode']
    #session['text_var'] = text
    #session['iat_mode'] = iat_mode
    return redirect('/results')

@app.route('/results')
def render_text():
    return render_template('an-home.html')
