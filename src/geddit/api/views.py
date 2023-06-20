
from django.shortcuts import render
from django.http import JsonResponse, Http404, HttpResponse
from .models import Post
import core.geddit as geddit
import os
import json


def get(request, subreddit: str):
    # Query of the post ordered by desc created time
    q = Post.objects.filter(subreddit=subreddit).order_by('-created').values()

    if not q:
        raise Http404(
            "No entries found for subreddit. Please add subreddit to the listening Subreddit's list.")

    return JsonResponse(list(q), safe=False)


def add(request, subreddit: str):
    geddit.add_subreddit(subreddit)
    return HttpResponse('Subreddit added to the listening list.')


def register(request):
    if request.method == "POST":
        try:
            os.remove(".geddit")
        except FileNotFoundError:
            pass

        try:
            os.remove(".env")
        except FileNotFoundError:
            pass

        geddit.login(request.POST['username'], request.POST['password'], request.POST['cli_id'], request.POST['secret'])
        return HttpResponse('Successfully registered!')
    return render(request, 'api/register.html')