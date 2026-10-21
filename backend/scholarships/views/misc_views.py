from django.shortcuts import render

def jobs(request):
    return render(request, 'jobs/list.html', {})

def payment_form(request):
    return render(request, 'payment/form.html', {})

def about(request):
    return render(request, 'about/index.html', {})

def team(request):
    return render(request, 'about/team.html', {})

def contact(request):
    return render(request, 'about/contact.html', {})

def news(request):
    return render(request, 'news/list.html', {})

def faq(request):
    return render(request, 'faq/index.html', {})
