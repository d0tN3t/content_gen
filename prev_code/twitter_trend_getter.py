#https://wordpress.org/plugins/social-networks-auto-poster-facebook-twitter-g/
import tweepy,pdb,time,os,pickle,gnp,json,newspaper,requests,random,string,xmlrpclib,datetime,language_check,nltk,operator,urllib,praw
from topia.termextract import extract
from bs4 import BeautifulSoup
from langdetect import detect
from goose import Goose
from unidecode import unidecode
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import WhitespaceTokenizer
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
hdr = {'User-Agent': 'Mozilla/5.0'}
###########################################################################################################################################################

def get_trends_twitter():
	consumer_key = 'Zo4GxIwgb3DBkQiqTFKVXKdVT'
	consumer_secret = 'hVgYx2L00fX8ymBT89Q9FnCFCL4YKHd8cdH8yj6z01H1mIsVSu'
	access_token = '3243522126-02EWlFO4p7D0SmHLwepr0OM669KLFnkbZFDl3Kq'
	access_token_secret = 'Nx4e7VRNSOQPoOnzECw25GuiN13jXmw3LLCY2dVRk3ov7'
	# OAuth process, using the keys and tokens
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
	#print api.rate_limit_status()
	placeids=[23424975]#,23424977,23424748,23424916,23424775,23424942,23424948,23424803,23424848,	23424768] 
	countries=['uk']#,'us','aus','newzealand','canada','southafrica','singapore','ireland','india','brazil']
	hashtags_muiltple_regions=[]
	for index,each in enumerate(placeids):
		print countries[index]
		country_now=countries[index]
		trends1 = api.trends_place(each) # from the end of your code
		# trends1 is a list with only one element in it, which is a 
		# dict which we'll put in data.
		data = trends1[0] 
		# grab the trends
		trends = data['trends']
		# grab the name from each trend
		names = [trend['name'] for trend in trends]
		# put all the names together with a ' ' separating them
		trendsName = ' '.join(names)
		hashtags = [x['name'] for x in trends1[0]['trends'] if x['name'].startswith('#')]
		for hashtag in hashtags:
			hashtag=hashtag.strip('#')
			hashtags_muiltple_regions.append(str(unidecode(hashtag)))
		time.sleep(1)	
	return hashtags_muiltple_regions

def store_trends(trends_list):
	new_trends=[]
	#file read from directory
	current_path=os.path.dirname(os.path.realpath(__file__))
	current_path=current_path+'\\trends_till_now.p'
	#check if file exists
	if os.path.exists(current_path):
		file=open(current_path)
		stored_trends_list = pickle.load(file)
		file.close()
	else: 
		stored_trends_list=[]
	#append new items to the list	
	for item in trends_list:
		if item not in stored_trends_list:
			new_trends.append(item)
			stored_trends_list.append(item)
	#write items to pickle file\
	lp = pickle.dumps(stored_trends_list)
	fh = open('trends_till_now.p', 'w')
	fh.write(lp)
	fh.close()
	return new_trends

def urlsandtitles(trend):
	jsonobject = gnp.get_google_news_query(trend)
	stories=jsonobject['stories']
	urls=[]
	titles=[]
	for each in stories:
		url=each['link']
		title=each['title']
		if check_lang(url):
			urls.append(url)
			titles.append(title)
	return urls,titles

def checkfeasibletrend(new_trends):
	for trend in new_trends:
		urls,titles=urlsandtitles(trend)
		if len(urls) > 3:
			if len(urls) > 5:
				urls_parse_length=5
			else:	
				urls_parse_length=len(urls)
			summary,keywords=extract_summary_keywords(trend,urls[:urls_parse_length],titles)
			title=extract_title(titles)
			if(summary.count('.') > 7):
				post_url='https://enthusiastsports.wordpress.com/?p='+write_post_to_wordpress(summary,title,keywords)
				print post_url
				post_social_media(post_url,summary,title,keywords)


def	post_social_media(post_url,summary,title,keywords):
	pass

def write_post_to_wordpress(summary,title,keywords):
	date_now=str(datetime.datetime.today())[:-10]
	date_created = xmlrpclib.DateTime(datetime.datetime.strptime(str(date_now), "%Y-%m-%d %H:%M"))
	categories = [country_now]
	data = {'title': title, 'description': summary, 'dateCreated': date_created, 'categories': categories, 'mt_keywords': keywords}
	if os.exists("posts")==False:
		os.mkdir("posts")
	json.dump(d, open("text.txt",'w'))
	#post_id = server.metaWeblog.newPost(wp_blogid, wp_username, wp_password, data, status_published)
	return post_id

