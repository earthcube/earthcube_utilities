#!/usr/bin/env python3
# mknb.py has all the gist/colab w/caching, and working service,  clean&hook up soon

"""
RUN
* flask run

REQUIRED ENV
* AUTH_MODE - service, apitoken  (aka user)
* GIST_TOKEN - application token from Github
* GIST_USERNAME - Github Username for applicaiton token
GITHUB_OAUTHSECRET = GITHUB APP Secret
GITHUB_OAUTHCLIENTID = GIHUB Client ID
"""
# dwv 2021-10-08 added env varaibles, and error checks when missing.
#       worked to used embedded papermill to issues with parameter passing
#       pass parameter for templates

# 1st cut at a version of mknb.py that can handle sending in(differing)ext info to the new template
# &right now, just incl the tgy.py gist-mgt which should not only to the post but look up cached gists,returing colab urls

# start to prototype the code to create a NB, that will become a gist; that uses a template but inserts the url to open
# then the UI will open the url for this file, and it won't have to be taken from the nb-url in the nb
# and if it is a gist, can be opened in colab directly; rob liked a rendered gist after suggesting nbpreview
# dwnurl  = "https://darchive.mblwhoilibrary.org/bitstream/1912/23805/1/dataset-753388_hhq-chlorophyll__v1.tsv"
# dwnurl="https://darchive.mblwhoilibrary.org/bitstream/1912/26532/1/dataset-752737_bergen-mesohux-2017-dissolved-nutrients__v1.tsv"
# now turn this into a flask service that take the dwnurl

# plan is to inject the url into a template and write it to fn, so a direct link2it can come from the search gui

# used: https://github.com/nteract/papermill to inject the url, &can run it too

# base_url = "http://141.142.218.86:8081/notebooks/"  #was when I tested a jupyterhub intemediate;maybe binder friendly too
# will mv them below post_gist so they can call that and return the colab-nb vs the testing/jupyterhub one

# import urllib.parse #mostly want safe filenames v url's right now, but enough overlap worth using

# =original gist code: ;now only testing, rm-soon
import csv
import json
import pathlib

import pandas
from authlib.oauth2.rfc6749 import OAuth2Token


def tpg(fn="https/darchive.mblwhoilibrary.org_bitstream_1912_26532_1_dataset-752737_bergen-mesohux-2017-dissolved-nutrients__v1.tsv.ipynb"):  # test
    r = post_gist(fn)
    print(r)


# ==will replace this w/tgy.py code, that includes finding a fn in the gitsts, vs remaking it

import os
import sys
import urllib.parse
import papermill as pm
from os import path
import tempfile

from flask import Flask, redirect, session, jsonify, make_response
from flask import request
from flask import g, url_for, render_template
from flask_ipban import IpBan
from werkzeug.middleware.proxy_fix import ProxyFix
from authlib.integrations.flask_client import OAuth
from functools import wraps
import markdown
import markdown.extensions.fenced_code

from requests_toolbelt import MultipartEncoder
import gistyc


# (x) Need username for GIST tokent
# (x) need template path so papermill can find things. use OS path?
# (x) need to write to temp directory, if possible, or clean up on exit
# use development flag for the cleanup.
# should we just hash the name... would be simpler, because we want to pass multiple files to a notebook for a run.
# (x) be able to pass a different template, or pull from a repo/url.
## (implemented temp file) can papermill to memory file reads, or be embedded to do such things?


def first_str(s):
    r = s.split(' ', 1)
    return r[0]


AUTH_MODE = os.getenv('AUTH_MODE')
AUTH_TOKEN = os.getenv('GIST_TOKEN')
AUTH_USER = os.getenv('GIST_USERNAME')
GITHUB_OAUTHSECRET = os.getenv('GITHUB_SECRET')
GITHUB_OAUTHCLIENTID = os.getenv('GITHUB_CLIENTID')

