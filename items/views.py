import random
from datetime import timedelta
from django.template.defaultfilters import date as _date

from django.contrib import messages
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import ListView, DetailView

from items.models import Expert, History
from users.forms import UserForm


class HomeView(View):

    def get(self, request):
        form = UserForm()
        history_list = History.objects.all()[:5]
        history_count = History.objects.count()
        return render(request, 'home.html', locals())

    def post(self, request):
        form = UserForm(request.POST)
        history_list = History.objects.all()[:5]
        history_count = History.objects.count()
        if form.is_valid():
            book = form.cleaned_data.get('book')
            _type = form.cleaned_data.get('type')
            okuu_kitep = authenticate(username=form.cleaned_data.get('okuu_kitep'),
                                      password=form.cleaned_data.get('okuu_kitep_password'))
            sector_knigi = authenticate(username=form.cleaned_data.get('sector_knigi'),
                                        password=form.cleaned_data.get('sector_knigi_password'))
            if okuu_kitep and okuu_kitep.category == 'okuu_kitep' and sector_knigi and sector_knigi.category == 'sector_knigi':
                prev_month = now().today() - timedelta(days=30)
                valid_expert_list = Expert.objects.filter(book=book)
                history = History.objects.filter(book=book, created__gte=prev_month)
                if history.exists():
                    valid_expert_list.exclude(history=history)
                if valid_expert_list.exists():
                    winner = random.choice(valid_expert_list)
                    document = f'''<div class="print-container">
                               <div class="text-center title"><strong>Эксперт Тандоо </strong></div>
                                <div class="d-flex mt-5">
                               <div class="mr-auto"><p> Бишкек ш. </p></div>
                               <div class="ml-auto"><span>{_date(now(), 'j-F Y')} ж.</span></div></div>
                               <p class="mt-3">{winner.fullname}</p>
                               <p class="mt-2">Окуу китепбинин аталышы {book.name}</p>
                               <p class="mt-2">окуу усулдук комплексине {_type} экспертиза
                                жүргүзүү үчүн эксперт катары тандалды</p>
                               <p class="mt-2">Комиссия:</p>
                               <p class="mt-2">{okuu_kitep.fullname} ________________</p>
                               <p class="mt-2">{sector_knigi.fullname} _______________</p>
                               <p class="mt-2">Көзөмөлдөөчүлөр:</p>
                               <p class="mt-2">______________________________________________</p>
                               <p class="mt-2">______________________________________________</p>
                               <p style="margin-top: 150px">Документтин аныктыгын төмөнкү QR код аркылуу текшерип алыңыз.</p>
                               <div id="qrcode" style="margin-top: 10px;"></div>
                               </div>
                               '''
                    history = History.objects.create(winner=winner, book=book,
                                                     okuu_kitep=okuu_kitep, sector_knigi=sector_knigi,
                                                     document=document)
                    return render(request, 'victory.html', locals())
                messages.add_message(request, messages.ERROR, _(f'The book {book.name} has no experts'),
                                     'alert-danger')
                return render(request, 'home.html', locals())
            else:
                messages.add_message(request, messages.ERROR, _('Please enter the correct username '
                                                                'and password for a staff account. '
                                                                'Note that both fields may be case-sensitive.'),
                                     'alert-danger')
                return render(request, 'home.html', locals())
        return render(request, 'home.html', locals())


class HistoryListView(ListView):
    model = History
    paginate_by = 5


class HistoryDetailView(DetailView):
    model = History


class ExpertListView(ListView):
    model = Expert
    paginate_by = 5


class ExpertDetailView(DetailView):
    model = Expert
