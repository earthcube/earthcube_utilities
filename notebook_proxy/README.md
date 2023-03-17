# Make Notebook Proxy
This proxy creates a notebook in Google Collab from a template. The parameters extracted from the Scicence on Schema JSON-LD files, and sent to the proxy
/mknb

For testing, running locally works well.

In production, a container is utilized. This is created by a github workflow, (containerize.yaml)

## Calling the Notebook Proxy

 http://localhost:3031/ should return the index.html

 http://localhost:3031/alive/ will let you know it's working.

http://localhost:3031/mknb/
This proxy creates a notebook in Google Collab from a template. The parameters extracted from the Scicence on Schema JSON-LD files, and sent to the proxy
/mknb
* url - url of the resource
* ext - encoding format of the resource.
* urn - urn geocodes urn. 
* template -- name of the template file to render. (optional: default: template.ipynb)

Note about url, urns, ext:
A hash in the name of the item causes the rest of the url passed to be ignored.
To avoid this, we custom encode '#' as &lt;hash&gt;

so:

`ext=http://linked.earth/ontology/core/1.2.0/index-en.html#Dataset`

becomes:

`ext=http://linked.earth/ontology/core/1.2.0/index-en.html<hash>Dataset`


## Development:

### install ec utiltites in development mode
```python
python -m pip install -e ec ../earthcube_utilities

```

```python
python -m pip install -e bar @ git+https://github.com/earthcube/earthcube_utilities.git
```

```python
python -m pip install -e ec /path/to/earthcube_utilities

```

### start
In order to use oauth, you need to setup a github app, and set the following environment variables

GITHUB_OAUTHSECRET = GITHUB APP Secret
GITHUB_OAUTHCLIENTID = GIHUB Client ID


```shell
cd src/notebook_proxy
flask mknb
```
this will start it at:
 http://localhost:5000/

```shell
cd src/notebook_proxy
python mknb.py
```
 http://localhost:3031/

## Docker 
A docker container is built using github actions:

https://hub.docker.com/repository/docker/nsfearthcube/mknb

Note need to update to https://github.com/tiangolo/uwsgi-nginx-flask-docker

---
## Setting up a developer access token
before use you need a token:
* go to settings>developer settings.
* personal access token
* create a token with gist permissions.

---
## command to install a container for local use:
```
docker pull nsfearthcube/mknb:latest

docker run -e GITHUB_CLIENTID={GITHUB OAUTH APP} -e GITHUB_SECRET={GITHUB OAUTH APP SECRET}  -p 127.0.0.1:3031:3031 nsfearthcube/mknb:latest
```


---
# For docker compose:
Need notes here.

--- 
# Local Build
You can build locally from the earthcube_utilities directory

```%  docker build .``` 

```%  docker images``` 
```% docker images
REPOSITORY          TAG       IMAGE ID       CREATED          SIZE
<none>              <none>    1f0ebd17e990   22 minutes ago   959MB
``` 
image id is: 1f0ebd17e990

``` docker run -e GIST_TOKEN={YOUR TOKEN} -e GIST_USERNAME={YOU USERNAME}  -p 127.0.0.1:3031:3031 {image id}``` 

Proxy is now running at:
 http://localhost:3031/

try:
http://localhost:3031/mknb?url=http://lipdverse.org/Temp12k/1_0_2/Svartvatnet-Norway.Seppa.2009.lpd&ext=application%2Fzip%20%3B%20http%3A%2F%2Flinked.earth%2Fontology%2Fcore%2F1.2.0%2Findex-en.html%3Chash%3EDataset&urn=urn:gleaner:milled:lipdverse:509e465d0793506b237cea8069c3cb2d276fe9c2&encoding=application%2Fzip%20%3B%20http%3A%2F%2Flinked.earth%2Fontology%2Fcore%2F1.2.0%2Findex-en.html%3Chash%3EDataset&

---


### Testing and development notes


from raw.github
http://localhost:5000/mknb?url=http://lipdverse.org/Temp12k/1_0_2/Svartvatnet-Norway.Seppa.2009.lpd&ext=application%2Fzip%20%3B%20http%3A%2F%2Flinked.earth%2Fontology%2Fcore%2F1.2.0%2Findex-en.html%3Chash%3EDataset&urn=urn:gleaner:milled:lipdverse:509e465d0793506b237cea8069c3cb2d276fe9c2&encoding=application%2Fzip%20%3B%20http%3A%2F%2Flinked.earth%2Fontology%2Fcore%2F1.2.0%2Findex-en.html%3Chash%3EDataset&template=https://raw.githubusercontent.com/earthcube/NotebookTemplates/geocodes_template/GeoCODEStemplates/ARGO/SA_01_Argo_Data_Exploration.ipynb

http://localhost:5000/mknb?url=http://lipdverse.org/Temp12k/Svartvatnet-Norway.Seppa.2009.lpd&ext=application%2Fzip%20%3B%20http%3A%2F%2Flinked.earth%2Fontology%2Fcore%2F1.2.0%2Findex-en.html%3Chash%3EDataset&urn=urn:gleaner:milled:lipdverse:509e465d0793506b237cea8069c3cb2d276fe9c2&encoding=application%2Fzip%20%3B%20http%3A%2F%2Flinked.earth%2Fontology%2Fcore%2F1.2.0%2Findex-en.html%3Chash%3EDataset&template=https://github.com/earthcube/NotebookTemplates/blob/geocodes_template/GeoCODEStemplates/Development/2_numpy.ipynb