# useEC=None #"yes"
# if useEC:
#     AUTH_TOKEN=os.getenv('ec_gist_token') #for when post to earthcube gists, soon
# else:
#     AUTH_TOKEN=os.getenv('gist_token')
# if AUTH_TOKEN==None or AUTH_USER == None:
#     print("Error set a GIST_TOKEN and GIST_USERNAME env variable ")
#     print("e.g. docker run -e GIST_TOKEN={YOUR TOKEN} -e GIST_USERNAME={YOU USERNAME}  -p 127.0.0.1:3031:3031 nsfearthcube/mknb:latest")
#     print("or set in docker-compose or kubernetes secrets")
#     exit(1)
# https://github.com/ThomasAlbin/gistyc
if AUTH_MODE == None:
    print("Error set a AUTH_MODE env variable ")
    print(
        "e.g. docker run -e AUTH_MODE={service||apikey} -e GITHUB_SECRET={GITHUB_OAUTHCLIENTID} -e GITHUB_CLIENTID={YOU GITHUB_OAUTHSECRET}  -p localhost:3031:3031 nsfearthcube/mknb:latest")
    print("or set in docker-compose or kubernetes secrets")
    exit(1)
elif AUTH_MODE == "service":
    if GITHUB_OAUTHSECRET == None or GITHUB_OAUTHCLIENTID == None:
        print("Error set a GITHUB_SECRET and GITHUB_CLIENTID env variable ")
        print(
            "e.g. docker run -e AUTH_MODE=service -e GITHUB_SECRET={GITHUB_OAUTHCLIENTID} -e GITHUB_CLIENTID={YOU GITHUB_OAUTHSECRET}  -p localhost:3031:3031 nsfearthcube/mknb:latest")
        print("or set in docker-compose or kubernetes secrets")
        exit(1)
elif AUTH_MODE == "apikey":
    if AUTH_TOKEN == None or AUTH_USER == None:
        print("Error set a GITHUB_SECRET and GITHUB_CLIENTID env variable ")
        print(
            "e.g. docker run -e AUTH_MODE=apikey -e AUTH_USER={USER} -e AUTH_TOKEN={YOU GITHUB_APIKEY}  -p localhost:3031:3031 nsfearthcube/mknb:latest")
        print("or set in docker-compose or kubernetes secrets")
        exit(1)
else:
    print('Uknown AUTH_MODE')
    exit(1)




def gist_api(token):
        if AUTH_MODE == "service":
            token = session.get('token')
            apikey = token['access_token']
            return gistyc.GISTyc(auth_token=apikey)
        elif AUTH_MODE == "apikey":
            token = session.get('token')
            return  gistyc.GISTyc(auth_token=token)


# Initiate the GISTyc class with the auth token
# gist_api = gistyc.GISTyc(auth_token=AUTH_TOKEN)

# in mknb called post_gist, could call create_
# def mk_gist(fn):
def post_gist(fn, collection=None):
    fcu = find_gist(fn)
    if fcu:
        print(f'found saved gist:{fn}')
        return fcu
    else:
        # return gist_api.create_gist(file_name=fn)
        print(f'file_name={fn}')
        filename = pathlib.Path(fn)
        gistFile = open(fn, 'r')
        obj = gistFile.read()
        notebookFilename = os.path.basename(fn)
        # files = ("ec_gist", obj, "application/vnd.jupyter")

        if collection != None:
            # fileRes = [("files",
            #             ("ec_gist", obj, "application/vnd.jupyter"),
            #             ("datasets.json", executionParameters, "application/vnd.jupyter"),
            #             )
            #            ]
            files = {notebookFilename: {"content": obj},
                     "zzdatasets.json": {"content": str(collection)}}
            # gist is titled after the first file, and not renamable.
        else:
            # fileRes = [("files", ("ec_gist", obj, "application/vnd.jupyter"))]
            files = {notebookFilename: {"content": obj}}
        fields = {"public": True,
                  "description": f'Earthcube Gist:{fn}',
                  "files": files
                  }
        # encoder = MultipartEncoder(fields)
        # headers = {'Content-Type': encoder.content_type}
        token = session.get('token')
        g_api = gist_api(token)
        g = g_api.create_gist(file_name=fn)
        # token = session.get('token')
        # j=json.dumps(fields )
        # g = oauth.github.post('gists', token=token, data=j, )
        # if (g.status_code == 201):
        #     createdGist = g.json()
        #     cu = colab_url(createdGist['id'], notebookFilename)
        #     hcu = htm_url(cu)
        #     return hcu
        cu = colab_url(g['id'], notebookFilename)
        hcu = htm_url(cu)
        return hcu

        # could look up url, but find should do it, also makes sure it's there/in a way
        fcu = find_gist(notebookFilename)
        print(f'found-made-gist:{fcu}')
        return fcu


# def update_gist(fn): #might come into play later
#     return gist_api.update_gist(file_name=fn)

