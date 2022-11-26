from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout #averiguar sobre esto
from django.contrib import messages
#from main.consts import BUNIT_OPTIONS
from .models import Database, Empleados, Event
from django.contrib.auth.models import Group, Permission, User
#from .filters import databasefilter
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, EventForm, databasefilter, dataForm
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
from dateutil.relativedelta import relativedelta
from datetime import date
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .tasks import send_mail_task
#Problemas

# Como mostrar los datos guardados en un enlace (listo)
# Como encontrar los status y estado de la renovacion y donde mostrarlo (listo - consultar)
# Como eliminar los cambios hechos que se muestran (listo)
# Retroceder de pagina en pagina (show_changes) (listo)
# Mensjae para el caso de subscribir (listo)
# Correo informativo para rrhh (listo) 
# Crear cuentas por roles.. (listo)
# Mandar el mensaje cuando esta cerca el vencimiento de contrato ...(listo)
# Poner un numero a los nombres de show_changes (listo)
# Arreglar ese filtro 
# Agregar los decoradores 
# El orden al retroceder
# En update uno no debe ser capaz de modificar el nombre
# Prohibir que renueve dos veces
# Agregar un check en show_changes
# Los administradores tienen que tener la posibilidad de eliminar un queryset directo de contratos
#Para prohibir el acceso desde home a loginpage o register es necesario una autenticacion
# Arreglar los mensajes al realizar una accion
#https://realpython.com/manage-users-in-django-admin/

@unauthenticated_user
def loginpage(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "El usuario o contraseña es incorrecto") 

    context = {}
    return render(request, 'login.html', context)

@unauthenticated_user
def registerpage(request):
    
    register = CreateUserForm()
    if request.method == 'POST':
        register = CreateUserForm(request.POST)
        if register.is_valid():
            register.save()
            user = register.cleaned_data.get('username')
            messages.success(request,'Cuenta fue creada por' + "" + user) #Muestra un mensaje sobre la cuenta en el login

            return redirect('loginpage')

    context = {'register': register}
    return render(request, 'register.html', context)

def logoutuser(request):
    logout(request)
    return redirect('loginpage')

#agregar decorador del registerpage
#User.objects.filter(group__name="admin")

#@allowed_users(allowed_roles=['admin'])
def home(request): 

    data = Database.objects.all()
    bunit_table = Database.objects.values("bunit").distinct()
    boss_table = Database.objects.values("bossname").distinct()
    #users=User.objects.filter(group__name="admin")
    #print(users)
    #contratos = Database.objects.get(id=pk)
    #context = {'contratos':contratos}

    return render(request,'home.html')

#def test(request):
#Reconocer que el valor del item.name es igual al del eventform
#Foreignkey entre los valores despegables y el database model

@login_required(login_url='loginpage')
#@allowed_users(allowed_roles=['admin','usuarios'])

#contrt_id
def contratos(request):
    # Los de recursos humanos van renovar? 
    #data = Database.objects.filter(bossname = request.user.username)
    #if request.user.groups.filter(name="usuarios").exists(): 
    #    data = Database.objects.filter(bossname = request.user.username)
    #    for i in range(0,len(data)):
    #        x_id = data[i].id # Empleado Fitz
    #        Do = Database.objects.get(pk = x_id)
    #        De = Do.event_set.all() #Todos los que ha sido renovados
##
    #        if De!= Event.objects.none(): #Si De no es un query vacio
    #            x_cs = Do.contractenddate
    #            x_pr = De[i].plazo_renovacion #Supongamos que solamente se va renovar de una misma peronsa una sola vez
    #            renovacion_value = int(x_pr)
    #            new_emp_contractend = x_cs.date() + relativedelta(months=renovacion_value)
    #            Do.contractenddate = new_emp_contractend 
    #            Do.save()
    #        else:
    #            print("No se ha renovado para el jefe")
    # Para el caso en el que el admin tmb quiera hacer cambios 
####
    #Do = Database.objects.get(pk=Eoid)
    #Do.contractenddate = neoce
    #Do.save()
    #Tengo que econtrar el plazo_renovacion

    #empleados = Database.objects.filter(status="Por vencer").values().distinct()
    #emails = []
    #for emp in empleados:
    #    emails.append(emp['bossname'])

    #empleados = Database.objects.filter(status="Por vencer").values().distinct()
    #emails = []
    #for emp in empleados:
    #    emails.append(emp['bossmail'])
#
    #print(emails)
#
    #emails_unit = list(set(emails))
    #print(emails_unit)

    #for person in emails_unit:
    #    print(person)
    #    print(type(person))


    #names_boss = Database.objects.filter(bossmail="paul.pillhuaman@unmsm.edu.pe", status="Por vencer").values()
    #print(names_boss)
    #for i in range(0,len(names_boss)):
    #    names.append(names_boss[i]['name'])
    #
    #print(names)

    if request.user.groups.filter(name="admin").exists(): 
        data = Database.objects.all()
        myFilter = databasefilter(request.GET, queryset = data)
        filter = myFilter.qs

        #context = { 'myFilter': myFilter, 'filter': filter }
    elif request.user.groups.filter(name="usuarios").exists(): 
        data_user = Database.objects.filter(bossname = request.user.username)
        myFilter = databasefilter(request.GET, queryset = data_user)
        filter = myFilter.qs

        #context = { 'myFilter': myFilter, 'filter': filter }
    p = Paginator(filter,30)
    page = request.GET.get('page')
    pagination = p.get_page(page)
    #num = "a" * pagination.paginator.num_pages
    try:
        pagination = p.get_page(page)
    except PageNotAnInteger:
        pagination = p.page(1)
    except EmptyPage:
        pagination = p.page(p.num_pages)

    num = pagination.paginator.num_pages
    #print(num)
    nums = []
    for i in range(1,num+1):
        nums.append(i)

    context = { 'myFilter': myFilter, 'filter': filter , 'pagination': pagination, "nums": nums}


    return render(request, 'contratos.html', context) 


