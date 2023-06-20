
from django.shortcuts import render
from django.http import JsonResponse, Http404, HttpResponse
from .models import Post
import core.geddit as geddit
import os
from django.core import management


# Get posts from a subreddit
def get_all(request):
    q = Post.objects.all().order_by('-created').values()

    if not q:
        raise Http404(
            "No entries found. Please add a subreddit to the listening Subreddit's list.")

    return JsonResponse(list(q), safe=False)


# Get posts from a subreddit
def get(request, subreddit: str):
    # Query of the post ordered by desc created time
    q = Post.objects.filter(subreddit=subreddit).order_by('-created').values()

    if not q:
        raise Http404(
            "No entries found for subreddit. Please ad a subreddit to the listening Subreddit's list.")

    return JsonResponse(list(q), safe=False)


# Add a subreddit name to subreddit listening list
def add(request, subreddit: str):
    geddit.add_subreddit(subreddit)
    result = management.call_command('update_posts')
    if result == -1:
        HttpResponse('Subreddit added to the listening list but returned no data.')
    return HttpResponse('Subreddit added to the listening list.')


# Register credentials of the user
def register(request):
    if request.method == "POST":
        # Delete tokens file
        try:
            os.remove(".geddit")
        except FileNotFoundError:
            pass

        # Delete credentials file
        try:
            os.remove(".env")
        except FileNotFoundError:
            pass

        geddit.login(request.POST['username'], request.POST['password'],
                     request.POST['cli_id'], request.POST['secret'])
        return HttpResponse('Successfully registered!')
    return render(request, 'api/register.html')
