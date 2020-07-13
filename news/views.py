import json
import datetime
import pdb

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views import View
from hypernews.settings import NEWS_JSON_PATH
import os


# Create your views here.



class HomePageView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Coming Soon')





class MainPageView(View):
    # create new view function for the hyper news page
    def get(self, request, *args, **kwargs):
        context = {}
        context['posts'] = []

        posts_by_date = self.load_posts()
        for key in sorted(posts_by_date.keys()):
            context['posts'].append([key, posts_by_date[key]])
        return render(request, 'news/news_home.html', context=context)

    def load_posts(self):
        try:
            with open(NEWS_JSON_PATH) as json_posts:
                posts_list = json.load(json_posts)
                return(self.post_by_date(posts_list))
        except:
            return 'Posts Not Found'

    def post_by_date(self, posts_list):
        output_dict = {}
        for post in posts_list:
            date = post["created"]
            formatted_post_date = datetime.datetime(*[int(ele) for ele in date[:10].split('-')])
            try:
                output_dict[formatted_post_date].append(post)
            except KeyError:
                output_dict[formatted_post_date] = [post]
        return output_dict




class NewsView(View):

    def get(self, request, post_id, *args, **kwargs):
        if not os.path.exists(NEWS_JSON_PATH):
            post_array = [
            {
            "created": "2020-02-22 16:40:00",
            "text": "A new star appeared in the sky.",
            "title": "The birth of the star",
            "link": 9234732 }]
            with open(NEWS_JSON_PATH, 'w') as posts:
                json.dump(post_array, posts)

        context = False

        with open(NEWS_JSON_PATH) as posts:
            array_of_posts = json.load(posts)

        for post in array_of_posts:
            if post['link'] == int(post_id):
                context = post

        if not context:
            raise Http404('<h1>Page not found</h1>')


        return render(request, "news/news.html", context=context)