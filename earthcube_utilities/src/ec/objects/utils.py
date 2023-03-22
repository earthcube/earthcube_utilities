
def parts_from_urn(urn):
    parts = urn.split(':')
    id = parts[len(parts)-1]
    repo = parts[len(parts)-2]
    org = parts[len(parts)-3] ## new identifier will have an org identifier

    return {"id": id, "repo":repo, "org":org}