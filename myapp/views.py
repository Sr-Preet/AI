import datetime

from django.shortcuts import render, redirect
from myapp.forms import ImageForm, ChatterForm
from myapp.models import Image, Chatter
import requests
import Algorithmia

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


def chat(request):
    return render(request, 'chatbot.html', {})


def chatter(request):
    context = {}
    form = ChatterForm()
    context['form'] = form
    start = datetime.datetime.today()
    end = start - datetime.timedelta(days=7)
    x = Chatter.objects.all().filter(date_added__range=[end, start])
    if request.method == 'POST':
        t = request.POST['txt']
        input = {
            "text": str(t),
            "language": "en",
            "replacer": "*"
        }
        client = Algorithmia.client('simSOfi6O34iCn1hnqpkdWIT2Wx1')
        algo = client.algo('FedericoV/ProphanityFilter/0.1.1')
        x = algo.pipe(input).result
        t = x['filtered text']
        obj = Chatter.objects.create(txt=t)
        obj.save()
        x = Chatter.objects.all().filter(date_added__range=[end, start])
    context['txt'] = x
    return render(request, 'chatter.html', context)


def soss(request):
    return render(request, 'soss.html', {})


def comp(request):
    context = {}
    lang = {
        'C': 'C',
        'C++': 'CPP',
        'C#': 'CSHARP',
        'JAVA': 'JAVA',
        'Perl': 'PERL',
        'PHP': 'PHP',
        'Python': 'PYTHON3',
        'R': 'R',
        'Ruby': 'RUBY',
    }
    context['lang'] = lang
    if request.method == "POST":
        ln = request.POST['lng']
        src = request.POST['source']
        RUN_URL = u'https://api.hackerearth.com/v3/code/run/'
        CLIENT_SECRET = '469547230aac11857e2ef259e4ca5122bd9d63a6'

        source = "print 'Hello World'"

        data = {
            'client_secret': CLIENT_SECRET,
            'async': 0,
            'source': src,
            'lang': ln,
            'time_limit': 5,
            'memory_limit': 262144,
        }

        r = requests.post(RUN_URL, data=data)
        out = r.json()
        out = out['run_status']
        if 'output_html' in out:
            context['res'] = out['output_html']
            context['src'] = src
        else:
            context['res'] = out['status_detail']
            context['src'] = src
        return render(request, 'compiler.html', context)
    return render(request, 'compiler.html', context)
