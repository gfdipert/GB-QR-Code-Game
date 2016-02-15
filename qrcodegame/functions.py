from qrcode.main import QRCode
import urllib
import os

def createqrstuff(form):
	form = form
	outputQRCodes(form)
	outputHTML(form)

def getoutfolder(guide_id):
	global outfolder
	outfolder = "/tmp/qrcodegame/" + guide_id
	if not os.path.exists(outfolder):
		result = os.makedirs(outfolder)
		if not os.path.isdir(outfolder):
			raise Exception("Output folder does not exist and could not be created.")
	return outfolder

def outputQRCodes(form):
	"""Create QR codes for phrase pieces."""
	delimiter = '/'
	components = form['phrase'].value().split(delimiter)
	title = urllib.quote(form['page_title'].value())
	position = 0
	global count
	count = 0
	#creates QR codes for every phrase
	for component in components:
		format_str = "http://guidebook.com/guide/%s/web/?title=%s&dataSource=%s%%3Fs%%3D%s%%26l%%3D%s"
		letters = component.lstrip()
		prepend = len(component) - len(letters)
		letters = letters.rstrip()
		url_string = format_str % (form['guide_id'].value(), form['page_title'].value(), form['html'].value(), prepend+position, urllib.quote(urllib.quote(letters)))
		print "Generating QR code for URL: %s" % url_string
		position += len(component) # Use the len including spaces so we skip the proper amt
		makeQR(url_string, "%s_%s.png"%(count+1,letters), form)
		count = count + 1
	makeQR("http://guidebook.com/guide/%s/web/?title=%s&dataSource=%s%%3Freset%%3Dtrue" % (form['guide_id'].value(), form['page_title'].value(), form['html'].value()), 'reset.png', form)

def makeQR(url, filename, form):
	"""Create and save QR code for phrase piece."""
	outfolder = getoutfolder(form['guide_id'].value())
	qr = QRCode()
	qr.add_data(url)
	im = qr.make_image()
	im.save(outfolder+"/"+filename, 'png')

