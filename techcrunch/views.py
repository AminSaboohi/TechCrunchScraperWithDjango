from django.shortcuts import render, redirect

from django.views.generic import ListView

# Create your views here.
from .forms import SearchByKeywordForm
from django.contrib.auth import logout

from django.contrib import messages
from .models import Keyword
from django.views import generic
from django.urls import reverse_lazy
from .forms import SignUpForm


from .tasks import techcrunch_search_by_keyword_task


# Create your views here.

def search_by_keyword_view(request):
    if request.method == 'POST':
        form = SearchByKeywordForm(request.POST, )
        if form.is_valid():
            data = {
                'keyword': form.cleaned_data['keyword'],
                'page_count': form.cleaned_data['page_count'],
            }
            print(data)

            result = techcrunch_search_by_keyword_task.delay(
                keyword=form.cleaned_data['keyword'],
                page_count=form.cleaned_data['page_count'],
            )
            print('techcrunch_search_by_keyword_task', result)
    else:
        form = SearchByKeywordForm()

    return render(request, template_name='techcrunch/search_by_keyword.html',
                  context={'form': form})


def logout_user(request):
    logout(request)
    messages.success(request, message="You Have Been Logged Out...")
    return redirect('home')


class HomeView(ListView):
    model = Keyword
    template_name = 'techcrunch/home.html'
    ordering = ['id']


class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
