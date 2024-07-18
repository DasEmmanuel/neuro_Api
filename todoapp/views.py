from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
import mysql.connector as mysql
import os
import sys

dbHost = "216.48.185.115"
dbDatabase = "sravaDB"
dbUser = "abhinesh"
dbPassword = "information"

# db_connect = mysql.connect(
#                     host=dbHost, database=dbDatabase, user=dbUser, password=dbPassword)
# mycursor = db_connect.cursor()
# #mycursor.execute("SELECT * FROM sravaDB.asrTestingFIles WHERE userId = 19")
# mycursor.execute("SELECT * FROM sravaDB.asrTestingFIles WHERE userId = 36 AND file_Name LIKE 'N%';")
# myVideos = mycursor.fetchall()
# print(myVideos,"line------------20")

# userID = "19"
# SearchText="कांग्रेस"
# db_connect = mysql.connect(
#         host=dbHost, database=dbDatabase, user=dbUser, password=dbPassword)
# mycursor = db_connect.cursor()
# mycursor.execute("SELECT * FROM sravaDB.asrTestingFIles WHERE userId = 19 AND video_json LIKE '%"+SearchText+"%';")
    
# mykeywordsResults = mycursor.fetchall()
# print(mykeywordsResults,"line-------30")

def index(request):
    return render(request, 'partials/index.html')

def about(request):
    return render(request, 'partials/about.html')

def register(request):

    return render(request, 'partials/register.html')

def contacts(request):

    return render(request, 'partials/contacts.html')

def help(request):

    return render(request, 'partials/help.html')

@csrf_exempt
def fileUploads(request):
    if request.method == "POST":
        data = request.POST

        userID = data["userId"]
        languages = data["languages"]
        fileName = data["fileName"]
        video_text = data["video_text"]
        video_json = data["video_json"]
        save_file_names = request.FILES['video_paths']

        print(data,"----------line 39")
        print(request.FILES['video_paths'],"----------line 40")

        file_path_manual = os.path.dirname( os.path.realpath(sys.argv[0])) + "/static/video/"
        print(file_path_manual,"line--------45")
        save_file_names = request.FILES['video_paths']
        file = save_file_names
        imageName1 = file.name
        tothefile = file_path_manual + imageName1
        tothefile.replace("C:/Users/pc/Desktop/MajorProject/Todoproject/static/video","http://127.0.0.1:8000")
        imageName2 = os.path.splitext(tothefile)[0]
        filepathfinal = "http://127.0.0.1:8000/static/video/"+imageName1
        print(imageName2,"line---------62")
        print(filepathfinal,"line------------63")
        with open(tothefile,'wb') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        print(fileName,"line--------53")
        db_connect = mysql.connect(host=dbHost, database=dbDatabase, user=dbUser, password=dbPassword)
        mycursor = db_connect.cursor()
        newRecords = 'insert into asrTestingFIles (userId,languages,file_Name,video_text,video_json,video_path) values(%s,%s,%s,%s,%s,%s)'
        mycursor.execute(newRecords, (userID,languages,fileName,video_text,video_json,filepathfinal))
        db_connect.commit()
    return JsonResponse({"status": "200", "message": "Success"}, safe=False)

@csrf_exempt
def Default_keywords(request):
    myTablesData = [] ; tablesArray =[]
    if request.method == "POST":
        data = request.POST
        userID = data["userId"]
        fileId = data["fileId"]
        

        db_connect = mysql.connect(
        host=dbHost, database=dbDatabase, user=dbUser, password=dbPassword)
    mycursor = db_connect.cursor()
    mycursor.execute(
        "SELECT * FROM sravaDB.asrKeywords WHERE userId='"+userID+"' AND videoId='"+fileId+"';")
    
    mykeywordsResults = mycursor.fetchall()
    
    for items in mykeywordsResults:
        myTablesData.append({"asrKeywordsId":items[0],"keywords":items[1]})
        tablesArray.append(items[1])

    #myvideosData.append({"fileId":items[0],"userId":items[1],"languages":items[2],"file_Name":items[3],"video_text":items[4],"video_json": str(items[5]),"video_player":items[6]})
    return JsonResponse({"status": "200", "message": "Success", "myTablesData": myTablesData, "tablesArray":tablesArray}, safe=False)

