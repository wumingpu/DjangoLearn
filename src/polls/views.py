#from django.shortcuts import render
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.template import RequestContext,loader
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from .models import Question,Choice 

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        #return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    
    #output = ','.join([p.question_text for p in latest_question_list])
    #return HttpResponse("Hello, world. You're at the polls index.")
    #return HttpResponse(output)
    
    #template = loader.get_template('polls/index.html')
    #context = RequestContext(request,{
    #    'latest_question_list' : latest_question_list,
    #})
    #return HttpResponse(template.render(context))

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    #try:
    #    question = Question.objects.get(pk=question_id)
    #except Question.DoesNotExist:
    #    raise Http404("Question does not exist")
    #return HttpResponse("You're looking at question %s." % question_id)
    #question = get_object_or_404(Question,pk=question_id)
    #return render(request,'polls/detail.html',{'question':question})

class ResultsView(generic.DetailView):
    model=Question
    template_name='polls/results.html'
    #response = "You're looking at the results of question %s."
    #return HttpResponse(response % question_id)

def vote(request,question_id):
    p=get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist): # KeyError是字典方法request.POST找不到值引发的。
        return render(request,'polls/detail.html',{
            'question':p,
            'error_message':"You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        #return HttpResponse("You're voting on question %s." % question_id)
        return HttpResponseRedirect(reverse('polls:results',args=(p.id,)))
        #reverse函数是为了避免在视图中硬编码url，它将返回字符串/polls/3/results/
        
def results(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    return render(request,'polls/results.html',{'question':question})