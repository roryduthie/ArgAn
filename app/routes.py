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

@application.route('/form', methods=['POST'])
def my_form_post():
    #iat_mode = 'false'
    text = request.form['text']
    #iat_mode = request.form['iat_mode']
    session['text_var'] = text
    #session['iat_mode'] = iat_mode
    return redirect('/results/overview')

@application.route('/results/participant')
def participant_results():

    text = session.get('text_var', None)
    check = check_analytics(text)

    raw_cog = get_pcogency_raw(text)
    parts = len(raw_cog)

    cog_div = get_pcogency_vis(text)
    corr_div = get_pcorrectness_vis(text)
    coh_div = get_pcoherence_vis(text)
    inter_div = get_interaction_vis(text)


    return render_template('participant.html', parts = parts, cog_placeholder = Markup(cog_div), corr_placeholder = Markup(corr_div), coh_placeholder = Markup(coh_div), inter_placeholder = Markup(inter_div))

@application.route('/results/hyp')
def event_hyp_results():

    text = session.get('text_var', None)
    check = check_analytics(text)

    hevy_div = get_hyp_evidence_vis(text)
    agent_div = get_hyp_agent_vis(text)
    object_div = get_hyp_object_vis(text)
    event_div = get_event_vis(text)
    location_div = get_event_location_vis(text)

    raw_stats = get_raw_stats(text)
    hyp_count = get_hyps(raw_stats)

    raw_events = get_raw_events(text)
    events = len(raw_events)


    return render_template('event.html', hevy_placeholder = Markup(hevy_div), agent_placeholder = Markup(agent_div), object_placeholder = Markup(object_div), hyps = hyp_count, events = events, event_placeholder = Markup(event_div), location_placeholder = Markup(location_div))

@application.route('/results/overview')
def render_text():
    text = session.get('text_var', None)
    check = check_analytics(text)

    html = get_centrality_vis(text)
    jsn = get_centrality_vis_cloud(text)
    stats_html = get_statistics_vis(text)
    s_node_time = get_s_node_timeline_vis(text)
    cogency_html = get_cogency_vis(text)
    coherence_html = get_coherence_vis(text)
    correctness_html = get_correctness_vis(text)
    div_html = get_div_vis(text)
    div_json = get_div_vis_cloud(text)
    appeal_html = get_appeal_vis(text)
    popularity_html = get_popularity_vis(text)


    raw_stats = get_raw_stats(text)

    prop_count, loc_count, RA_count, CA_count, MA_count = get_stats(raw_stats)


    #At this point also pull the raw data so we can easily toggle

    return render_template('an-home.html', div_placeholder=Markup(html), cloud_jsn=jsn, stats_placeholder = Markup(stats_html), s_time_placeholder = Markup(s_node_time), cogency_placeholder = Markup(cogency_html), coherence_placeholder = Markup(coherence_html),correctness_placeholder = Markup(correctness_html), mas=MA_count, cas=CA_count, ras=RA_count, props=prop_count, locs=loc_count, appeal_placeholder = Markup(appeal_html),popularity_placeholder = Markup(popularity_html),divis_placeholder = Markup(div_html), cloud_div=div_json)

def get_stats(json_array):
    prop_count = 0
    loc_count = 0
    RA_count = 0
    CA_count = 0
    MA_count = 0

    for stat in json_array:
        if stat['type'] == 'RA':
            RA_count = stat['count']
        if stat['type'] == 'CA':
            CA_count = stat['count']
        if stat['type'] == 'MA':
            MA_count = stat['count']

        if stat['type'] == 'I-node':
            prop_count = stat['count']
        if stat['type'] == 'Locution':
            loc_count = stat['count']
    return prop_count, loc_count, RA_count, CA_count, MA_count

def get_hyps(json_array):
    hyp_count = 0


    for stat in json_array:
        if stat['type'] == 'YA' and stat['text'] == 'Hypothesising':
            hyp_count = stat['count']
    return hyp_count

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

def get_statistics_vis(ID):
    url = 'http://arganbackend.arg.tech/statistics-vis/'

    url = url + str(ID)

    with urllib.request.urlopen(url) as response:
        html = response.read()
        html = html.decode('utf-8')
    return html

def get_s_node_timeline_vis(ID):
    url = 'http://arganbackend.arg.tech/s-node-timeline-vis/'

    url = url + str(ID)

    with urllib.request.urlopen(url) as response:
        html = response.read()
        html = html.decode('utf-8')
    return html

