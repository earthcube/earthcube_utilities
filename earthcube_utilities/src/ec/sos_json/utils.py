import json
from string import Template

from pyld import jsonld

jsonld_context = context = { "@vocab": "https://schema.org/"}


def compact_jld_str(jld_str):
    doc = json.loads(jld_str)
    compacted = jsonld.compact(doc, jsonld_context)
    r = json.dumps(compacted, indent=2)
    return r


def formatted_jsonld(jld_str, form="compact", schemaType="Dataset"):
    if (form == 'jsonld'):
        return jld_str

    elif (form == "frame"):
        frame = (' {\n'
                 '              "@context": {\n'
                 '                "@vocab": "https://schema.org/",\n'
                 '                    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",\n'
                 '                    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",\n'
                 '                    "schema": "https://schema.org/",\n'
                 '                    "xsd": "http://www.w3.org/2001/XMLSchema#"\n'
                 '              },\n'
                 '              "@type": "schema:${schemaType}"\n'
                 '  }\n '
                 )
        f_template = Template(frame)
        thsGraphQuery = f_template.substitute(schemaType=schemaType)

        frame_doc = json.loads(thsGraphQuery)
        doc = json.loads(jld_str)

        framed = jsonld.frame(doc, frame_doc)

        r = json.dumps(framed, indent=2)
        return r
    else: # compact
        doc = json.loads(jld_str)
        compacted = jsonld.compact(doc, jsonld_context)
        r = json.dumps(compacted, indent=2)
        return r