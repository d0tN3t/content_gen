INSTALLATION:
1. Install Anaconda Python 2.7 64 bit distribution
	Link: http://continuum.io/downloads#all	
2. cd into this folder and run the following command from terminal
	python -m pip install -r requirements.txt
3. Run the Main.py file.

OUTPUT:
1. The output is appended in "\posts\content.json". 
 	{'title': title of post, 'description': summary of given no. of lines, 'dateCreated': date of creation, 'categories': categories of post, 'mt_keywords': keywords of the post}

OTHERS:
1. The script has an option of making it run inifinitely. It will keep checking if a new trend is available and it will posts only if there is.
	Uncomment lines 259-264
2.  The script is limited by twitter's rate limit and sleeps in btw till satisified.