def get_cogency_vis(ID):
    url = 'http://arganbackend.arg.tech/cogency-vis/'

    url = url + str(ID)

    with urllib.request.urlopen(url) as response:
        html = response.read()
        html = html.decode('utf-8')
    return html

def get_coherence_vis(ID):
    url = 'http://arganbackend.arg.tech/coherence-vis/'

    url = url + str(ID)

    with urllib.request.urlopen(url) as response:
        html = response.read()
        html = html.decode('utf-8')
    return html

def get_correctness_vis(ID):
    url = 'http://arganbackend.arg.tech/correctness-vis/'

    url = url + str(ID)

    with urllib.request.urlopen(url) as response:
        html = response.read()
        html = html.decode('utf-8')
    return html

def get_raw_stats(ID):
    url = 'http://arganbackend.arg.tech/statistics-raw/'

    url = url + str(ID)

    with urllib.request.urlopen(url) as response:
        jsn = json.load(response)
    return jsn

def get_raw_events(ID):
    url = 'http://arganbackend.arg.tech/hevy-event-raw/'

    url = url + str(ID)

    with urllib.request.urlopen(url) as response:
        jsn = json.load(response)
    return jsn



def get_div_vis(ID):

    url = 'http://arganbackend.arg.tech/divisiveness-vis/'

    url = url + str(ID)

    with urllib.request.urlopen(url) as response:
        html = response.read()
        html = html.decode('utf-8')
    return html

def get_div_vis_cloud(ID):
    url = 'http://arganbackend.arg.tech/divisiveness-cloud-vis/'

    url = url + str(ID)

    with urllib.request.urlopen(url) as response:
        jsn = json.load(response)
    return jsn

def get_appeal_vis(ID):

    url = 'http://arganbackend.arg.tech/appeal-vis/'

    url = url + str(ID)

    with urllib.request.urlopen(url) as response:
        html = response.read()
        html = html.decode('utf-8')
    return html

def get_popularity_vis(ID):

    url = 'http://arganbackend.arg.tech/popularity-vis/'

    url = url + str(ID)

    with urllib.request.urlopen(url) as response:
        html = response.read()
        html = html.decode('utf-8')
    return html

def get_hyp_evidence_vis(ID):

    url = 'http://arganbackend.arg.tech/hevy-hyp-evidence-vis/'

    url = url + str(ID)

    with urllib.request.urlopen(url) as response:
        html = response.read()
        html = html.decode('utf-8')
    return html

def get_hyp_agent_vis(ID):

    url = 'http://arganbackend.arg.tech/actor-vis/'

    url = url + str(ID)

    with urllib.request.urlopen(url) as response:
        html = response.read()
        html = html.decode('utf-8')
    return html

def get_hyp_object_vis(ID):

    url = 'http://arganbackend.arg.tech/object-vis/'

    url = url + str(ID)

    with urllib.request.urlopen(url) as response:
        html = response.read()
        html = html.decode('utf-8')
    return html

def get_event_vis(ID):

    url = 'http://arganbackend.arg.tech/hevy-event-vis/'

    url = url + str(ID)

    with urllib.request.urlopen(url) as response:
        html = response.read()
        html = html.decode('utf-8')
    return html

def get_event_location_vis(ID):

    url = 'http://arganbackend.arg.tech/event-location-vis/'

    url = url + str(ID)

    with urllib.request.urlopen(url) as response:
        html = response.read()
        html = html.decode('utf-8')
    return html

def get_pcogency_raw(ID):

    url = 'http://arganbackend.arg.tech/pcogency-raw/'

    url = url + str(ID)

    with urllib.request.urlopen(url) as response:
        jsn = json.load(response)
    return jsn

def get_pcogency_vis(ID):

    url = 'http://arganbackend.arg.tech/pcogency-vis/'

    url = url + str(ID)

    with urllib.request.urlopen(url) as response:
        html = response.read()
        html = html.decode('utf-8')
    return html


def get_pcorrectness_vis(ID):

    url = 'http://arganbackend.arg.tech/pcorrectness-vis/'

    url = url + str(ID)

    with urllib.request.urlopen(url) as response:
        html = response.read()
        html = html.decode('utf-8')
    return html


def get_pcoherence_vis(ID):

    url = 'http://arganbackend.arg.tech/pcoherence-vis/'

    url = url + str(ID)

    with urllib.request.urlopen(url) as response:
        html = response.read()
        html = html.decode('utf-8')
    return html


def get_interaction_vis(ID):

    url = 'http://arganbackend.arg.tech/interaction-vis/'

    url = url + str(ID)

    with urllib.request.urlopen(url) as response:
        html = response.read()
        html = html.decode('utf-8')
    return html






