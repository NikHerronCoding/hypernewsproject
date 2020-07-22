import pdb
import json
import datetime
import random
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views import View
from hypernews.settings import NEWS_JSON_PATH
from news.forms import CreateNewsForm
import os


# Create your views here.



class HomePageView(View):

    def get(self, request, *args, **kwargs):
        return redirect('/news/')


class MainPageView(View):
    # create new view function for the hyper news page
    def get(self, request, *args, **kwargs):
        #  adding json file if it does not exist
        if not os.path.exists(NEWS_JSON_PATH):
            post_array = [
            {
            "created": "2020-02-22 16:40:00",
            "text": "A new star appeared in the sky.",
            "title": "The birth of the star",
            "link": 9234732 }]
            with open(NEWS_JSON_PATH, 'w') as posts:
                json.dump(post_array, posts)

        context = {}
        context['posts'] = []
        with open(NEWS_JSON_PATH) as path:
            posts = json.load(path)

        posts_by_date = self.load_posts()
        keys = sorted(posts_by_date.keys())
        keys.reverse()
        for key in keys:
            context['posts'].append([key, posts_by_date[key]])
        query = self.request.GET.get('q')
        if query != None:
            context = self.filter_by(posts_by_date, query, request)
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

    def filter_by(self,posts_by_date, query, request):
        context = {'posts':[]}
        for date in posts_by_date:
            for post in posts_by_date[date]:
                if query in post['title']:
                    context['posts'].append([date, [post]])
        return context




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
        # pdb.set_trace()
        with open(NEWS_JSON_PATH) as posts:
            array_of_posts = json.load(posts)

        for post in array_of_posts:
            if post['link'] == int(post_id):
                context = post

        if not context:
            raise Http404('<h1>Page not found</h1>')


        return render(request, "news/news.html", context=context)

class CreateNewsView(View):
    def get(self, request):
        form = CreateNewsForm()
        return render(request, 'news/create_news.html', {'form':form})

    def post(self, request, *args, **kwargs):
        new_post = {}
        title = request.POST.get('title')
        content = request.POST.get('content')
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        post_id = random.randint(0,100000000)

        new_post['created'] = time
        new_post['text'] = content
        new_post['title'] = title
        new_post['link'] = post_id

        with open(NEWS_JSON_PATH) as post_data:
            post_list = json.load(post_data)

        post_list.append(new_post)

        with open(NEWS_JSON_PATH, 'w') as post_data:
            json.dump(post_list, post_data)

        return redirect('/news')


