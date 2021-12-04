from django.shortcuts import render
from .forms import ProductForm
# Create your views here.

def Home(request):
    form = ProductForm()
    return render(request, 'base.html', {'form': form})


def get_pd(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'base.html', {'form': form})