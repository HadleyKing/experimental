#!/usr/bin/env python 
# -*- coding: utf-8 -*-

################################################################################
                        ##text to JSON##
'''reads text file and makes BCO.'''
################################################################################

import json, argparse

parser = argparse.ArgumentParser()
parser.add_argument('json', type=argparse.FileType('r'), help="json to convert")
args = parser.parse_args()
data = json.load(args.json)
#______________________________________________________________________________#
def jsonload( file ):
    '''loads a bco file'''

    with open(file, 'rU') as file:
        bco = json.load(file)
    return bco
#______________________________________________________________________________#
def parse_top( dic ):
    """Pulls the top level fields from the BCO"""
    data = dic
    top = ''
    
    top = 'Top Level\n' + 'BCO ID:\t'+ data['object_id']\
    + '\nE-Tag:\t' + data['etag']\
    + '\nSpecification:\t' + data['spec_version']
    
    return top
#______________________________________________________________________________#
def parse_prov( dic ):
    """"""

    prov = dic
    contributors, review = str(), str()
    for r in prov['review']:

        try: reviewer = '\n\t' + str(r['status'])+' by '+ r['reviewer']['name']\
        +' ('+r['reviewer']['orcid']+')'+', '+ r['reviewer']['affiliation']+\
        '; '+ str(', '.join(r['reviewer']['contribution']))
        
        except: reviewer = '\n\t' + str(r['status'])+' by '+ r['reviewer']['name']\
        +', affiliated with '+ r['reviewer']['affiliation']+'; '+ str(', '.join(r['reviewer']['contribution']))
        review = review + reviewer

    for c in prov['contributors']:
        
        try: contributor = '\n    ' + str(c['name']+ ' (' + c['orcid']+ ')' \
         + '; ' + c['affiliation'] + ': ' + str(', '.join(c['contribution'])))
        
        except: contributor = '\n    ' + str(c['name'] + '; ' + c['affiliation']\
         + ': ' + str(', '.join(c['contribution'])))

        contributors = contributors + contributor
 
    try: start_time, end_time = prov['embargo']['start_time'], prov['embargo']['end_time']
    except: start_time, end_time = 'na', 'na'
    
    provenance = 'Provenance Domain:'\
    + '\n  Name:\t' + prov['name']\
    + '\n  Version:\t' + prov['version']\
    + '\n  Review:\t' + review\
    + '\n  Contributors: ' + contributors\
    + '\n  Created: ' + prov['created']\
    + '\t  Modified: '+ prov['modified']\
    + '\n  Embargo\t' + 'Start: ' + start_time + '\tEnd: ' + end_time\
    + '\n  License: ' + prov['license']

    return provenance
#______________________________________________________________________________#
def parse_usability( dic ):
    """"""

    use = dic
    usability = str()
    usability = 'Usability Domain:\n    ' + '\n    '.join('%s'%d for d in use)
    return usability
#______________________________________________________________________________#
def parse_extension( dic ):
    """"""

    extension = dic
    extensionD = str()
    ext = {}

    for e in extension:
        ext = json.dumps(e)
        ext = ext.replace('"','')
        ext = ext.replace('[','\n\t')
        ext = ext.replace('{','\n\t')
        ext = ext.replace(',','\n\t')
        ext = ext.replace(']','\n\t')
        ext = ext.replace('}','\n\t')
        extensionD = extensionD + str(ext)

    extensionD = "Extension Domain:\n" + extensionD
    return extensionD
#______________________________________________________________________________#
def parse_description( dic ):
    """"""

    des = dic
    keywords, references, steps = str(), str(), str()
    keywords = "  Keywords\t" + ', '.join('%s'% k for k in des['keywords'])

    for x in des['xref']:
        ids = "\tIdentifiers\t"+', '.join('%s'% d for d in x['ids'])
        reference = '\n    Name\t' + str(x['name'] + '\tName Space\t' + x['namespace'] + ids)
        references = references + reference
    references = "\n  External References\t" + references

    for p in des['pipeline_steps']:

        inp, out = '', ''

        for i in p['input_list']: 
            inp = inp + ' ' + i['uri'] 

        for o in p['output_list']: 
            out = out + ' ' + o['uri']

        try: step = "\n    Step %d: %s\n    Version: %s  Description: %s \n    Input List: %s \n    Output List: %s" % \
        (p['step_number'], p['name'], p['version'], p['description'], inp, out)

        except: step = "\n    Step %d: %s\n    Version: %s  Description: %s \n    Input List: %s \n    Output List: %s" % \
        (p['step_number'], p['name'], 'NA', p['description'], inp, out)
        steps = steps + step
        
    steps = "\n  Pipeline Steps" + steps

    descriptionD = 'Description Domain:\n' \
    + keywords + references + steps
        
    return descriptionD