#@allowed_users(allowed_roles=['admin','usuarios'])
def events(request, event_id):

    database = Database.objects.get(pk= event_id)
    #x = database.event_set.all()[0].id
    #varact = Event.objects.get(pk=x)
    #print(varact)
    #x = database.event_set.id
    #varact = Event.objects.get(pk = x)
    name_emp = database.name
    empemail_emp = database.empemail
    bmpposition_emp = database.bmpposition
    bossname_emp = database.bossname
    bossmail_emp = database.bossmail
    contractstartdate = database.contractstartdate
    contractenddate = database.contractenddate
    today = date.today()

    print(name_emp)

    submitted = False
    form = EventForm(request.POST or None)
    #form = EventForm(initial={'Empleados': name_emp})

    if request.method == 'POST':
        #form = EventForm(request.POST)
        template = render_to_string( 'message.html', {'name': request.user.username, 'usuario': database.name, 'hoy': today} )
        email_addres = 'paul.pillhuaman@unmsm.edu.pe'
        #event = database.event_set.all()
        #name_empleado = event[0].Empleados
        name_empleado = database.id

        #form = EventForm(initial={'Empleados': name_emp})
        if form.is_valid():
            #form.cleaned_data['Empleados'] = name_emp
            form.save()
            return HttpResponseRedirect('/contratos?submitted=True')
            #send_mail_task.delay(email_addres,template)
            #email.fail_silently=False
        else:
            form = EventForm() #Eventform
            if 'submitted' in request.GET:
                submitted = True


    context ={'form':form, 'submitted': submitted, 'name_emp':name_emp, 'empemail_emp':empemail_emp, 'bmpposition_emp':bmpposition_emp, 
    'bossname_emp':bossname_emp, 'bossmail_emp':bossmail_emp, 'contractenddate': contractenddate, 'contractstartdate': contractstartdate, 'database': database }

    #request.post.get()
    return render(request, 'event.html', context)


#def send_emails():


#allowed_users(allowed_roles=['admin','usuarios'])
def show_changes(request):

    #data = Database.objects.all()
    #datupd = data.filter(plazo_renovacion="3 MESES")
    #event = Event.objects.all()
    #Empleado = Event.objects.values('Empleados').distinct()
    #print(request.user.username)
    #context = {'Empleado': Empleado, 'event': event}

    if request.user.groups.filter(name="admin").exists():
        data = Event.objects.all().order_by('id')
        Empleado = Event.objects.values('Empleados')
        #context = {'Empleado': Empleado, 'event': event}
        context = { 'data': data}
    
    elif request.user.groups.filter(name="usuarios").exists():
        data_all = Database.objects.filter(bossname = request.user.username).order_by('id')
        data = Event.objects.none() #Declara un query vacio 
        for i in range(0,len(data_all)):
            data = data | data_all[i].event_set.all()
            #data = data_all[0].event_set.all() | data_all[1].event_set.all() | data_all[2].event_set.all()
        context = { 'data': data }

    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST.get('actionname')
            if action == 'delete':
                id_list = request.POST.getlist('idcheckbox')
                for id in id_list:
                    event = Event.objects.get(pk = id)
                    name_delete = event.Empleados
                    name = str(name_delete)
                    event.delete()
                    messages.success(request, 'Has eliminado la renovacion de:'+ " " + name )

                print("funciona")
                return redirect('show_changes')
            #elif action == 'no_action':
            #    
            #    
#
            #    return redirect('show_changes.html')
        

            #id_list = request.POST.getlist('idcheckbox')
            #for id in id_list:

    #https://stackoverflow.com/questions/431628/how-can-i-combine-two-or-more-querysets-in-a-django-view

    return render(request, 'show_changes.html', context)

#urls dinamicas

#@allowed_users(allowed_roles=['admin'])
#allowed_users(allowed_roles=['admin','usuarios'])
def update_event(request, event_id):
    
    event = Event.objects.get(pk= event_id)
    form = EventForm(request.POST or None, instance = event) 
    #name = form.get('Empleados')
    if form.is_valid():
        form.save()
        name_update = form.cleaned_data.get('Empleados')
        name_str = str(name_update)
        messages.success(request, 'Has actualizado la renovacion de:'+ " " + name_str)

        return redirect('show_changes')

    #instance what i put in the form ?
    context = {'event': event, 'form':form, 'event':event }
    return render(request, 'update_event.html', context)

@allowed_users(allowed_roles=['admin'])
def update_rrhh(request, event_id):

    Eo = Event.objects.get(pk=event_id)
    databaseid = Eo.Empleados.id
    Do = Database.objects.get(pk = databaseid)
    form = dataForm(request.POST or None, instance = Do)
    if form.is_valid():
        form.save()

        return redirect('show_changes')

    context = {'form': form, 'databaseid': databaseid}
    return render(request, 'editar_admin.html', context)

@allowed_users(allowed_roles=['admin'])
def delete_event(request, event_id):
    event = Event.objects.get(pk = event_id)
    name_delete = event.Empleados
    name = str(name_delete)
    event.delete()
    messages.success(request, 'Has eliminado la renovacion de:'+ " " + name )
    return redirect('show_changes')



@login_required(login_url='loginpage') # Esto principalmente te bloquea la entrada a comosiones desde el loginpage
def comisiones(request):
    return render(request, 'comisiones.html')

@login_required(login_url='loginpage')
def constancias(request):
    return render(request, 'constancias.html')

#def second(render):
#    return render()