from django.http import HttpResponse
from django.shortcuts import  render
from django.template.loader import get_template

# Don't Repeat Yourself = DRY

def home_page(request):
    title = "Hello there"
    context = {"title": title}
    return render(request, "home.html", context)

def about_page(request):
    return render(request, "about.html", {"title": "About us"})

def contact_page(request):
    return render(request, "hello.html", {"title": "Contact us"})

def example_page(request):
    context = {"title": "Example"}
    template_name = "hello.html"
    template_obj = get_template(template_name)
    render_item = template_obj.render(context)
    return HttpResponse(render_item)
