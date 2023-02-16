import logging
from io import StringIO

import sparqldataframe

context = "@prefix : <https://schema.org/> ."

def get_summary4repo(endpoint):
    file = '../resources/sparql/summary_query.txt'
    with open(file, 'r') as f:
        lines = f.read()
    df = sparqldataframe.query(endpoint,lines)
    return df

def summaryDF2ttl(df, repo):
    "summarize sparql qry (or main quad store)s ret DataFrame, as triples in ttl format w/g as the new subj"
    urns = {}
    import json
    def is_str(v):
        return type(v) is str

    #with open(f'{repo}.ttl', "w") as f:
    f = StringIO()
    f.write(f'{context}\n')
    for index, row in df.iterrows():
        logging.debug(f'dbg:{row}')
        gu=df["g"][index]
        #skip the small %of dups, that even new get_summary.txt * has
        there = urns.get(gu)
        if not there:
            urns[gu]=1
        elif there:
            #print(f'already:{there},so would break loop')
            continue #from loop
        #rt=row['resourceType']
        rt_=row['resourceType']
        rt=rt_.replace("https://schema.org/","")
        logging.debug(f'rt:{rt}')
        name=json.dumps(row['name']) #check for NaN/fix
        if not name:
            name=f'""'
        if not is_str(name):
            name=f'"{name}"'
        if name=="NaN": #this works, but might use NA
            name=f'"{name}"'
        description=row['description']
        if is_str(description):
            sdes=json.dumps(description)
            #sdes=description.replace(' / ',' \/ ').replace('"','\"')
            #sdes=sdes.replace(' / ',' \/ ').replace('"','\"')
          # sdes=sdes.replace('"','\"')
        else:
            sdes=f'"{description}"'
        kw_=row['kw']
        if is_str(kw_):
            kw=json.dumps(kw_)
        else:
            kw=f'"{kw_}"'
        pubname=row['pubname']
        #if no publisher urn.split(':')
        #to use:repo in: ['urn', 'gleaner', 'summoned', 'opentopography', '58048498c7c26c7ab253519efc16df237866e8fe']
        #as of the last runs, this was being done per repo, which comes in on the CLI, so could just use that too*
        if pubname=="No Publisher":
            ul=gu.split(':')
            if len(ul)>4: #could check, for changing urn more, but for now:
                #pub_repo=ul[3]
                pub_repo=ul[4]
                if is_str(pub_repo):
                    pubname=pub_repo
                else: #could just use cli repo
#                        global repo
                    pubname=repo
        datep=row['datep']
        if datep == "No datePublished":
            datep=None
        placename=row['placenames']
        s=row['subj']
        f.write(" \n")
        f.write(f'<{gu}>\n')
        #print(f'        a {rt} ;')
        if rt == "tool":
            f.write(f'        a :SoftwareApplication ;\n')
        else:
            f.write(f'        a :Dataset ;\n')
       #print(f'        :name "{name}" ;')
        f.write(f'        :name {name} ;\n')
       #print(f'        :description """{description}""" ;')
       #print(f'        :description """{sdes}""" ;')
        f.write(f'        :description ""{sdes}"" ;\n')
       #print(f'        :keyword "{kw}" ;')
       #print(f'        :keyword {kw} ;') #not what schema.org &the new query uses
        f.write(f'        :keywords {kw} ;\n')
        f.write(f'        :publisher "{pubname}" ;\n')
        f.write(f'        :place "{placename}" ;\n')
        if datep:
            f.write(f'        :date "{datep}" ;\n') #might be: "No datePublished" ;should change in qry, for dv's lack of checking
        f.write(f'        :subjectOf <{s}> .\n')
        #du= row.get("disurl") #not seeing yet
        du= row.get('url') # check now/not yet
        if is_str(du):
            f.write(f'        :distribution <{du}> .\n')
        mlat= row.get('maxlat') # check now/not yet
        if is_str(mlat):
            f.write(f'        :latitude {mlat} .\n')
        mlon= row.get('maxlon') # check now/not yet
        if is_str(mlon):
            f.write(f'        :longitude {mlon} .\n')
        encodingFormat= row.get('encodingFormat') # check now/not yet
        if is_str(encodingFormat):
            f.write(f'        :encodingFormat {encodingFormat} .\n')
        #see abt defaults from qry or here, think dv needs date as NA or blank/check
        #old:
        #got a bad:         :subjectOf <metadata-doi:10.17882/42182> .
        #incl original subj, just in case for now
        #lat/lon not in present ui, but in earlier version

        #### end for ####
    return f.getvalue()