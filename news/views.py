import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from hypernews.settings import NEWS_JSON_PATH
import os


# Create your views here.

class MainPageView(View):
    def get(self, request, *args, **kwargs):
        text = '<h1>Coming soon</h1>'
        return HttpResponse(text)

class NewsView(View):
    POSTS_PATH  = NEWS_JSON_PATH

    def get(self, request, *args, **kwargs):
        post_array = [
        {
        "created": "2020-02-22 16:40:00",
        "text": "A new star appeared in the sky.",
        "title": "The birth of the star",
        "link": 9234732 }]

        post_id = 9234732

        with open(NEWS_JSON_PATH, 'w') as posts:
            json.dump(post_array, posts)

        with open(NEWS_JSON_PATH) as posts:
            array_of_posts = json.load(posts)

        for post in array_of_posts:
            if post['link'] == int(post_id):
                context = post

        return render(request, "news/news.html", context=context)