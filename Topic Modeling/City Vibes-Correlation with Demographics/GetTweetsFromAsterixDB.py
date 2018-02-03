import pycurl

import string

from StringIO import StringIO



c = pycurl.Curl()

buffer = StringIO()



print("started")



#my_query="""use%20dataverse%20TwitterDataverse%0Afor%20%24x%20in%20dataset%20Tweets%0Areturn%20%24x"""

my_query="use%20dataverse%20TwitterDataverse%20for%20%24x%20in%20dataset%20Tweets%20where%20not(is-null(%24x.coordinates))%20return%20%24x"



#============ input: format: "IP:PORT"

ip_and_port='10.44.1.70:19002'

print  'http://'+ip_and_port+'/aql?aql='+my_query

c.setopt(c.URL, 'http://'+ip_and_port+'/aql?aql='+my_query+'&wrapper-array=false')

c.setopt(c.WRITEDATA, buffer)

c.perform()

c.close()   

#write results to file

body = buffer.getvalue()

f=open("all.txt","w")

f.write(body)

f.close()



print "Done"


