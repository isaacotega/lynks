from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from . import connection as mysql
import datetime
import json
import random
from django.views.decorators.csrf import ensure_csrf_cookie


date = str(datetime.datetime.now().year) + " " + str(datetime.datetime.now().month) + " " + str(datetime.datetime.now().day)

time = str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute)

def randomTwentyDigits() :

	i = 0

	randomTwentyDigits = ""

	while i < 20 :

		randomTwentyDigits += str(random.randrange(0, 10))

		i = i + 1

	return randomTwentyDigits
	
class styles :
	
	context = {}
	
	def posts(self, request) :
		
		stylesheet = loader.get_template("web/styles/posts.css")
		
		return HttpResponse(stylesheet.render(self.context))
		
styles = styles()
	
	
class scripts :
	
	context = {}
	
	def posts(self, request) :
		
		script = loader.get_template("web/scripts/posts.js")
		
		return HttpResponse(script)
		
scripts = scripts()

	
class ajaxHandlers :
	
	context = {}
	
	def posts(self, request) :
		
		data = {
			"usercode": request.POST["usercode"]
		}
		
		sql = "SELECT * FROM posts ORDER BY RAND() LIMIT 10 "
	
		mysql.cursor.execute(sql)
	
		result = mysql.cursor.fetchall()
		
		postsData = []
		
		for eachResult in result :
			
			eachResultObj = {}

			eachResultObj["posterUsercode"] = eachResult["poster_usercode"]
			eachResultObj["postId"] = eachResult["post_id"]
			eachResultObj["title"] = eachResult["title"]
			eachResultObj["body"] = eachResult["body"]
			eachResultObj["category"] = eachResult["category"]
			eachResultObj["subcategory"] = eachResult["subcategory"]
			eachResultObj["views"] = eachResult["views"]
			eachResultObj["link"] = eachResult["link"]
			eachResultObj["datePosted"] = eachResult["date_posted"]
			eachResultObj["timePosted"] = eachResult["time_posted"]
			eachResultObj["lastUpdateDate"] = eachResult["last_update_date"]
			eachResultObj["lastUpdateTime"] = eachResult["last_update_time"]
			eachResultObj["user"] = {
				"liked": False,
				"disliked": False,
				"reported": False
			}
			eachResultObj["statistics"] = {
				"likes": 0,
				"dislikes": 0,
				"views": 0,
				"reports": 0
			}
			
			sql = "INSERT INTO views (post_id, viewer_usercode, date_viewed, time_viewed)  VALUES ('" + eachResultObj["postId"] + "', '" + data["usercode"] + "', '" + date + "', '" + time + "') "
	
			mysql.cursor.execute(sql)
	
			
			sql = "SELECT * FROM views WHERE post_id = '" + eachResultObj["postId"] + "' "
	
			mysql.cursor.execute(sql)
	
			viewsResult = mysql.cursor.fetchall()
			
			eachResultObj["statistics"]["views"] = len(viewsResult)
						
			
			sql = "SELECT * FROM reports WHERE post_id = '" + eachResultObj["postId"] + "' "
	
			mysql.cursor.execute(sql)
	
			reportsResult = mysql.cursor.fetchall()
			
			eachResultObj["statistics"]["reports"] = len(reportsResult)
						
			for eachReportResult in reportsResult :
				
				if eachReportResult["reporter_usercode"] == data["usercode"] :
					
					eachResultObj["user"]["reported"] = True
				
            			
			sql = "SELECT * FROM reactions WHERE post_id = '" + eachResultObj["postId"] + "' "
	
			mysql.cursor.execute(sql)
	
			reactionsResult = mysql.cursor.fetchall()
			
			for eachReactionResult in reactionsResult :
				
				if eachReactionResult["reaction_type"] == "like" :
						
					eachResultObj["statistics"]["likes"] += 1
				
				if eachReactionResult["reaction_type"] == "dislike" :
						
					eachResultObj["statistics"]["dislikes"] += 1
				 
				if eachReactionResult["reactor_usercode"] == data["usercode"] :
					
					if eachReactionResult["reaction_type"] == "like" :
						
						eachResultObj["user"]["liked"] = True
						
					if eachReactionResult["reaction_type"] == "dislike" :
						
						eachResultObj["user"]["disliked"] = True
						
			
			
			postsData.append(eachResultObj)
			
		return HttpResponse(json.dumps(postsData))
		
		
		
	def postActions(self, request) :
		
		data = {
		}
		xx = ""
		
		usercode = request.POST["usercode"]
		
		postId = request.POST["postId"]
		
		action = request.POST["action"]
		
		
		if action == "like" or action == "dislike" :
		
			reactionType = action
		
			sql = "SELECT * FROM reactions WHERE post_id = '" + postId + "' AND reactor_usercode = '" + usercode + "' AND reaction_type = '" + reactionType + "' "
	
			mysql.cursor.execute(sql)
	
			result = mysql.cursor.fetchall()
			
			if len(result) == 0 :
				
				sql = "INSERT INTO reactions (reactor_usercode, post_id, reaction_type, date_reacted, time_reacted) VALUES ('" + usercode + "', '" + postId + "', '" + reactionType + "', '" + date + "', '" + time + "') "
				
			else :
		
				sql = "DELETE FROM reactions WHERE post_id = '" + postId + "' AND reactor_usercode = '" + usercode + "' AND reaction_type = '" + reactionType + "' "
	
			mysql.cursor.execute(sql)
	
			
		return HttpResponse(json.dumps(sql))
		
		
ajaxHandlers = ajaxHandlers()






