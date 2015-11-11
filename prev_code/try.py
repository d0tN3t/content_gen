import xmlrpclib,datetime
date_now=str(datetime.datetime.today())[:-10]

date_created = xmlrpclib.DateTime(datetime.datetime.strptime(str(date_now), "%Y-%m-%d %H:%M"))
print date_created