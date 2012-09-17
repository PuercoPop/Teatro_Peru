# -*- coding: utf-8 -*-

import datetime

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
import django.contrib.auth as auth
#from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.utils import simplejson

from teatro_peru import models, forms


def cartelera(request):
    """
    template: cartelera.html
    Parametros a pasar al Template

    mes {
      size  : número de días
      name : nombre del mes
    }
    dias {
      dia : fechas incluidas
    }
    obras {
      titulo: título de la obra
      width: duración de la obra para las fechas mostradas en la carteleras
      prev_space: duración entre el día de hoy ya la primera fecha
    }
    """

    m_mes = {
                1: 'Enero',
                2: 'Febrero',
                3: 'Marzo',
                4: 'Abril',
                5: 'Mayo',
                6: 'Junio',
                7: 'Julio',
                8: 'Agosto',
                9: 'Septiembre',
                10: 'Octubre',
                11: 'Noviembre',
                12: 'Diciembre'
            }
    today = datetime.date.today()
    lastday = today + datetime.timedelta(45)
    day_ptr = datetime.date.today()

    dias = []
    for count in xrange(45):
        dias.append({
                        'ano': day_ptr.year,
                        'mes': day_ptr.month,
                        'dia': day_ptr.day
                    })
        day_ptr = day_ptr + day_ptr.resolution

    #meses = set( [ mes['mes'] for mes in dias ] )
    meses = [mes['mes'] for mes in dias]

    #eliminar duplicados preservando el orden
    u_meses = set()
    u_meses = [x for x in meses if x not in u_meses and not u_meses.add(x)]
    #u_meses = set(meses)
    times = []
    for item in u_meses:
        times.append(meses.count(item))

    #Map month number to name. And encode size
    d_meses = []
    for num_mes, veces in zip(u_meses, times):
        d_meses.append({'name': m_mes[num_mes], 'size': veces})

    #Construct the obras parameters
    obras = []
    for item in models.Showing.objects.filter(
                                            season_end__gte=today
                                        ).filter(
                                                season_start__lte=lastday
                                        ):
        obra = {}
        obra['titulo'] = item.obra.titulo
        obra['plaza'] = item.plaza.nombre
        obra['puesta_id'] = item.id
        obra['id'] = item.obra.id

        #Si la fecha de inicio es anterior
        #If 0 > Then the play ends before the end of the calendar
        diff_start = item.season_start - today
        diff_end = lastday - item.season_end
        if (item.season_start - today).days > 0:
            obra['prev_space'] = (item.season_start - today).days
            if (lastday - item.season_end).days > 0:
                obra['width'] = (item.season_end - item.season_start).days
            else:
                obra['width'] = (lastday - item.season_start).days
        else:
            obra['prev_space'] = 0
            if diff_end.days > 0:
                obra['width'] = (item.season_end - today).days
            else:
                obra['width'] = (lastday - today).days

        diff_end = lastday - item.season_end

        obras.append(obra)

    return render(
            request,
            'teatro_peru/cartelera.html',
            {
                'obras': obras,
                'meses': d_meses,
                'dias': dias,
            })


def show_showing(request, puesta_id):
    obra = get_object_or_404(Showing, pk=obra_id,)
    return render(
                render,
                'teatro_peru/puesta.html',
                {'puesta': puesta},
            )


def show_play(request, play_id):
    """
    Show info regarding a Play's showing
    """
    obra = get_object_or_404(Play, pk=play_id,)

    return render(
        request,
        'teatro_peru/obra.html',
        {'obra': obra},
        )


def elenco_view(request, elenco_id):
    try:
        miembro_elenco = models.CastMember.objects.get(id=elenco_id)
    except ObjectDoesNotExist:
        return render(
                    'Forever404.html',
                    {'name': elenco_id},
                )
    return render(
                request,
                'elenco.html',
                {'elenco': miembro_elenco},
            )