# Get a list of GISTs
# this before auth prevents running.
# gist_list = gist_api.get_gists()
# g=gist_list #could get this in each fnc that needs it, or leave it global
# g=None #just reset in flask app before calling mknb fnc
# might need to update in other places, maybe even w/in find_gist

def file_ext(fn):
    st = os.path.splitext(fn)
    return st[-1]


def path_leaf(path):
    import ntpath
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def gist_fn(gj):
    return list(gj['files'].keys())[0]


def colab_url(gist_id, fn):
    # if useEC:
    #     return 'https://colab.research.google.com/gist/earthcube/' + gist_id + "/" + fn
    # else:
    #     return 'https://colab.research.google.com/gist/valentinedwv/' + gist_id + "/" + fn
    #     return 'https://colab.research.google.com/gist/mchenry/' + gist_id + "/" + fn
    username = session.get('user')
    return f'https://colab.research.google.com/gist/{username}/{gist_id}/{fn}'


def htm_url(url):
    # return f"""<html><head><meta http-equiv = "refresh" content = "0; url={url}" /></head><body><a href={url}>notebook to view your data</a></body></html>"""
    return f"""<html><head><meta http-equiv = "refresh" content = "0; url={url}" /></head><body><a href={url}>nb</a></body></html>"""


def htm_url_(url):  # old1before fwd to colab-NB-url
    return f'<html><a href={url}>notebook to view your data</a></html>'


def print_nb_gists(g):  # was used before writing find_gist
    for gn in range(len(g)):
        fn = gist_fn(g[gn])
        ft = file_ext(fn)
        if (ft == '.ipynb'):
            print("Gist URL : %s" % (g[gn]['url']))
            # print("GIST ID: %s"%(g[gn]['id']))
            gist_id = (g[gn]['id'])
            print(f'GIST_ID:{gist_id}')
            print(f'fn: {fn}')
            cu = colab_url(gist_id, fn)
            print(f'url: {cu}')
        else:
            print(f'it was of type:{ft}')


# print_nb_gists(g)
# ffn = 'darchive.mblwhoilibrary.org_bitstream_1912_23805_1_dataset-753388_hhq-chlorophyll__v1.tsv.ipynb'

# be able to find a fn w/in the list: g
# def find_gist(ffn):
def find_gist(ffnp):
    ffn = path_leaf(ffnp)
    token = session.get('token')
    g_api = gist_api(token)
    g = g_api.get_gists()  # was in global but refresh here

    # token = session.get('token')
    # res = oauth.github.get('gists', token=token)
    #g = res.json()
    # TODO, look for response 200... if not throw error
    for gn in range(len(g)):
        fn = gist_fn(g[gn])
        if (ffn == fn):
            gist_id = (g[gn]['id'])
            cu = colab_url(gist_id, fn)
            hcu = htm_url(cu)
            return hcu
    return None  # don't want2end w/o a ret


# fcu = find_gist(ffn)
# print(f'fn has a nb:{fcu}')

# will need to find a way to post to 'earthcube' gists
# ==
# change dwnurl to path for the nb that pagemill makes, so if we see it again, it can just reuse cached version
def dwnurl2fn(dwnurl):
    # #fn = dwnurl.replace("/","_").replace(":__","/",1) + ".ipynb"
    # #fn = dwnurl.replace("/","_").replace(":__","/",1).replace("?","") + ".ipynb"
    fn = dwnurl.replace("/", "_").replace(":__", "/", 1).replace("?", "").replace("#", "<hash>") + ".ipynb"
    # #fn = dwnurl.replace("/","_").replace(":__","/",1).replace("?","").replace("#","_").replace(" ; ","_") + ".ipynb"
    return fn


# papermill can read templates from different sources. https://github.com/nteract/papermill/blob/3002e9f4ca221eed8286116e26b0bd8d15114a1f/papermill/iorw.py#L421
# so if template name starts will approved name (http://github) then pass that
# otherwise join with template path

def templateUri(templateName):
    if templateName.startswith("http://") or templateName.startswith("https://"):  # catches github, too.
        return templateName
    else:
        basedir = os.path.abspath(os.path.dirname(__file__))
        template_file = os.path.join(basedir, f'templates/{templateName}')
        return template_file