#______________________________________________________________________________#
def parse_execution( dic ):
    """"""

    exe = dic
    en_vars, scripts, uris, prereqs, dataEndpoints  = str(), str(), str(), str(), str()
    for s in exe['script']:
        script = s['uri']['uri']+', '
        scripts = scripts + script

    for sp in exe['software_prerequisites']:
        for u in sp['uri']: 
            uri = "%s\t%s\t"% (u, sp['uri'][u])
            uris = uris+uri
        prereq = "\n    Name: %s    Version: %s  \n    URI Object:\n      %s"% \
        ( sp['name'], sp['version'], uris)

        prereqs = prereqs + prereq

    for d in exe['external_data_endpoints']:
        dataEndpoint = "\n\tName\t%s\tURL\t%s" % \
        (d['name'], d['url'])
        dataEndpoints = dataEndpoints + dataEndpoint
    
    for var in exe['environment_variables']:
        en_var = "\n    %s\t%s" % \
        (var, exe['environment_variables'][var])
        en_vars = en_vars + en_var

    executionD = "Execution Domain:\n" \
        + "  Scripts: " + scripts \
        + "\n  Script Driver: " + exe['script_driver'] \
        + "\n  Software Prerequisites: " + prereqs \
        + "  \n  External Data Endpoints:" + dataEndpoints \
        + "\n  Environment Variables:" + en_vars

    return executionD
#______________________________________________________________________________#
def parse_param( dic1, dic2 ):
    """"""

    param = dic1
    des = dic2
    name = {}
    paraD = str()

    for d in des['pipeline_steps']:
        name[d['step_number']] = d['name']

    for p in param:

        para = "  %s\t%s\t%s\n" % (name[int(p['step'])], p['param'], p['value'])
        paraD = paraD + para

    paraD = "Parametric Domain:\n"+paraD
    return paraD
#______________________________________________________________________________#
def parse_io( dic ):
    """"""

    io = dic
    inputfiles, outputFiles = str(), str()
    for item in io['input_subdomain']:

        try: filename = item['uri']['filename']
        except: filename = '\t'

        try: uri = item['uri']['uri']
        except: uri = '\t'

        try: time = item['uri']['access_time']
        except: time = '\t'

        inputfile = "    Filename: %s    Access Time: %s  \n    URI: %s\n" % \
        ( filename, time, uri)

        inputfiles = inputfiles + inputfile

    for out in io['output_subdomain']:

        try: media = out['mediatype']
        except: media = '\t'

        try: filename = out['uri']['filename']
        except: filename = '\t'

        try: uri = out['uri']['uri']
        except: uri = '\t'

        try: time = out['uri']['access_time']
        except: time = '\t'

        outputFile = "\n    Filename: %s    Media Type: %s    Access Time: %s  \n    URI: %s" % \
        ( filename, media, time, uri)
        outputFiles = outputFiles + outputFile
    
    ioD =  "Input/output Domain:" + "\n  Input Subdomain:\n"\
        + inputfiles + "  Output Subdomain:" + outputFiles

    return ioD
#______________________________________________________________________________#
def parse_err( dic ):
    """"""

    err = dic
    
    empD ='  Empirical Error:\n\t' + json.dumps(err['empirical_error'])
    empD = empD.replace('"','')
    empD = empD.replace('[','\n\t')
    empD = empD.replace('{','\n\t')
    empD = empD.replace(',','\n\t')
    empD = empD.replace(']','\n\t')
    empD = empD.replace('}','\n\t')

    algoD = '\n  Algorithmic Error:\n\t' + json.dumps(err['empirical_error'])
    algoD = algoD.replace('"','')
    algoD = algoD.replace('[','\n\t')
    algoD = algoD.replace('{','\n\t')
    algoD = algoD.replace(',','\n\t')
    algoD = algoD.replace(']','\n\t')
    algoD = algoD.replace('}','\n\t')

    errD = 'Error Domain:\n'+empD + algoD
    return errD
#______________________________________________________________________________#
def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('json', type=argparse.FileType('r'), help="json to convert")
    args = parser.parse_args()
    data = json.load(args.json)
    top = parse_top(data)
    provenance = parse_prov(data['provenance_domain'])
    usability = parse_usability(data['usability_domain'])
    extension = parse_extension(data['extension_domain'])
    description = parse_description(data['description_domain'])
    execution = parse_execution(data['execution_domain'])
    try: para = parse_param(data['parametric_domain'], data['description_domain'])
    except: para = ''
    io = parse_io(data['io_domain'])
    error = parse_err(data['error_domain'])
    json.dumps(data['error_domain'])
    print(top)
    print(provenance)
    print(usability)
    print(extension)
    print(description)
    print(execution)
    print(para)
    print(io)
    print(error)

#______________________________________________________________________________#
if __name__ == '__main__':
    main()