from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from .models import Users,Travel
import bcrypt
from datetime import datetime,date,timedelta

# Create your views here.
def index(request):
    request.session['user_id']=0
    return render(request,'trip_app/index.html')


def validation(request):
    errors = Users.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
           messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        passW= bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        check=Users.objects.all()
        for item in check:
            if item.email_address==request.POST['email']:
                messages.add_message(request, messages.ERROR, "User Already exists.. Please login")
                print item.email_address
                print "User Already Exists"
                return redirect('/')
            
        use=Users.objects.create(first_name=request.POST['fName'],last_name=request.POST["lName"],email_address=request.POST['email'],password= passW)
        if use.id:
            request.session['user_id']=use.id
            return redirect('/sendtosuccess')
        else:
            messages.add_message(request, messages.ERROR, "Could not add new user.. Try again")


def success(request):
    user=Users.objects.get(id=request.session['user_id'])
    
    rest=Travel.objects.exclude(travellers=request.session['user_id']) & Travel.objects.exclude(owner=request.session['user_id'])
    for item in rest:
        print "---------------------"
        print Users.objects.filter(destina=item.id)
        print "----------------------"
    context={
        'plans':user.destina.all() | user.creator.all(),
        'name': user.first_name,
        'email':user.email_address,
        'unjoinedPlans':rest
    }

    return render(request,'trip_app/success.html',context)


def login(request):
    log=Users.objects.all()
    for value in log:
        if value.email_address==request.POST['lemail'] and bcrypt.checkpw(request.POST['lpassword'].encode(), value.password.encode()):
            request.session['user_id']=value.id
            return redirect('/sendtosuccess') 

    messages.add_message(request, messages.ERROR, "Something went wrong..check your id & password")
    return redirect('/')

def join(request,trip_id):
    print trip_id
    this_trip=Travel.objects.get(id=trip_id)
    this_user=Users.objects.get(id=request.session['user_id'])
    this_trip.travellers.add(this_user)
    return redirect('/sendtosuccess')

def display(request,trip_id):
    trip=Travel.objects.get(id=trip_id)
    Participants= Users.objects.filter(destina=trip_id)
    for i in Participants:
        print i.first_name
    context_trip={
        'things':trip,
        'people':Participants
    }
    return render(request,'trip_app/showDestination.html',context_trip)

def addtrip(request):
    return render(request,"trip_app/addtrip.html")

def add(request):
    if len(request.POST['destination'])<1 or len(request.POST['description'])<1 :
        messages.add_message(request, messages.ERROR, "All the fields are Required")
        return redirect('/addTrip')

    if request.POST['start_date'] > request.POST['end_date']:
        messages.add_message(request, messages.ERROR, "End date cannot be earlier than start")
        return redirect('/addTrip')
   
    if (datetime.today()-timedelta(days=5)) > datetime.strptime(request.POST['start_date'],'%Y-%m-%d'):
        print "---------Here---------"
        print datetime.today()+timedelta(days=5)
        print datetime.strptime(request.POST['start_date'],'%Y-%m-%d')
        print "-------------------"
        messages.add_message(request, messages.ERROR, "The date has to be in future")
        return redirect('/addTrip')


    user=Users.objects.get(id=request.session['user_id'])

    t=Travel.objects.create(destination=request.POST['destination'],start_date=request.POST['start_date'],end_date=request.POST['end_date'],plan=request.POST['description'],owner=user)

    return redirect('/destination/{}'.format(t.id),trip_id=t.id)

def logout(request):
    request.session.flush()
    return redirect('/')

def home(request):
    return redirect('/sendtosuccess')
