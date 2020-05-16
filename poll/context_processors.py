from poll.models import Questions

def polls_count(request):
    cnt = Questions.objects.count()
    return {"polls_count": cnt}