@csrf_exempt
def add_keywords(request):
    myTablesData = []
    myvideosData = []
    if request.method == "POST":
        data = request.POST
        userID = data["userId"]
        fileId = data["fileId"]
        textEnters = data["textEnters"]
        graphColours = data["graphColours"]
        

        db_connect = mysql.connect(
        host=dbHost, database=dbDatabase, user=dbUser, password=dbPassword)
        mycursor = db_connect.cursor()
        mycursor.execute(
        "SELECT * FROM sravaDB.asrKeywords WHERE userId='"+userID+"' AND videoId='"+fileId+"' AND keywords='"+textEnters+"';")
    
        mykeywordsResults = mycursor.fetchall()
    

    if mykeywordsResults == []:
        db_connect = mysql.connect(
            host=dbHost, database=dbDatabase, user=dbUser, password=dbPassword)
        mycursor = db_connect.cursor()
        newRecords = 'insert into asrKeywords (userID,videoId,keywords) values(%s,%s,%s)'
        mycursor.execute(newRecords, (userID, fileId, textEnters))
        db_connect.commit()

        mycursor = db_connect.cursor()
        newRecordsGraphs = 'insert into asrGraphs (keywords,colours,userId,fileId) values(%s,%s,%s,%s)'
        mycursor.execute(newRecordsGraphs, (textEnters,graphColours,userID,fileId))
        db_connect.commit()

        mycursor.execute("SELECT * FROM asrTestingFIles WHERE fileId='"+fileId+"'")
        myVideos = mycursor.fetchall()

        for items in myVideos:
            myvideosData.append({"fileId":items[0],"userId":items[1],"languages":items[2],"file_Name":items[3],"video_text":items[4],"video_json": str(items[5]),"video_player":items[6]})

        db_connect.commit()
        db_connect.close()
        return JsonResponse({"status": "200", "message": "Success","myvideosData": myvideosData}, safe=False)
    else:
        if textEnters == mykeywordsResults[0][1]:
            return JsonResponse({"status": 400, "message": "Keyword already Exists"}, safe=False)
        else:
            db_connect = mysql.connect(
                    host=dbHost, database=dbDatabase, user=dbUser, password=dbPassword)
            mycursor = db_connect.cursor()
            newRecords = 'insert into asrKeywords (userID,videoId,keywords) values(%s,%s,%s)'
            mycursor.execute(newRecords, (userID, fileId, textEnters))
            db_connect.commit()

            newRecordsGraphs = 'insert into asrGraphs (keywords,colours,userId,fileId) values(%s,%s,%s,%s)'
            mycursor.execute(newRecordsGraphs, (textEnters,graphColours,userID,fileId))
            db_connect.commit()

            mycursor.execute("SELECT * FROM asrTestingFIles WHERE fileId='"+fileId+"'")
            myVideos = mycursor.fetchall()

            for items in myVideos:
                myvideosData.append({"fileId":items[0],"userId":items[1],"languages":items[2],"file_Name":items[3],"video_text":items[4],"video_json": str(items[5]),"video_player":items[6]})
            
            db_connect.commit()
            return JsonResponse({"status": "200", "message": "Success","myvideosData": myvideosData}, safe=False)


@csrf_exempt
def search_keywords(request):
    myvideosData = []
    if request.method == "POST":
        data = request.POST
        userID = data["userId"]
        SearchText = data["findKeywords"]
        

        db_connect = mysql.connect(
         host=dbHost, database=dbDatabase, user=dbUser, password=dbPassword)
        mycursor = db_connect.cursor()
        mycursor.execute("SELECT * FROM sravaDB.asrTestingFIles WHERE userId='"+userID+"' AND video_json LIKE '%"+SearchText+"%';")
        mykeywordsResults = mycursor.fetchall()
        # print(mykeywordsResults,"line-------189")

        if mykeywordsResults == []:
            return JsonResponse({"status": "400" , "message": "Undefined Keyword"}, safe=False)
        
        else:
            for items in mykeywordsResults:
                myvideosData.append({"fileId":items[0],"userId":items[1],"languages":items[2],"file_Name":items[3],"video_text":items[4],"video_json": str(items[5]),"video_player":items[6]})
                
                return JsonResponse({"status": "200", "message": "Success","myvideosData": myvideosData,"keywords":SearchText}, safe=False)


