from django.shortcuts import render, redirect
from myapp.forms import ImageForm
from myapp.models import Image
import requests

CONSTANT = 1


# Create your views here.

def home(request):
    return render(request, 'home.html', {})


def image(request):
    context = {}
    form = ImageForm()
    context['form'] = form
    if 'id' in request.session:
        try:
            del request.session['id']
            print('deleted')
        except:
            pass
        return redirect('myapp:color')
    Image.objects.all().delete()
    if request.method == 'POST':
        request.session['id'] = CONSTANT
        x = ImageForm(request.POST or None, request.FILES or None)
        if x.is_valid():
            x.save()
            obj = Image.objects.all()
            for i in obj:
                ur = i.img.url
                r = requests.post(
                    "https://api.deepai.org/api/colorizer",
                    files={
                        'image': open(f"{i.img.url}".lstrip('/'), 'rb'),
                    },
                    headers={'api-key': '26b262fa-e8f6-49dd-90ba-a452658e04f0'}
                )
                context['color'] = r.json()
                context['original'] = obj
                return render(request, 'image.html', context)
    return render(request, 'image.html', context)


def love(request):
    context = {}
    if request.method == "POST":
        boy = request.POST['boy']
        girl = request.POST['girl']
        url = "https://love-calculator.p.rapidapi.com/getPercentage"

        querystring = {"fname": boy, "sname": girl}

        headers = {
            'x-rapidapi-host': "love-calculator.p.rapidapi.com",
            'x-rapidapi-key': "2685d9224cmshf5c9ac312582c02p1a6081jsn90f45cc94f80"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        dic = response.text
        dic = dic.split(',')
        per = dic[2].split(':')
        res = dic[3].split(':')
        r = res[1]
        r = r.rstrip('}')
        r = r.strip('"')
        p = per[1]
        p = p.strip('"')
        context['perc'] = p
        context['res'] = r
        return render(request, 'love.html', context)
    return render(request, 'love.html', {})


def collatz(request):
    context = {}
    if request.method == "POST":
        ls = []
        num = request.POST['num']
        num = int(num)
        count = 0
        it = 0
        while count < 1:
            ls.append(num)
            if num == 1:
                count = count + 1
            if num % 2 == 0:
                num = num // 2
            else:
                num = 3 * num + 1
            it = it + 1
        context['ls'] = ls
        context['it'] = it
    return render(request, 'collatz.html', context)
