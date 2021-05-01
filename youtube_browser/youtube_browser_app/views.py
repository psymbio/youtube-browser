import requests

from isodate import parse_duration

from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def index(request):
    videos = []
    if request.method == 'POST':
        number = request.POST.get('notosearch', False)
        searchquery = request.POST.get('searchquery', False)
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'
        search_params = {'part': 'snippet',
            'q': searchquery,
            'key': settings.YT_KEY,
            'maxResults': number,
            'type': 'video'}
        r = requests.get(search_url, params=search_params)
        print(r)
        results = r.json()['items']
        print(r)
        video_ids = []
        for result in results:
            # print(result['id']['videoId'])
            video_ids.append(result['id']['videoId'])
        lucky =  request.POST.get('searchlucky', False)
        if lucky == True:
            return redirect("https://www.youtube.com/watch?v="+video_ids[0])
        video_params = {
            'part': 'snippet, contentDetails',
            'key': settings.YT_KEY,
            'id': ','.join(video_ids),
            'maxResults': number,
        }
        r2 = requests.get(video_url, params=video_params)
        results2 = r2.json()['items']
        for result in results2:
            # print(result['snippet']['title'])
            # print(result['id'])
            # print(parse_duration(result['contentDetails']['duration']))
            # print(parse_duration(result['contentDetails']['duration']).total_seconds // 60)
            # print(result['snippet']['thumbnails']['high']['url'])
            video_data = {
                'title': result['snippet']['title'],
                'id': result['id'],
                'url': "https://www.youtube.com/watch?v="+result['id'],
                'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail': result['snippet']['thumbnails']['high']['url']
            }

            videos.append(video_data)
    # print(videos)
    context = {'videos': videos}
    
    return render(request, 'search2.html', context)