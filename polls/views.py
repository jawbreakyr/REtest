from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F
from django.urls import reverse
from django.template import loader
from django.http import Http404
from django.utils import timezone
from django.views import generic

from polls.models import Question, Choice


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     output = ', '.join([q.question_text for q in latest_question_list])
#     return HttpResponse(output)

# def index(request):
# 	latest_question_list = Question.objects.order_by('-pub_date')[:5]
# 	template = loader.get_template('polls/index.html')
# 	context = { 'latest_question_list': latest_question_list, }
# 	return HttpResponse(template.render(context, request))

# a simplified view for using a shortcut but w/o sorting
# def index(request):
#	# latest_question_list = Question.objects.order_by('-pub_date')[:5]
#	latest_question_list = get_list_or_404(Question, )
#	context = {'latest_question_list':latest_question_list}
#	return render(request, 'polls/index.html', context)

#class based views inheriting from a generic view
class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		"""Return the five published questions."""
		# return Question.objects.order_by('-pub_date')[:5]
		"""'<=' not supported between instances of 'DeferredAttribute' and 'datetime.datetime'"""
		# return Question.objects.filter(Question.pub_date <= timezone.now()).order_by('-pub_date')[:5]
		"""Return the last five published questions(not 
		including those set to be published in the future)"""
		return Question.objects.filter(
			pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


# def detail(request, question_id):
# 	try:
# 		question = Question.objects.get(pk=question_id)
# 	except Question.DoesNotExist:
# 		raise Http404("Question does not exist you shitbag.")
# 	return render(request, 'polls/details.html', {'question': question})

# a much for simplified view for details page thats renders the data using a shortcut
# def detail(request, question_id):
#	question = get_object_or_404(Question, pk=question_id)
#	return render(request, 'polls/details.html', { 'question':question })

#class based views inheriting from a generic view
class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/details.html'

# def results(request, question_id):
#	question = get_object_or_404(Question, pk=question_id)
#	return render(request, 'polls/results.html', { 'question': question })

#class based views inheriting from a generic view
class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'


def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/details.html', {
			'question': question,
			'error_message': "You didn't select a choice.",
			})
	else:
		selected_choice.votes = F('votes') + 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
	