def index(request) :
	
	template = loader.get_template("web/index.html")
	
	return HttpResponse(template.render())
	
	
def redirector(request) :
	
	template = loader.get_template("web/redirector/index.html")
	
	context = {
		"url": request.GET["url"]
	}
	
	return HttpResponse(template.render(context))
	
	
	
def signup(request) :
	
	template = loader.get_template("web/signup/index.html")
		
	data = {
		"firstName": request.GET["first-name"],
		"lastName": request.GET["last-name"],
		"username": request.GET["username"],
		"email": request.GET["email"],
		"gender": request.GET["gender"],
		"password": request.GET["password"],
		"usercode": randomTwentyDigits(),
		"cookieCode": randomTwentyDigits(),
		"dateJoined": date,
		"timeJoined": time
	}
	
	sql = "SELECT * FROM accounts WHERE username = '" + data["username"] + "'"
	
	mysql.cursor.execute(sql)
	
	result = mysql.cursor.fetchall()
	
	if len(result) == 0 :
	
		sql = "INSERT INTO accounts (usercode, first_name, last_name, email, password, gender, username, date_registered, time_registered) VALUES ('" + data["usercode"] + "', '" + data["firstName"] + "', '" + data["lastName"] + "', '" + data["email"] + "', '" + data["password"] + "', '" + data["gender"] + "', '" + data["username"] + "', '" + data["dateJoined"] + "', '" + data["timeJoined"] + "')"
	
		mysql.cursor.execute(sql)
	
		context = {
			"alert": "Android.SignUpSuccessfull(" + data["usercode"] + ")"
		}
	
		return HttpResponse(template.render(context))
		
	else :
		
		context = {
			"alert": "Android.SignUpFailed()"
		}
	
		return HttpResponse(template.render(context))

	

	
def login(request) :
	
	template = loader.get_template("web/login/index.html")
		
	data = {
		"username": request.GET["username"],
		"password": request.GET["password"]
	}
	
	sql = "SELECT usercode FROM accounts WHERE username = '" + data["username"] + "' AND password = '" + data["password"] + "'"
	
	mysql.cursor.execute(sql)
	
	result = mysql.cursor.fetchone()
	
	if result == None :
	
		context = {
			"alert": "Android.LogInFailed()"
		}
	
		return HttpResponse(template.render(context))
		
	else :
			
		userInfo = {
			"usercode": result[0]
		}
		
		context = {
			"alert": "Android.LogInSuccessfull(" + userInfo["usercode"] + ");"
		}
	
		return HttpResponse(template.render(context))



def post(request) :
	
	template = loader.get_template("web/post/index.html")
		
	data = {
		"postId": randomTwentyDigits(),
		"posterUsercode": request.GET["poster-usercode"],
		"title": request.GET["title"],
		"body": request.GET["body"],
		"category": request.GET["category"],
		"subcategory": request.GET["subcategory"],
		"tags": request.GET["tags"],
		"link": request.GET["link"],
		"datePosted": date,
		"timePosted": time,
		"lastUpdateDate": date,
		"lastUpdateTime": time
	}
	
	sql = "INSERT INTO posts (poster_usercode, post_id, title, body, category, subcategory, tags, link, date_posted, time_posted, last_update_date, last_update_time) VALUES ('" + data["posterUsercode"] + "', '" + data["postId"] + "', '" + data["title"] + "', '" + data["body"] + "', '" + data["category"] + "', '" + data["subcategory"] + "', '" + data["tags"] + "', '" + data["link"] + "', '" + data["datePosted"] + "', '" + data["timePosted"] + "', '" + data["lastUpdateDate"] + "', '" + data["lastUpdateTime"] + "') "
	
	mysql.cursor.execute(sql)
	
	context = {
		"alert": "Android.PostSuccessfull();"
	}
	
	return HttpResponse(template.render(context))
	


def posts(request) :
	
	header = loader.get_template("web/templates/header.html")
	
	body = loader.get_template("web/posts/index.html")
	
	footer = loader.get_template("web/templates/footer.html")
	
	context = {
		"stylesheet": loader.get_template("web/styles/posts.css").render(),
		"JQuery": loader.get_template("web/scripts/JQuery.js").render(),
		"javascript": loader.get_template("web/scripts/posts.js").render(),
		"postBox": loader.get_template("web/templates/post-box.html").render().replace("\n", ""),
		"dotsLoader": loader.get_template("web/templates/dots-loader.html").render({"JQuery": loader.get_template("web/scripts/JQuery.js").render()}),
		"lynksSplash": loader.get_template("web/templates/lynks-splash.html").render(),
		"usercode": request.GET["usercode"]
	}
	
	return HttpResponse(header.render(context) + body.render(context) + footer.render(context))
	
	
def report(request) :
	
	template = loader.get_template("web/report/index.html")
		
	data = {
		"postId": request.GET["post-id"],
		"reportId": randomTwentyDigits(),
		"reporterUsercode": request.GET["reporter-usercode"],
		"body": request.GET["body"],
		"dateReported": date,
		"timeReported": time
	}
	
	sql = "INSERT INTO reports (report_id, post_id, reporter_usercode, body, date_reported, time_reported) VALUES ('" + data["reportId"] + "', '" + data["postId"] + "', '" + data["reporterUsercode"] + "', '" + data["body"] + "', '" + data["dateReported"] + "', '" + data["timeReported"] + "') "
	
	mysql.cursor.execute(sql)
	
	context = {
		"alert": "Android.reportSuccessfull();"
	}
	
	return HttpResponse(template.render(context))
	