# pagemill insert param&run the NB
# def pm(dwnurl, fn):
def pm_nb(collection, template=None, filename="temp.ipynb"):
    dwn_url= None
    ext = None
    urn = None
    query_q = None
    if collection.get("datasets") != None:
        dwn_url = collection["datasets"][0].get("downloadurl")
        ext = collection["datasets"][0].get("ext")
        urn = collection["datasets"][0].get("urn")
        dwnurl = dwn_url.replace('/', '')
        fn = dwnurl2fn(dwnurl)
        temp_dir = tempfile.gettempdir()
        fn = os.path.join(temp_dir, fn)
    if collection.get("query") != None:
        query_q = collection["query"].get("q")

    # basedir = os.path.abspath(os.path.dirname(__file__))
    # template_file = os.path.join(basedir, f'templates/{template}')
    template_file = templateUri(template)
    # dont try reusung until we get the naming issues resolved. Templates named after datasets, so if user changes
    # template, old template is used.
    e = None
    try:
        e = pm.execute_notebook(  # not env sure we need to have e. https://github.com/nteract/papermill
            template_file,  # 'templates/template.ipynb', #path/to/input.ipynb',
            filename,  # 'path/to/output.ipynb',
            parameters=dict(url=dwn_url, ext=ext, urn=urn, q=query_q),
            prepare_only=True,
            log_output=True
        )
    except Exception as err:
        print(f'except:{err}')  # might have to catch this exception
        raise err
    print(f'pm:{e}')  # might have to catch this exception
    # if path.exists(fn):
    #     print(f'reuse:{fn}')
    # else: #could use the template.ipynb w/o cached data, if the 1st try w/'mybinder-read-pre-gist.ipynb' fails
    #     e = None
    #     try:
    #         e = pm.execute_notebook( #  not env sure we need to have e. https://github.com/nteract/papermill
    #            template_file, # 'templates/template.ipynb', #path/to/input.ipynb',
    #            fn,  #'path/to/output.ipynb',
    #            parameters = dict(url=dwn_url, ext=ext, urn=urn, prepare_only=True, log_output=True)
    #         )
    #     except Exception as err:
    #         print(f'except:{err}') #might have to catch this exception
    #     print(f'pm:{e}') #might have to catch this exception
    # return base_url + fn
    return post_gist(filename, collection)  # htm w/link to colab of the gist

    # above had problems(on1machine), so have cli backup in case:


def pm_nb3(dwn_url, ext=None, urn=None):
    dwnurl = dwn_url.replace('/', '')
    fn = dwnurl2fn(dwnurl)
    if path.exists(fn):
        print(f'reuse:{fn}')
    else:
        if ext:
            # #sext=ext.replace(" ","_").replace("(","_").replace(")","_")
            # #sext=ext.replace(" ","_").replace("(","_").replace(")","_").replace(";","_") #make this safer
            # #sext=ext.replace(" ","_").replace("(","_").replace(")","_").replace(";"," ") #make this safer
            # #sext=ext.replace(" ","_").replace("(","_").replace(")","_").replace(";"," ").replace("\n",' ')
            # sext=ext.replace(" ","_").replace("(","_").replace(")","_").replace(";","_").replace("\n",' ')
            # sext1=first_str(sext)
            # sext1 = urllib.parse.quote_plus(ext)
            # print(f'ext:{sext},1:{sext1}')
            # ext_arg=f' -p ext {sext1} '
            sext1 = ext.strip()
            print(f'ext:{ext},1:{sext1}')
            ext_arg = f' -p ext "{sext1}" '
        else:
            ext_arg = ""
        if urn:
            urn_arg = f' -p urn "{urn}" '
        else:
            urn_arg = ""
        # cs=f'papermill --prepare-only template.ipynb {fn} -p contenturl {dwnurl} {ext_arg} {urn_arg}'
        cs = f'papermill --prepare-only src/notebook_proxy/templates/template.ipynb {fn} -p url {dwnurl} {ext_arg} {urn_arg}'
        print(cs)
        os.system(cs)
    return post_gist(fn)


# def pm2(dwnurl, fn):
# def pm_nb2(dwn_url, ext=None):