def outputHTML(form):
	"""Create output HTML file based on input arguments.
	
	Two versions of the output text are provided below. One includes
	a hyperlink for completed text once the game is completed.
	
	"""
	delimiter = '/'
	phrase = form['phrase'].value().replace(delimiter,"")
	spaces = ""
	for letter in phrase:
		if letter != " ":
			letter = "_"
		spaces+=letter
	# Add seperate HTML file text if they want a form to appear after phrase is completed
	if form['completedurl'].value() != 'NONE':
		html = """	<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
				<meta name="viewport" content="width=device-width; initial-scale=1.0; maximum-scale=1.0; user-scalable=0;">
				<style>
					html, body{
						background-color:#f9f9f9;
					}
					*{
						font-family:"Helvetica Neue", "Helvetica", Arial, sans-serif;
					}
					.container{
						padding:10px;
						text-align:center;
					}
					.logo{
						background:transparent url(logo.png) left top no-repeat;
						width:153px;
						height:125px;
						background-size:153px 125px;
						-webkit-background-size:153px 125px;
						-moz-background-size:153px 125px;
						background-size:153px 125px;
						margin:20px auto 50px auto;
					}
					#phrase{
						font-size:20px;
						font-weight:bold;
						color:#aaa;
					}
					#phrase .letters{
						color:#444;
					}
					.instructions{
						font-size:12px;
						color:#666;
						background-color:#eee;
						display:inline-block;
						padding:20px;
						border-radius:5px;
						margin-top:50px;
						box-shadow:0 1px 1px rgba(0,0,0,.12);
					}
					.instructions strong{
						display:block;
						font-size:14px;
					}
					
					a{
						text-decoration: none;
						color:#40b4fa;
					}
				</style>
			</head>
			<body>
				<div class="container">
					<div class="logo"></div>
					<div id="phrase">%(spaces)s</div>
					<p class="instructions">
						<strong>%(message_title)s</strong>
						%(message)s
					</p>
				</div><!-- end container-->
				<script>
					var phrase = "%(spaces)s";
					var qs = getQueryString();
					var startIndex = parseInt(qs['s']);
					var letters = decodeURIComponent(qs['l']);
					var reset = qs['reset'];
					var storedPhrase = window.localStorage["%(storage_key)s"];
					var cookiePhrase = readCookie("%(storage_key)s");
					if(storedPhrase == undefined && cookiePhrase != null)
						storedPhrase = cookiePhrase;
					if(cookiePhrase == null && storedPhrase != undefined)
						cookiePhrase = storedPhrase;
					var phraseElement = document.getElementById('phrase');
					if(isNaN(startIndex) || !letters) {
						startIndex = 0;
						letters = '';
					}
					if(!storedPhrase || reset == 'true') {
						phrase = fillInLetters(phrase, startIndex, letters);
					}
					else {
						phrase = fillInLetters(storedPhrase, startIndex, letters);
					}
					window.localStorage["%(storage_key)s"] = phrase;
					createCookie("%(storage_key)s", phrase, 365);
					phraseElement.innerHTML = htmlFormat(phrase);
					function fillInLetters(phrase, startIndex, letters) {
						var newPhrase = phrase.slice(0, startIndex) + letters + phrase.slice(startIndex + letters.length)
						return newPhrase;
					}
					function htmlFormat(phrase) {
						var newPhrase = phrase.replace(/([^_ ]+)/g, '<span class="letters">$&</span>');
						if(newPhrase.search("_") == -1 && newPhrase.search("%(completedurl)s") == -1){
							appendText = ' <br><br> <a href="%(completedurl)s">%(completedtext)s</a>';
							newPhrase = newPhrase + appendText
						}
						return newPhrase;
					}
					
					function getQueryString() {
					  var result = {}, queryString = location.search.substring(1),
					      re = /([^&=]+)=([^&]*)/g, m;
					  while (m = re.exec(queryString)) {
					    result[decodeURIComponent(m[1])] = decodeURIComponent(m[2]);
					  }
					  return result;
					}
					function createCookie(name,value,days) {
						if (days) {
							var date = new Date();
							date.setTime(date.getTime()+(days*24*60*60*1000));
							var expires = "; expires="+date.toGMTString();
						}
						else var expires = "";
						document.cookie = name+"="+value+expires+"; path=/";
					}
					function readCookie(name) {
						var nameEQ = name + "=";
						var ca = document.cookie.split(';');
						for(var i=0;i < ca.length;i++) {
							var c = ca[i];
							while (c.charAt(0)==' ') c = c.substring(1,c.length);
							if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
						}
						return null;
					}
				</script>
		</body></html>
	""" % {
		"storage_key":form['storagekey'].value() if form['storagekey'].value() else "guide_%s_phrase" % form['guide_id'].value(),
		"spaces":spaces,
		"count":count,
		"message":form['message'].value(),
		"message_title":form['message_title'].value(),
		"completedurl":form['completedurl'].value(),
		"completedtext":form['completedtext'].value()
		}
	else:
		html = """	<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
				<meta name="viewport" content="width=device-width; initial-scale=1.0; maximum-scale=1.0; user-scalable=0;">
				<style>
					html, body{
						background-color:#f9f9f9;
					}
					*{
						font-family:"Helvetica Neue", "Helvetica", Arial, sans-serif;
					}
					.container{
						padding:10px;
						text-align:center;
					}
					.logo{
						background:transparent url(logo.png) left top no-repeat;
						width:153px;
						height:125px;
						background-size:153px 125px;
						-webkit-background-size:153px 125px;
						-moz-background-size:153px 125px;
						background-size:153px 125px;
						margin:20px auto 50px auto;
					}
					#phrase{
						font-size:20px;
						font-weight:bold;
						color:#aaa;
					}
					#phrase .letters{
						color:#444;
					}
					.instructions{
						font-size:12px;
						color:#666;
						background-color:#eee;
						display:inline-block;
						padding:20px;
						border-radius:5px;
						margin-top:50px;
						box-shadow:0 1px 1px rgba(0,0,0,.12);
					}
					.instructions strong{
						display:block;
						font-size:14px;
					}
				</style>
			</head>
			<body>
				<div class="container">
					<div class="logo"></div>
					<div id="phrase">%(spaces)s</div>
					<p class="instructions">
						<strong>%(message_title)s</strong>
						%(message)s
					</p>
				</div><!-- end container-->
				<script>
					var phrase = "%(spaces)s";
					var qs = getQueryString();
					var startIndex = parseInt(qs['s']);
					var letters = decodeURIComponent(qs['l']);
					var reset = qs['reset'];
					var storedPhrase = window.localStorage["%(storage_key)s"];
					var cookiePhrase = readCookie("%(storage_key)s");
					if(storedPhrase == undefined && cookiePhrase != null)
						storedPhrase = cookiePhrase;
					if(cookiePhrase == null && storedPhrase != undefined)
						cookiePhrase = storedPhrase;
					var phraseElement = document.getElementById('phrase');
					if(isNaN(startIndex) || !letters) {
						startIndex = 0;
						letters = '';
					}
					if(!storedPhrase || reset == 'true') {
						phrase = fillInLetters(phrase, startIndex, letters);
					}
					else {
						phrase = fillInLetters(storedPhrase, startIndex, letters);
					}
					window.localStorage["%(storage_key)s"] = phrase;
					createCookie("%(storage_key)s", phrase, 365);
					phraseElement.innerHTML = htmlFormat(phrase);
					function fillInLetters(phrase, startIndex, letters) {
						var newPhrase = phrase.slice(0, startIndex) + letters + phrase.slice(startIndex + letters.length)
						return newPhrase;
					}
					function htmlFormat(phrase) {
						return phrase.replace(/([^_ ]+)/g, '<span class="letters">$&</span>');
					}
					
					function getQueryString() {
					  var result = {}, queryString = location.search.substring(1),
					      re = /([^&=]+)=([^&]*)/g, m;
					  while (m = re.exec(queryString)) {
					    result[decodeURIComponent(m[1])] = decodeURIComponent(m[2]);
					  }
					  return result;
					}
					function createCookie(name,value,days) {
						if (days) {
							var date = new Date();
							date.setTime(date.getTime()+(days*24*60*60*1000));
							var expires = "; expires="+date.toGMTString();
						}
						else var expires = "";
						document.cookie = name+"="+value+expires+"; path=/";
					}
					function readCookie(name) {
						var nameEQ = name + "=";
						var ca = document.cookie.split(';');
						for(var i=0;i < ca.length;i++) {
							var c = ca[i];
							while (c.charAt(0)==' ') c = c.substring(1,c.length);
							if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
						}
						return null;
					}
				</script>
		</body></html>
	""" % {
		"storage_key":form['storagekey'].value() if form['storagekey'].value() else "guide_%s_phrase" % form['guide_id'].value(),
		"spaces":spaces,
		"count":count,
		"message":form['message'].value(),
		"message_title":form['message_title'].value(),
		}
	f = open(outfolder+"/"+form['html'].value(), "w")
	f.write(html)
	f.close()

