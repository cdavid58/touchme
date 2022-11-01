from django.shortcuts import render,redirect
from youtubesearchpython import VideosSearch    
import webbrowser, pafy, os, json, requests,threading,queue
from django.http import HttpResponse
from moviepy.editor import *

my_queue = queue.Queue()

def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

def Restaurar(request):
	return HttpResponse('')

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
		request.session['code'] = request.POST['code']

		if json.loads(response.text)['Message']:
			return redirect('Client')
	return render(request,'login.html')

gender = {}
list_music = []

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


# --------------------------------------------------------------------------------

def Index(request):
	global gender
	list_gender = []
	for key, value in gender.items():
		if value is not None:
			list_gender.append({'gender':value})
	url = "http://localhost:9090/bar/Get_List_Song/"
	payload = json.dumps({
	  "code": request.session['code']
	})
	headers = {
	  'Content-Type': 'application/json'
	}
	response = requests.request("POST", url, headers=headers, data=payload)
	music = json.loads(response.text)
	return render(request,'index.html',{'gender':list_gender[1:],'list_canciones':music,
																				'list_music':json.dumps(music)
																			})


def Client(request):
	global gender
	list_gender = []
	for key, value in gender.items():
		if value is not None:
			list_gender.append({'gender':value})

	url = "http://localhost:9090/bar/Get_List_Song/"

	payload = json.dumps({
	  "code": request.session['code']
	})
	headers = {
	  'Content-Type': 'application/json'
	}
	response = requests.request("POST", url, headers=headers, data=payload)
	return render(request,'client.html',{'gender':list_gender[1:],'list_canciones':json.loads(response.text)})

def Save_Music_Client(request):
	if request.is_ajax():
		title = Download_Music(request)
		url = "http://localhost:9090/bar/Save_Song/"
		payload = json.dumps({
		  "code": request.session['code'],
		  "music": title,
		  "artist": request.GET.get('artist')
		})
		headers = {
		  'Content-Type': 'application/json'
		}
		response = requests.request("POST", url, headers=headers, data=payload)
		return HttpResponse('')
		


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
	audio.write_audiofile('./static/'+normalize(title)+'.mp3')
	audio.close()
	os.remove(title+'.webm')
	return normalize(title)

def Download_Music(request):
	u = threading.Thread(target=Download_Musics,args=(request,), name='Invoice')
	u.start()
	data = my_queue.get()
	return data	


def Delete_Song(request):
	if request.is_ajax():
		name_music = request.GET.get('name_music')
		print(name_music)
		url = "http://localhost:9090/bar/Delete_Music/"
		payload = json.dumps({
		  "music": name_music
		})
		headers = {
		  'Content-Type': 'application/json'
		}
		response = requests.request("POST", url, headers=headers, data=payload)
		url = "http://localhost:9090/bar/Get_List_Song/"
		payload = json.dumps({
		  "code": request.session['code']
		})
		headers = {
		  'Content-Type': 'application/json'
		}
		response = requests.request("POST", url, headers=headers, data=payload)
		music = json.loads(response.text)
		return HttpResponse(json.dumps(music))


def Request_List_Song(request):
	url = "http://localhost:9090/bar/Get_List_Song/"

	payload = json.dumps({
	  "code": request.session['code']
	})
	headers = {
	  'Content-Type': 'application/json'
	}
	response = requests.request("POST", url, headers=headers, data=payload)
	music = json.loads(response.text)
	return HttpResponse(json.dumps(music))