def extract_title(titles):
	short_titles=[]
	if len(titles) >5:
		titles=titles[:5]
	for each in titles:
		if "..." not in each:
			short_titles.append(unidecode(each))
	if len(short_titles)==0:
		short_titles=titles

	title_index=random.randint(0, len(short_titles)-1)
	title=replacesynonym(short_titles[title_index])
	title=string.capwords(title.replace("_"," "))
	matches = tool.check(title)
	correct_title=language_check.correct(title, matches)
	return correct_title

def extract_summary_keywords(trend,urls,titles): 
	sentences_count=12
	total_articles_content=extract_text(urls)
	keywords=extract_keywords_from_all_text(total_articles_content,titles)
	current_path=os.path.dirname(os.path.realpath(__file__))
	current_path=current_path+'\\'+trend+'.txt'
	with open(current_path, 'w') as the_file:
	 	the_file.write(total_articles_content)
	parser = PlaintextParser.from_file(current_path, Tokenizer(LANGUAGE))
	os.remove(current_path)
	sentences=''
	for sentence in summarizer(parser.document, sentences_count):
		sentences=sentences+' '+str(sentence) 
	replaced_syn=replacesynonym(sentences)
	matches = tool.check(sentences)
	correct_summary=language_check.correct(sentences, matches)
	return correct_summary,keywords
	#return sentences	  

def extract_keywords_from_all_text(total_articles_content,titles):
	x= sorted(extractor_keyword(total_articles_content))
	dict_key={}
	for each in x:
		i=0
		key=each[0]
		tokens=nltk.word_tokenize(key)
		tokens=[s.translate(None, string.punctuation) for s in tokens]
		tokens=filter(None, tokens)
		for token in tokens:
			for title in titles:
				if token in title:
					i+=1
		dict_key[key]=i
	keywords=dict(sorted(dict_key.iteritems(), key=operator.itemgetter(1), reverse=True)[:3]).keys()
	return keywords

def extract_text(urls):
	total_articles_content=''
	for url in urls:
		page_content_html,check = tries(url,7)
		if check:
			article = extractor.extract(raw_html=page_content_html)
			text = unidecode(article.cleaned_text)
			total_articles_content=total_articles_content+' '+text
		return total_articles_content	


def tries(url, max_tries):
	check=False
	for ty in range(1, max_tries+1):
		try:
			req = requests.get(url)
			page_content = req.content
			check=True
			break
		except requests.exceptions.ConnectionError as e:
			print("Error {} for try {}".format(e, ty))
			page_content=""
	return page_content,check

def replacesynonym(text):
	c=WhitespaceTokenizer().tokenize(text)
	outputty = ''
	for word in c:
		syn = wordnet.synsets(word)
		if word not in stops and syn:
			pdb.set_trace()
			outputty+=' '+syn[0].lemma_names[0]
		else:
			outputty +=' ' +word
	return outputty

def check_lang(url):
	html,check = tries(url,7)
	if check:
		soup = BeautifulSoup(html)
		for script in soup(["script", "style"]):
			script.extract()    
			text = soup.get_text()
			lines = (line.strip() for line in text.splitlines())
			chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
			text = '\n'.join(chunk for chunk in chunks if chunk)
			try :
				return 'en'==detect(unidecode(text))
			except langdetect.lang_detect_exception.LangDetectException:
				return False
		else:
			return False 
country_now=''
stops = set(stopwords.words('english')+['I'])
LANGUAGE = "english"
stemmer = Stemmer(LANGUAGE)
summarizer = Summarizer(stemmer)
summarizer.stop_words = get_stop_words(LANGUAGE)
tool = language_check.LanguageTool('en-US')
extractor = Goose()
wp_url = "https://enthusiastsports.wordpress.com/xmlrpc.php"
wp_username = "abhigenie92"
wp_password = "engrade12"
wp_blogid = ""
status_draft = 0
status_published = 1
server = xmlrpclib.ServerProxy(wp_url)
extractor_keyword = extract.TermExtractor()

latest_trends=get_trends_twitter()
new_trends=store_trends(latest_trends)
checkfeasibletrend(new_trends)