@csrf_exempt
def UpdategraphKeywords(request):
    if request.method == "POST":
        data = request.POST

        fileId = data["fileId"]
        textEnters = data["textEnters"]
        keywordscount = data["keywordscount"]

        db_connect = mysql.connect(host=dbHost, database=dbDatabase, user=dbUser, password=dbPassword)
        mycursor = db_connect.cursor()
        mycursor.execute("SELECT * FROM sravaDB.asrKeywords WHERE asrKeywordsId='"+fileId+"' AND keywords='"+textEnters+"';")
        mykeywordsResults = mycursor.fetchall()
    
        if textEnters == mykeywordsResults[0][1]:
            db_connect = mysql.connect(
                        host=dbHost, database=dbDatabase, user=dbUser, password=dbPassword)
            mycursor = db_connect.cursor()
            mycursor.execute(" UPDATE asrGraphs SET counts=%s,tableId=%s WHERE keywords=%s ", (keywordscount,fileId,textEnters))
            db_connect.commit()

            return JsonResponse({"status": "200"}, safe=False)

@csrf_exempt
def delete_keywords(request):
    myvideosData = []
    if request.method == "POST":
        data = request.POST

        fileId = data["fileId"]
        globalVideoId = data["globalVideoId"]
        print(fileId,"line-------162")
        print(globalVideoId,"line-------163")
        

        db_connect = mysql.connect(
        host=dbHost, database=dbDatabase, user=dbUser, password=dbPassword)
        mycursor = db_connect.cursor()
        mycursor.execute("DELETE FROM asrKeywords WHERE asrKeywordsId='"+fileId+"'")
        db_connect.commit()

        mycursor.execute("DELETE FROM asrGraphs WHERE tableId='"+fileId+"'")
        db_connect.commit()

        mycursor.execute("SELECT * FROM asrTestingFIles WHERE fileId='"+globalVideoId+"'")
        myVideos = mycursor.fetchall()
        print(myVideos,"line------173")
        for items in myVideos:
            myvideosData.append({"fileId":items[0],"userId":items[1],"languages":items[2],"file_Name":items[3],"video_text":items[4],"video_json": str(items[5]),"video_player":items[6]})

        db_connect.commit()
        return JsonResponse({"status": "200", "message": "Deleted keyword Successfully","myvideosData":myvideosData}, safe=False)

@csrf_exempt
def file_keywords_update(request):
    myvideosData = []
    if request.method == "POST":
        data = request.POST

        globalVideoId = data["globalVideoId"]
        finalEditedText = data["finalEditedText"]
        convertingTextObjects = data["convertingTextObjects"]

        db_connect = mysql.connect(
                    host=dbHost, database=dbDatabase, user=dbUser, password=dbPassword)
        mycursor = db_connect.cursor()
        mycursor.execute("SELECT * FROM asrTestingFIles WHERE fileId='"+globalVideoId+"'")
        myVideos = mycursor.fetchall()

        
        if(myVideos)==[]:
            return JsonResponse({"status": "400", "message": "keyword not found"}, safe=False)
        else:
            mycursor.execute(" UPDATE asrTestingFIles SET video_text=%s,video_json=%s WHERE fileId=%s ", (finalEditedText,convertingTextObjects,globalVideoId))
            db_connect.commit()

            mycursor.execute("SELECT * FROM asrTestingFIles WHERE fileId='"+globalVideoId+"'")
            myVideos = mycursor.fetchall()
            for items in myVideos:
                myvideosData.append({"fileId":items[0],"userId":items[1],"languages":items[2],"file_Name":items[3],"video_text":items[4],"video_json": str(items[5]),"video_player":items[6]})
            db_connect.commit()

            return JsonResponse({"status": "200", "message": "Updated keyword Successfully","myvideosData":myvideosData}, safe=False)