def mknb(collection, template=None):
    "url2 pm2gist/colab nb"
    if collection is None or len(collection["datasets"]) < 1:
        r = f'bad-parameter:no datasets or empty datasets'
    dwnurl_str = collection["datasets"][0].get("downloadurl")
    ext = collection["datasets"][0].get("ext")
    urn = collection["datasets"][0].get("urn")
    if (dwnurl_str and dwnurl_str.startswith("http")):
        # fn=dwnurl2fn(dwnurl_str) #already done in pm_nb
        # r=pm_nb(dwnurl_str, ext)
        # r=pm_nb2(dwnurl_str, ext)
        # r=pm_nb3(dwnurl_str, ext, urn)
        ## r = pm_nb(dwnurl_str, ext, urn, template)
        dwnurl = dwnurl_str.replace('/', '')
        fn = dwnurl2fn(dwnurl)
        temp_dir = tempfile.gettempdir()
        fn = os.path.join(temp_dir, fn)
        r = pm_nb(collection, template, fn)
    else:
        r = f'bad-url:{dwnurl_str}'
    return r


##############
# Server
#   imports move to top of file
################
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

oauth = OAuth(app)
ip_ban = IpBan(ban_seconds=200)
ip_ban.init_app(app)
blockip = os.getenv("blockip")
if blockip:
    ip_ban.block(blockip)
app.wsgi_app = ProxyFix(app.wsgi_app, x_prefix=1)


###
## Auth
#########
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # if g.user is None:
        if (AUTH_MODE == 'service'):
            if session.get('token') is None:
                return redirect(url_for('login', next=request.url))
        else:
            session['token'] = AUTH_TOKEN
            session['user'] = AUTH_USER

        return f(*args, **kwargs)

    return decorated_function


github = None
if (AUTH_MODE == 'service'):
    oauth.register(
        name='github',
        client_id=GITHUB_OAUTHCLIENTID,
        client_secret=GITHUB_OAUTHSECRET,
        access_token_url='https://github.com/login/oauth/access_token',
        access_token_params=None,
        authorize_url='https://github.com/login/oauth/authorize',
        authorize_params=None,
        api_base_url='https://api.github.com/',
        client_kwargs={'scope': 'gist,read:user'},
    )
    github = oauth.create_client('github')


# else:
#    github = oauth.create_client('github')

@app.route('/login')
def login():
    session['next'] = request.args.get('next') or '/'
    redirect_uri = url_for('auth', _external=True)
    return oauth.github.authorize_redirect(redirect_uri)


@app.route('/auth')
def auth():
    token = oauth.github.authorize_access_token()
    if token:
        session['token'] = token
    user = oauth.github.get('user', token=token)
    if user.status_code == 200:
        u = user.json()
        userlogin = u.get('login')
        session['user'] = userlogin
    return redirect(session.get('next'))


@app.route('/logout')
def logout():
    session.pop('token', None)
    return redirect('/')


#### #############
## Notebook Proxy
##############
@app.route('/')
def template():
    user = session.get('user')
    return render_template('index.html', user=user)


@app.route('/readme')
def readme():
    readme_file = open("README.md", "r")
    md_template_string = markdown.markdown(
        readme_file.read(), extensions=["fenced_code"]
    )

    return md_template_string


@app.route('/mknb/')  # works, but often have2rerun the clicked link2get rid of errors
@login_required
def mk_nb():
    # dwv setup userauth
    token = session.get('token')
    g_api = gist_api(token)
    # gist_api = gistyc.GISTyc(auth_token=access_token)
    # gist_api = gistyc.GISTyc(auth_token=token)
    # "make a NoteBook"
    dwnurl_str = request.args.get('url', type=str)
    print(f'url={dwnurl_str}')
    ext = request.args.get('ext', default='None', type=str)
    print(f'ext={ext}')
    urn = request.args.get('urn', default='None', type=str)
    print(f'urn={urn}')
    template = request.args.get('template', default='template.ipynb', type=str)
    print(f'template={template}')
    collection_parameter = {}
    collection_parameter["datasets"] = [{"urn": urn, "ext": ext, "downloadurl": dwnurl_str}]
    # r= mknb(dwnurl_str,ext,urn, template)
    r = mknb(collection_parameter, template)
    return r

@app.route('/mkQ/')
@login_required
def mk_Q():
    "make a NoteBook"
    q = request.args.get('q',  type = str)
    print(f'q={q}')
    template = request.args.get('template', default='sparql.ipynb', type=str)
    print(f'template={template}')
    #r= mkQ(q) #just pagemill directly
    #r= pm_q3(q)
    collection_parameter = {}
    collection_parameter["query"] = {"q": q,}
    fn = "q_" + q + ".ipynb"
    temp_dir = tempfile.gettempdir()
    fn = os.path.join(temp_dir, fn)
    r = pm_nb(collection_parameter, template,fn)
    return r

