import xmlrpclib,datetime
wp_url = "https://enthusiastsports.wordpress.com/xmlrpc.php"
wp_username ="abhigenie92"
wp_password ="engrade12"
wp_blogid = ""

status_draft = 0
status_published = 1

server = xmlrpclib.ServerProxy(wp_url)

title = "Something New"
content = "Body "
date_now=str(datetime.datetime.today())[:-10]
print date_now
date_created = xmlrpclib.DateTime(datetime.datetime.strptime(str(date_now), "%Y-%m-%d %H:%M"))

categories = ["somecategory"]
tags = ["sometag", "othertag"]
data = {'title': title, 'description': content, 'dateCreated': date_created, 'categories': categories, 'mt_keywords': tags}

post_id = server.metaWeblog.newPost(wp_blogid, wp_username, wp_password, data, status_published)


