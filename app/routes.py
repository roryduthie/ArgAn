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
    text = request.form['text']
    #iat_mode = request.form['iat_mode']
    session['text_var'] = text
    #session['iat_mode'] = iat_mode
    return redirect('/results')

@app.route('/results')
def render_text():
    text = session.get('text_var', None)
    check = check_analytics(text)

    html = get_centrality_vis(text)
    jsn = get_centrality_vis_cloud(text)

    #At this point also pull the raw data so we can easily toggle

    return render_template('an-home.html', div_placeholder=Markup(html), cloud_jsn=jsn)

def check_analytics(ID):
    return ''

def get_centrality_vis(ID):

    url = 'http://arganbackend.arg.tech/eigen-cent-vis/'

    url = url + str(ID)

    with urllib.request.urlopen(url) as response:
        html = response.read()
        html = html.decode('utf-8')
    return html

def get_centrality_vis_cloud(ID):
    url = 'http://arganbackend.arg.tech/eigen-cent-cloud-vis/'

    url = url + str(ID)

    with urllib.request.urlopen(url) as response:
        jsn = json.load(response)
    return jsn