def service(request):
    return render(request, 'partials/service.html')

def displayGraph(request):
    return render(request, 'partials/graphs.html')

@csrf_exempt
def searchVideos(request):
    myvideosData = []
    if request.method == "POST":
        data = request.POST
        userId = data['userId']
        videoSearch = data['videoSearch']
        # print(userId,"line----------247")
        # print(videoSearch,"line----------248")

        if videoSearch == "":
            db_connect = mysql.connect(
                        host=dbHost, database=dbDatabase, user=dbUser, password=dbPassword)
            mycursor = db_connect.cursor()
            #mycursor.execute("SELECT * FROM sravaDB.asrTestingFIles WHERE userId = 19")
            mycursor.execute("SELECT * FROM sravaDB.asrTestingFIles WHERE userId ='"+userId+"';")
            
            myVideos = mycursor.fetchall()
            # print(myVideos,"line------------223")
            
            if myVideos == []:
                # context = {
                #     "status": "400", "message": "Video not found"
                # }
                return JsonResponse({"status": "400", "message": "Please upload videos"}, safe=False)
            else:
                for items in myVideos:
                
                    myvideosData.append({"fileId":items[0],"userId":items[1],"languages":items[2],"file_Name":items[3],"video_text":items[4],"video_json": str(items[5]),"video_player":items[6]})
            
                db_connect.close()
                return JsonResponse({"status": "200", 'message': "video found","context": myvideosData}, safe=False)
        else:
            db_connect = mysql.connect(
                        host=dbHost, database=dbDatabase, user=dbUser, password=dbPassword)
            mycursor = db_connect.cursor()
            #mycursor.execute("SELECT * FROM sravaDB.asrTestingFIles WHERE userId = 19")
            mycursor.execute("SELECT * FROM sravaDB.asrTestingFIles WHERE userId =19 AND file_Name LIKE '"+videoSearch+"%';")
            
            myVideos = mycursor.fetchall()
            # print(myVideos,"line------------223")
            
            if myVideos == []:
                # context = {
                #     "status": "400", "message": "Video not found"
                # }
                return JsonResponse({"status": "400", "message": "video not found"}, safe=False)
            else:
                for items in myVideos:
                
                    myvideosData.append({"fileId":items[0],"userId":items[1],"languages":items[2],"file_Name":items[3],"video_text":items[4],"video_json": str(items[5]),"video_player":items[6]})
            
                db_connect.close()
                return JsonResponse({"status": "200", 'message': "video found","context": myvideosData}, safe=False)


@csrf_exempt
def individualVideos(request):
    myvideosData = []
    if request.method == "POST":
        data = request.POST
        fileId = data['fileId']
    
        db_connect = mysql.connect(
                    host=dbHost, database=dbDatabase, user=dbUser, password=dbPassword)
        mycursor = db_connect.cursor()
        #mycursor.execute("SELECT * FROM sravaDB.asrTestingFIles WHERE userId = 19")
        mycursor.execute("SELECT * FROM sravaDB.asrTestingFIles WHERE fileId = '"+fileId+"%';")
        
        myVideos = mycursor.fetchall()
        # print(myVideos,"line------------261")
        
        if myVideos == []:
            
            return JsonResponse({"status": "400", "message": "video not found"}, safe=False)
        else:
            for items in myVideos:
            
                myvideosData = {"video_json": str(items[5])}
        
        db_connect.close()
        return JsonResponse({"context": myvideosData}, safe=False)
        
