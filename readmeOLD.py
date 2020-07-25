#!/usr/bin/env python 
# -*- coding: utf-8 -*-

################################################################################
                        ##text to JSON##
'''reads text file and makes BCO. Use https://powerfulpython.com/blog/python-string-formatting/ for reference'''
################################################################################

import json, argparse, pprint

#infile = '/Users/hadley/GitHub/examples/glycosylation-sites-UniCarbKB.json'
#infile = '/Users/hadley/GitHub/experimental/untitled.json'
#infile = '/Users/hadley/GitHub/examples/HCV1a.json'
#bcoFile = '/Users/hadley/GitHub/blank-bco.json'

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
def parse( dic ):
    ''''''

    bco = dic

    prov = bco['provenance_domain']
    contributors, review = str(), str()
    for r in prov['review']:
        
        try: reviewer = '\n    ' + str(r['status'])+': '+ r['reviewer']['name']\
        +' ('+r['reviewer']['orcid']+')'+', '+ r['reviewer']['affiliation']+\
        '; '+ str(r['reviewer']['contribution'])
        
        except: reviewer = '\n    ' + str(r['status'])+': '+ r['reviewer']['name']\
        +', '+ r['reviewer']['affiliation']+'; '+ str(r['reviewer']['contribution'])
        review = review + reviewer

    for c in prov['contributors']:
        
        try: contributor = '\n    ' + str(c['name']+ ' (' + c['orcid']+ ')' \
         + '; ' + c['affiliation'] + ': ' + str(c['contribution']))
        
        except: contributor = '\n    ' + str(c['name'] + '; ' + c['affiliation']\
         + ': ' + str(c['contribution']))
        
        contributors = contributors + contributor
 
    try: start_time, end_time = prov['embargo']['start_time'], prov['embargo']['end_time']
    except: start_time, end_time = 'na', 'na'

    use = bco['usability_domain']
    usability = str()
    usability = '\n    ' + '\n    '.join('%s'%d for d in use)

    ext = bco['extension_domain']
    extension = ',    '.join('%s'%t for t in ext)

    des = bco['description_domain']
    keywords, references, steps = str(), str(), str()
    keywords = ', '.join('%s'%k for k in des['keywords'])

    for x in des['xref']:
        ids = ', '.join('%s'%d for d in x['ids'])
        reference = '\n    ' + str(x['name'] + '; ' + x['namespace']+'; ' + ids)
        references = references + reference

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

    exe = bco['execution_domain']
    scripts, uris, prereqs, dataEndpoints  = str(), str(), str(), str()
    for s in exe['script']:
        script = s['uri']['uri']+', '
        scripts = scripts + script

    for sp in exe['software_prerequisites']:
        for u in sp['uri']: 
            uri = str(u)+ ': '+str(sp['uri'][u])
        uris = uris+uri
        prereq = "\n    Name: %s    Version: %s  \n    URI: %s" % \
        ( sp['name'], sp['version'], uris)

        prereqs = prereqs + prereq

    for d in exe['external_data_endpoints']:

        dataEndpoint = "\n    Name: %s    URL: %s" % \
        (d['name'], d['url'])
        dataEndpoints = dataEndpoints + dataEndpoint

    io = bco['io_domain']
    inputfiles, outputFiles = str(), str()
    for item in io['input_subdomain']: 

        try: filename = item['uri']['filename']
        except: filename = '\t'

        try: uri = item['uri']['uri']
        except: uri = '\t'

        try: time = item['uri']['access_time']
        except: time = '\t'

        inputfile = "\n    Filename: %s    Access Time: %s  \n    URI: %s\n" % \
        ( filename, time, uri)

        inputfiles = inputfiles + inputfile
#    print inputfiles

    for out in io['output_subdomain']:
        
        try: media = out['mediatype']
        except: media = '\t'

        try: filename = out['uri']['filename']
        except: filename = '\t'

        try: uri = out['uri']['uri']
        except: uri = '\t'

        try: time = out['uri']['access_time']
        except: time = '\t'

        outputFile = "\n    Filename: %s    Media Type: %s    Access Time: %s  \n    URI: %s\n" % \
        ( filename, media, time, uri)
        outputFiles = outputFiles + outputFile
#    print outputFiles

    err = bco['error_domain']

    print 'Top Level\n',\
    '  BCO ID: ', bco['bco_id'],\
    '\n  Checksum: ',bco['checksum'],\
    '\n  Specification:', bco['bco_spec_version'], \
    '\nProvenance Domain',\
    '\n  Name:', prov['name'],\
    '\n  Version: ',prov['version'],\
    '\n  Review: ', review,\
    '\n  Created: ', prov['created'],\
    '\n  Modified: ', prov['modified'],\
    '\n  Embargo: ', 'Start:', start_time, 'End: ', end_time,\
    '\n  Contributors: ', contributors,\
    '\n  License: ', prov['license'],\
    '\nUsability Domain: ', usability,\
    '\nExtensions: ', extension,\
    '\nDescription Domain ',\
    '\n  Keywords:', keywords,\
    '\n  External References: (Name, Namespace, Ids)', references,\
    '\n  Platform: ', ', '.join('%s'%d for d in des['platform']),\
    '\n  Pipeline Steps: ', steps, \
    '\nExecution Domain:',\
    '\n  Scripts:', scripts,\
    '\n  Script Driver:', exe['script_driver'],\
    '\n  Software Prerequisites:'+ prereqs,\
    '\n  External Data Endpoints:', dataEndpoints, \
    '\n  Envornment Variables:', '\n   ',json.dumps(exe['environment_variables']),\
    '\nInput/output Domain:',\
    '\n  Input Subdomain:', inputfiles,\
    '\n  Output Subdomain:', outputFiles,\
    '\nError Domain:',\
    '\n  Empirical Error:', '\n ',json.dumps(err['empirical_error']),\
    '\n  Algorithmic Error:', '\n ',json.dumps(err['algorithmic_error'])

    #return my_bco
  # Contribution:
#______________________________________________________________________________#
def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('json', type=argparse.FileType('r'), help="json to convert")
    args = parser.parse_args()
    data = json.load(args.json)
    provenance_domain = ''
    usability_domain = ''
    extension_domain 
    description_domain 
    execution_domain 
    io_domain 
    error_domain
    parse(data)

#______________________________________________________________________________#
if __name__ == '__main__':
    main()