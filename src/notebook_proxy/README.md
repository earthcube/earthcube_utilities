# Make Notebook Proxy
This proxy creates a notebook in Google Collab from a template. The parameters extracted from the Scicence on Schema JSON-LD files, and sent to the proxy
/mknb

A docker container is built using github actions:

https://hub.docker.com/repository/docker/nsfearthcube/mknb

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

docker run -e GIST_TOKEN={YOUR TOKEN} -e GIST_USERNAME={YOU USERNAME}  -p 127.0.0.1:3031:3031 nsfearthcube/mknb:latest
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
 http://127.0.0.1:3031/

---
## Calling the Notebook Proxy

 http://127.0.0.1:3031/ should return an index.html

 http://127.0.0.1:3031/alive/ will let you know it's working.

http://127.0.0.1:3031/mknb/
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