@csrf_exempt
def displayGraphPoints(request):
    myvideosData = [["Element", "Counts", { "role": "style" } ]]
    if request.method == "POST":
        data = request.POST

        fileId = data['fileId']
        userId = data['userId']

        print(fileId,"line------347")
        print(userId,"line------348")
    
        db_connect = mysql.connect(
                    host=dbHost, database=dbDatabase, user=dbUser, password=dbPassword)
        mycursor = db_connect.cursor()
        #mycursor.execute("SELECT * FROM sravaDB.asrTestingFIles WHERE userId = 19")
        mycursor.execute("SELECT * FROM sravaDB.asrGraphs WHERE userId='"+userId+"' AND fileId = '"+fileId+"';")
        myKeywordsResults = mycursor.fetchall()
        print(myKeywordsResults,"line------------354")
        
        if myKeywordsResults == []:
            
            return JsonResponse({"status": "400", "message": "Keywords not found"}, safe=False)
        else:
            db_connect = mysql.connect(host=dbHost, database=dbDatabase, user=dbUser, password=dbPassword)
            mycursor = db_connect.cursor()
        #mycursor.execute("SELECT * FROM sravaDB.asrGraphs WHERE userId='"+userId+"' AND fileId = '"+fileId+"';")
        #myKeywordsResults = mycursor.fetchall()
            print(myKeywordsResults,"line------------364")

            # [["Element", "Density", { role: "style" } ],
            # [file_Name, 8.94, "#b87333"],
            # ["Silver", 10.49, "silver"],
            # ["Gold", 19.30, "gold"],
            # ["Platinum", 21.45, "color: #e5e4e2"]]

            for items in myKeywordsResults:
                myvideosData.append([items[1],int(items[2]),items[3]])
            db_connect.commit()
            print(myvideosData,"line--------374")
            return JsonResponse({"status": "200", 'message': "success","myvideosData": myvideosData}, safe=False)



@csrf_exempt
def registerUrl(request):
    if request.method == "POST":
        data = request.POST
        userName = data["username"]
        passwordUser = data["passwordUser"]
        Fname = data["Fname"]
        Mname = data["Mname"]
        Lname = data["Lname"]
        PHno = data["PHno"]
        mail = data["mail"]

        db_connect = mysql.connect(
            host=dbHost, database=dbDatabase, user=dbUser, password=dbPassword)
        mycursor = db_connect.cursor()
           
        mycursor.execute(
            "SELECT * FROM sravaDB.asrTestings WHERE userName='"+userName+"';")
        myresults = mycursor.fetchall()
        
        
        if myresults == []:
            db_connect = mysql.connect(
                host=dbHost, database=dbDatabase, user=dbUser, password=dbPassword)
            mycursor = db_connect.cursor()
            newRecords = 'insert into asrTestings (userName,password,Fname,Mname,Lname,PHno,mail) values(%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(newRecords, (userName, passwordUser,Fname,Mname,Lname,PHno,mail))
            db_connect.commit()
            db_connect.close()
            return JsonResponse({"status": "200", 'message': "your data is registered successfully"}, safe=False)
        else:
            print("UserName is already existing")
            return JsonResponse({"status": "400", 'message': "UserName is already existing, Try another!"}, safe=False)

def login(request):
    return render(request, 'partials/login.html')

def menu(request):
    return render(request, 'partials/menu.html')

@csrf_exempt
def loginUrl(request):
    userDetails = []
    if request.method == "POST":
        data = request.POST

        userName = data["username"]
        passwordUser = data["passwordUser"]
        
        db_connect = mysql.connect(
            host=dbHost, database=dbDatabase, user=dbUser, password=dbPassword)
        mycursor = db_connect.cursor()
        mycursor.execute(
            "SELECT * FROM asrTestings WHERE userName='"+userName+"' AND password='"+passwordUser+"';")
        myloginUsers = mycursor.fetchall()
        

        if myloginUsers == []:
            message = "user not found ! Redirecting to Registration"
            return JsonResponse({"status": "400", 'message': message}, safe=False)
        
        else:

            for items in myloginUsers:
                userDetails.append({"id":items[0],"userName":items[1]})

            if myloginUsers[0][1] == userName:

                message = "Login Successfull! Redirecting to Our Service"
                return JsonResponse({"status": "200", 'message': message,"userDetails":userDetails}, safe=False)
        


