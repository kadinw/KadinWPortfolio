from django.shortcuts import render
from django.http import Http404
from polling.models import Poll

def list_view(request):
    content = {'polls': Poll.objects.all()}
    return render(request, 'polling/list.html')

def detail_view(request, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        raise Http404
    
    if request.method == "POST":
        if request.POST.get("vote") == "Yes":
            poll.score += 1
        else:
            poll.score -= 1
        poll.save()

    context = {'poll': poll}
    return(request, 'polling/detail.html', context)