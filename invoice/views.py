from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import get_template
from django.db import transaction
from django.utils.translation import gettext as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
import environ

env = environ.Env()
environ.Env.read_env()
API_KEY = env('API_KEY')

import pdfkit
import datetime

from .utils import pagination, get_invoice
from .decorators import *
from invoice.decorators import *
from .models import * 
from accounts.models import User, ClientUser



# Create your views here.

class HomeView(LoginRequiredSuperuserMixim, View):
    """ Main view """
    templates_name = 'invoice/index.html'
    invoices = Invoice.objects.select_related('client', 'save_by').all().order_by('-invoice_date_time')
    context = {
        'invoices': invoices
    }

    def get(self, request, *args, **kwags):

        items = pagination(request, self.invoices)

        self.context['invoices'] = items

        return render(request, self.templates_name, self.context)


    def post(self, request, *args, **kwagrs):

        # modify an invoice

        if request.POST.get('id_modified'):

            paid = request.POST.get('modified')

            try: 

                obj = Invoice.objects.get(id=request.POST.get('id_modified'))

                if paid == 'True':

                    obj.paid = True

                else:

                    obj.paid = False 

                obj.save() 

                messages.success(request,  _("Change made successfully.")) 

            except Exception as e:   

                messages.error(request, f"Sorry, the following error has occured {e}.")      

        # deleting an invoice    

        if request.POST.get('id_supprimer'):

            try:

                obj = Invoice.objects.get(pk=request.POST.get('id_supprimer'))

                obj.delete()

                messages.success(request, _("The deletion was successful."))   

            except Exception as e:

                messages.error(request, f"Sorry, the following error has occured {e}.")      

        items = pagination(request, self.invoices)

        self.context['invoices'] = items

        return render(request, self.templates_name, self.context)    


class AddClientView(LoginRequiredSuperuserMixim, View):
     """ add new customer """    
     template_name = 'invoice/add_client.html'

     def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

     def post(self, request, *args, **kwargs):
        
        data = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'gender': request.POST.get('gender'),
            'age': request.POST.get('age'),
            'location': request.POST.get('location'),
            'city': request.POST.get('city'),
            'address': request.POST.get('address'),
            'zip_code': request.POST.get('zip'),
            'save_by': request.user

        }

        try:
            created = ClientUser.objects.create(**data)

            if created:

                messages.success(request, "Client registered successfully.")

            else:

                messages.error(request, "Sorry, please try again the sent data is corrupt.")

        except Exception as e:    

            messages.error(request, f"Sorry our system is detecting the following issues {e}.")

        return render(request, self.template_name)   



class AddInvoiceView(LoginRequiredSuperuserMixim, View):
    """ add a new invoice view """

    template_name = 'invoice/add_invoice.html'

    clients = ClientUser.objects.select_related('save_by').all()

    context = {
        'clients': clients
    }

    def get(self, request, *args, **kwargs):
        return  render(request, self.template_name, self.context)

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        
        items = []

        try: 

            client = request.POST.get('client')

            type = request.POST.get('invoice_type')

            articles = request.POST.getlist('article')

            qties = request.POST.getlist('qty')

            units = request.POST.getlist('unit')

            total_a = request.POST.getlist('total-a')

            total = request.POST.get('total')

            comment = request.POST.get('commment')

            invoice_object = {
                'client_id': client,
                'save_by': request.user,
                'total': total,
                'invoice_type': type,
                'comments': comment
            }

            invoice = Invoice.objects.create(**invoice_object)

            for index, article in enumerate(articles):

                data = Article(
                    invoice_id = invoice.id,
                    name = article,
                    quantity=qties[index],
                    unit_price = units[index],
                    total = total_a[index],
                )

                items.append(data)

            created = Article.objects.bulk_create(items)   

            if created:
                messages.success(request, "Data saved successfully.") 
            else:
                messages.error(request, "Sorry, please try again the sent data is corrupt.")    

        except Exception as e:
            messages.error(request, f"Sorry the following error has occured {e}.")   

        return  render(request, self.template_name, self.context)


class InvoiceVisualizationView(LoginRequiredSuperuserMixim, View):
    """ This view helps to visualize the invoice """

    template_name = 'invoice/invoice.html'

    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')

        context = get_invoice(pk)

        return render(request, self.template_name, context)



@employee_required
@superuser_required
def get_invoice_pdf(request, *args, **kwargs):
    """ generate pdf file from html file """

    pk = kwargs.get('pk')

    context = get_invoice(pk)

    context['date'] = datetime.datetime.today()

    # get html file
    template = get_template('invoice/invoice_pdf.html')

    # render html with context variables

    html = template.render(context)

    # options of pdf format 

    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        "enable-local-file-access": ""
    }

    # generate pdf 

    pdf = pdfkit.from_string(html, False, options)

    response = HttpResponse(pdf, content_type='application/pdf')

    response['Content-Disposition'] = "attachement"

    return response


def invoice_live(request):

    url = "https://api-football-beta.p.rapidapi.com/fixtures"

    querystring = {"live":"all"}

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "api-football-beta.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    #print(response.json())
    data = response.json()

    data = data['response']


    return render(request, 'invoice/live.html', {'data': data})


def team_details(request, pk):

    API_KEY = env('API_KEY')
    fixture = pk

    url = "https://api-football-beta.p.rapidapi.com/teams"# fixtures live

    querystring = {"id":fixture}

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "api-football-beta.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()

    responses = data['response']
    return render(
        request=request,
        template_name='invoice/team.html',
        context={'responses': responses}
    )
        
def odd_by_fixture(request, pk):

    API_KEY = env('API_KEY')
    fixture = pk

    url = "https://api-football-beta.p.rapidapi.com/odds"

    querystring = {"fixture": fixture}

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "api-football-beta.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()

    responses = data['response']
    #print(responses)
    return render(
        request=request,
        template_name='invoice/odd_by_fixture.html',
        context={'responses': responses}
    )


def odd_by_bets(request, pk, pid):

    API_KEY = env('API_KEY')
    bookmaker = pid
    fixture = pk

    url = "https://api-football-beta.p.rapidapi.com/odds"

    querystring = {"bookmaker":bookmaker,"fixture":fixture}

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "api-football-beta.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()
    responses = data['response']

    #print(responses)
    return render(
        request=request,
        template_name='invoice/odd_by_bets.html',
        context={'responses': responses}
    )


#def odd_complementary(request, pk):

#   API_KEY = env('API_KEY')
#    fixture = pk

#    url = "https://api-football-beta.p.rapidapi.com/teams"# fixtures live

#    querystring = {"id":fixture}

#    headers = {
#        "X-RapidAPI-Key": API_KEY,
#        "X-RapidAPI-Host": "api-football-beta.p.rapidapi.com"
#    }

#    response = requests.get(url, headers=headers, params=querystring)

#    data = response.json()

#    fixtures = data['response']
#    print(fixtures)
#    return render(
#        request=request,
#        template_name='invoice/odd_by_bets.html',
#        context={'fixtures': fixtures}
#    )
