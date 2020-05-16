from django.shortcuts import render, HttpResponseRedirect
from django.http import Http404, HttpResponse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from poll.models import Questions, Answer, Choice
from employee.decorators import admin_hr_required, admin_only
from poll.forms import PollForm, ChoiceForm

# Create your views here.
def index(request):
    print('hiii')
    questions = Questions.objects.all()
    context = {
        "title": "Polls",
        "questions":  questions
    }
    return render(request, 'polls/index.html', context)

def details(request, id=None):
    context = {}
    try:
        question = Questions.objects.get(id=id)
        context = {
            "title": "Poll details",
            "question":  question
        }
    except Exception as e:
        print(e)
        raise Http404
    return render(request, 'polls/details.html', context)

def polls(request, id=None):
    if request.method == 'GET':
        print('hiii')
        context = {}
        try:
            question = Questions.objects.get(id=id)
        except Exception as e:
            print(e)
            raise Http404
        context['question'] = question
        return render(request, 'polls/poll.html', context)
    if request.method == 'POST':
        user_id = 1
        data = request.POST
        print(data)
        ret = Answer.objects.create(user_id=user_id, choice_id=data['answer'])
        if ret:
            return HttpResponse("Your vote is done successfully")
        else:
            return HttpResponse("Your vote is not done successfully")

class PollView(View):
    decorators = [login_required, admin_hr_required]

    @method_decorator(decorators)
    def get(self, request, id=None):
        if id:
            question = get_object_or_404(Qustions, id = id)
            poll_form = PollForm(instance=question)
            choices = question.choice_set.all()
            choice_forms = [ChoiceForm(prefix=str(
                choice.id), instance=choice) for choice in choice in choices           

            ]
            template = 'polls/edit_poll.html'
        else:
            poll_form = PollForm(instance=Questions())
            choice_forms = [ChoiceForm(prefix=str(
                x), instance=Choice()) for x in range(3)]
            template = 'polls/new_poll.html'
        context = {'poll_form': poll_form, 'choice_forms': choice_forms}
        return render(request, template, context)
    
    @method_decorator(decorators)
    def post(self, request, id=None):
        context = {}
        if id:
            return self.put(request, id)
        poll_form = PollForm(request.POST, instance=Questions())
        choice_forms = [ChoiceForm(request.POST, prefix=str(
            x), instance=Choice()) for x in range(0, 3)]
        if poll_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
            new_poll = poll_form.save(commit=False)
            new_poll.created_by = request.user
            new_poll.save()
            for cf in choice_forms:
                new_choice = cf.save(commit=False)
                new_choice.question = new_poll
                new_choice.save()
            return HttpResponseRedirect('/poll/')
        context = {'poll_form': poll_form, 'choice_forms': choice_forms}
        return render(request, 'polls/new_poll.html', context)

    @method_decorator(decorators)
    def put(self, request, id=None):
        context = {}
        question = get_object_or_404(Questions, id=id)
        poll_form = PollForm(request.POST, instance=question)
        choice_forms = [ChoiceForm(request.POST, prefix=str(
            choice.id), instance=choice) for choice in question.choice_set.all()]
        if poll_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
            new_poll = poll_form.save(commit=False)
            new_poll.created_by = request.user
            new_poll.save()
            for cf in choice_forms:
                new_choice = cf.save(commit=False)
                new_choice.question = new_poll
                new_choice.save()
            return redirect('polls_list')
        context = {'poll_form': poll_form, 'choice_forms': choice_forms}
        return render(request, 'polls/edit_poll.html', context)

    @method_decorator(decorators)
    def delete(self, request, id=None):
        question = get_object_or_404(Questions)
        question.delete()
        return redirect('polls_list')
    