@app.route('/logbad/')  # have try/except, so log errors soon, also have 'log' file in NB from wget/etc
def log_bad():
    dwnurl_str = request.args.get('url', type=str)
    lbs = f'log_bad:url={dwnurl_str}'
    print(lbs)  # just in the log for now
    err = request.args.get('error', default='None', type=str)
    if err:
        print(f'error:{err}')
    else:
        err = ""
    return err


@app.route('/alive/')
def alive():
    return "alive"


@app.route('/gists/')
@login_required
def gists():
    token = session.get('token')
    # test if oauth and gistcyn ca work in tandem
    g_api =gist_api(token)
    gists =g_api.get_gists()
    # token = OAuth2Token.find(
    #     name='github',
    #     user=request.user
    # )
    # API URL: https://api.github.com/user/repos
    #resp = oauth.github.get('gists', token=token)

    # API URL: https://api.github.com/user/repos
    # resp = oauth.github.get('user')
    #resp.raise_for_status()
   # gists = resp.json()
    return jsonify({'gists': gists})

# in mknb2, https://github.com/earthcube/ec/blame/master/NoteBook/mknb2.py
# there are several formats:
#  * get_graph (json)
# * /get_graph_jld/ (jsonld)
# * /get_graph_tsv/ (tsv)
# * /get_graph_csv/ (csv)
#  * get_graph_csv_g/ (csv) with more error checking that get_graph_csv

## CLEAN CODE NEEDED:
# we will need to import the completed ec_utilities, and the manage graph.
# query the graphstore using that code
# RDF to jsonld is in earthcube_utilities/ec/sos_json/rdf.py
## def get_rdf2jld(urn, endpoint, form="jsonld", schemaType="Dataset"):
## use form="frame"
## swear: this will break because there are types other than Dataset that might be returned.
# so use form="compact"

@app.route('/get_graph/<g>/<format>')
def get_graph(g,format="jsonld"):
    #format = request.args.get('format', type=str)
    # g = request.args.get('g',  type = str)
    # print(f'g={g}')
    # the return form EC is a sparqldataframe
    #r= ec.get_graph(g)
    r=get_mock_graph(g)
    #print(r)

    if format =="json":
        resp = make_response(r.to_json(), 200)
        resp.headers['Content-Type'] = 'application/json'
        return resp
    elif format =="jsonld":
        return  "Format not yet implemented: json-ld" , 400
    elif format=="csv":
        resp = make_response(r.to_csv(encoding='utf-8',lineterminator='\n',index=False,quoting=csv.QUOTE_NONNUMERIC), 200)
        resp.headers['Content-Type'] = 'text/csv'
        return resp
    elif format=="tsv":
        resp = make_response(r.to_csv( sep='\t', encoding='utf-8',lineterminator='\n',index=False,quoting=csv.QUOTE_NONNUMERIC),
                         200)
        resp.headers['Content-Type'] = 'text/tab-separated-values'
        return resp
    else:
        return  "Uknonwn format:"+format , 400

## placeholder for a working ec.get_graph(g)
# returns a dataframe that is from a summary record.
def get_mock_graph(g):
    file = './resources/summarydf_short.csv'
    # with open(file, 'r') as f:
    #     testdf = f.read()
    testdf = pandas.read_csv(file)
    return testdf

if __name__ == '__main__':
    if (len(sys.argv) > 1):
        dwnurl_str = sys.argv[1]
        if (len(sys.argv) > 2):
            ext = sys.argv[2]
        else:
            ext = None
        # g = gist_api.get_gists() #set the global w/fresh value
        r = mknb(dwnurl_str, ext)  # or trf.py test, that will be in ipynb template soon
        print(r)
    else:  # w/o args, just to run a service:
        # app.run(host='0.0.0.0', port=8004, debug=True)
        app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
        app.config['SESSION_TYPE'] = 'filesystem'

        # sess.init_app(app)
        app.run(host='0.0.0.0', port=3031, debug=True)

# this works, incl pm&gist caches, &now flask works too
# remember diff btw dwnurl_str, filename-path, &filename alone, &what gets compared to find_gist
# dv said he will have in a container, so will need token evn var, and http/s dirs, for now