def billboard_at_date(request, year=None, month=None, day=None):
    """
    First we search for all the showings that start befor the date and end after the date. Then we make sure that there is a showing for this day of the week. If no date is provided then the date defaults to today.
    """
    if (year is None) and (month is None) and (day is None):
        date_target = datetime.date.today()
    else:
        date_target = datetime.date(int(year), int(month), int(day))
    
    query = models.Showing.objects.filter(season_end__gte=date_target).filter(season_start__lte=date_target)

    if date_target.weekday() == 0:
        target_day = 'L'
    elif date_target.weekday() == 1:
        target_day = 'M'
    elif date_target.weekday() == 2:
        target_day = 'X'
    elif date_target.weekday() == 3:
        target_day = 'J'
    elif date_target.weekday() == 4:
        target_day = 'V'
    elif date_target.weekday() == 5:
        'S'
    elif date_target.weekday() == 6:
        target_day = 'D'

    result = query.filter(schedule__day__exact=target_day)

    return render(
        request,
        'teatro_peru/cartelera_day.html',
        {
            'fecha': date_target,
            'puestas': result,
            'fecha_next': date_target + datetime.timedelta(1),
            'fecha_prev': date_target - datetime.timedelta(1),}
        )


def log_user(request):
    if request.POST:
        user = auth.authenticate(username=request.POST['name'],
                password=request.POST['password'])
        if user is not None and user.is_active:
            print "You provided a correct username and password!"
            auth.login(request, user)
            return redirect('/')
        else:
            print "Your username and password were incorrect."
            return render('teatro_peru/login_form.html', {})
    else:
        return render('teatro_peru/login_form.html', {})


def logout_user(request):
    auth.logout(request)
    if request.GET:
        return redirect(request.GET['url'])
    return redirect('/hoy/')


def create_user(request):
    """
    TODO: Evaluate if one can use partials for form
    """
    if request.method == "POST":
        form = forms.UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return render(
                        request,
                        'teatro_peru/created_user.html',
                        {'user': user},
                    )
        else:
            return render(
                        request,
                        'teatro_peru/create_user.html',
                        {'form': form},
                    )
    else:
        form = forms.UserProfileForm()
        return render(
            request,
            'teatro_peru/create_user.html',
            {'form': form,},
            )


def show_plaza(request, id):
    return HttpResponse('I O U')


def crear_puesta(request):
    if request.method == "POST":
        pass
    else:
        pass
    return render(
            request,
            'teatro_peru/crear_puesta.html',
            {
                'form': forms.Showing
            })


def search_by_title(request):
    """
    Search by title autocomplete
    TODO: why render_to_string and not render?
    """
    if request.GET:
        pattern = request.GET[u'term']
        result = models.Obra.objects.filter(titulo__icontains=pattern)
        if result.count() >= 1:
            html_str = render_to_string('teatro_peru/show_obra.html',
                    {'obras': result})
            return HttpResponse(html_str,
                                mimetype='application/json',)
        else:
            return HttpResponse('', mimetype='application/json')
    else:
        return HttpResponse('', mimetype='application/json')


def validate_entrada(request):
    if request.POST:
        entradaForm = forms.Entrada(
                {
                    'name': request.POST['entrada'],
                    'cost': request.POST['costo'],
                })
        if entradaForm.is_valid():
            q = entradaForm.save(commit=False)
            html_str = render_to_string(
                    'teatro_peru/show_entrada.html',
                    {'m_entrada': q}
                    )
            return HttpResponse(html_str)
    return HttpResponse('No Parameters')


def validate_cast(request):
    if request.POST:
        elencoForm = forms.Elenco_val(
                {
                    'nombre': request.POST['nombre'],
                    'posicion': request.POST['posicion']
                })
        if elencoForm.is_valid():
            q = {
                    'nombre': request.POST['nombre'],
                    'posicion': request.POST['posicion']
                }
            html_str = render_to_string(
                    'show_elenco.html',
                    {'m_elenco': q}
                    )
            return HttpResponse(html_str)
    return HttpResponse('No Parameters')
