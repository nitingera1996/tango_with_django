import json
import urllib, urllib2

BING_API_KEY='RrVW0ULSIMUav1YQm+NA6f2sMX0Z1UjrOSUtOBdF/iA'

def run_query(search_terms):
    root_url="https://api.datamarket.azure.com/Bing/Search/"
    source="Web"
    results_per_page=10
    offset=0
    query = "'{0}'".format(search_terms)
    query = urllib.quote(query)
    search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(
        root_url,source,results_per_page,offset,query)
    username=""
    print search_url
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, search_url, username, BING_API_KEY)
    results=[]
    try:
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
		
        response = urllib2.urlopen(search_url).read()
		
        json_response = json.loads(response)
        #print json_response
        for result in json_response['d']['results']:
            #dict={'title':result['Title'],
            #'link':result['Url'],
            #'summary': result['Description']}
            #results.append(dict)
            results.append({
            'title': result['Title'],
            'link': result['Url'],
            'summary': result['Description']})
			
    except urllib2.URLError, e:
        print "Error when querying the Bing API: ",e
    #print results	
    return results
	
def main():
    print "Enter the query"
    str=raw_input(">")
    results=run_query(str)
    print results
    #for result in results:
     #   print result['title']
		
if __name__ == "__main__":
    main()