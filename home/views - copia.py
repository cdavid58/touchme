from django.shortcuts import render,redirect
from youtubesearchpython import VideosSearch    
import webbrowser, pafy, os, json, requests,threading,queue
from django.http import HttpResponse
from moviepy.editor import *

my_queue = queue.Queue()

def storeInQueue(f):
  def wrapper(*args):
  	global my_queue
  	my_queue.put(f(*args))
  return wrapper

def Login(request):
	if request.method == 'POST':
		url = "http://localhost:9090/bar/Verified_Login/"
		payload = json.dumps({
		  "lat": request.POST['lat'],
		  "lon": request.POST['lon'],
		  "number_phone": request.POST['number_phone'],
		  "code":request.POST['code']
		})
		headers = {
		  'Content-Type': 'application/json'
		}
		response = requests.request("POST", url, headers=headers, data=payload)
		Get_Gender_Bar(request.POST['code'])

		if json.loads(response.text)['Message']:
			return redirect('Client')
	return render(request,'login.html')

gender = {}
list_music = []

def Index(request):
	global gender
	list_gender = []
	for key, value in gender.items():
		if value is not None:
			list_gender.append({'gender':value})
	return render(request,'index.html',{'gender':list_gender[1:]})

def Get_Gender_Bar(code):
	global gender
	url = "http://localhost:9090/bar/Get_Gender_Bar/"
	payload = json.dumps({
	  "code": code
	})
	headers = {
	  'Content-Type': 'application/json'
	}
	response = requests.request("POST", url, headers=headers, data=payload)
	gender = json.loads(response.text)

def Restaurar(request):
	global list_music
	return HttpResponse(list_music)


# --------------------------------------------------------------------------------


def Client(request):
	global gender
	list_gender = []
	for key, value in gender.items():
		if value is not None:
			list_gender.append({'gender':value})
	return render(request,'client.html',{'gender':list_gender[1:]})

def Save_Music_Client(request):
	if 

@storeInQueue
def Download_Musics(request):
	global list_music
	music = request.GET.get('music')
	artist = request.GET.get('artist')
	list_music.append(music)
	videosSearch = VideosSearch(music+' '+artist, limit = 1)
	video = ""
	title = ""
	for i in range(1):
	    video = (videosSearch.result()['result'][i]['link'])
	    title = str(videosSearch.result()['result'][i]['title']).replace('"','_')
	video = pafy.new(video)
	bestaudio = video.getbestaudio()
	bestaudio.download()
	audio = AudioFileClip(title+'.webm')
	audio.write_audiofile('./static/'+title+'.mp3')
	audio.close()
	os.remove(title+'.webm')
	return title

def Download_Music(request):
	u = threading.Thread(target=Download_Musics,args=(request,), name='Invoice')
	u.start()
	data = my_queue.get()
	return HttpResponse(data)