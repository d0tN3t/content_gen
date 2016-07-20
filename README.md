

**content_gen tracks the top news trends and generates a summary of related news articles.**
The top trending topics are extracted with the help of twitter's api. For each trending topic, highest similarity news articles from google news website are parsed and translated. The corresponding summaries of articles and key-words are generated with the help of tf-idf.


INSTALLATION:
==============
1. Install Anaconda Python 2.7 64 bit distribution
	Link: http://continuum.io/downloads#all
2. Clone to your desktop

	```
	git clone https://github.com/abhigenie92/content_gen

	```
3. Install dependencies
 	```
	sudo apt-get install libxslt-devel libxml2-devel gcc
	```

4. cd into this folder and run the following command from terminal

	```
	cd content_gen
	python -m pip install -r requirements.txt
	```
5. Install nltk libraries.

    ```
    python import nltk; nltk.download()
    ```
6. Run the main.py file.

	```
	python main.py
	```

OUTPUT:
==============
The output is appended in "\posts\content.json".
 	{'title': title of post, 'description': summary of given no. of lines, 'dateCreated': date of creation, 'categories': categories of post, 'mt_keywords': keywords of the post}

OTHERS:
==============
1. The script has an option of making it run inifinitely. It will keep checking if a new trend is available and it will posts only if there is.
	Uncomment lines 259-264
2.  The script is limited by twitter's rate limit and sleeps in btw till satisified.

