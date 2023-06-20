
from http import HTTPStatus
from django.http import JsonResponse, Http404, HttpResponse
from .models import Post
import core.geddit as geddit


def get(request, subreddit: str):
    # Query of the post ordered by desc created time
    q = Post.objects.filter(subreddit=subreddit).order_by('-created')

    if not q:
        raise Http404(
            "No entries found for subreddit. Please add subreddit to the listening Subreddit's list.")

    return JsonResponse(list(q), safe=False)


def add(request, subreddit: str):
    geddit.add_subreddit(subreddit)
    return HttpResponse('Subreddit added to the listening list.')
