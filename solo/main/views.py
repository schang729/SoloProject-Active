from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Location, Activity
import bcrypt

def index(request):
    return render(request, "Dash/index.html")

def home(request):
    return render(request, "Dash/homepage.html")

def dashboard(request):

    if 'logged_user' not in request.session:
        messages.error(request, "Please register or log in first!")
        return redirect('/active/home')
    context = {
        'logged_user': User.objects.get(id=request.session['logged_user']),
        'other_activities': Activity.objects.exclude(user=request.session['logged_user'])


    }
    return render(request, 'Dash/dashboard.html', context)

def maps_sm(request):
    return render(request, "Dash/mapsSm.html")
def location(request):
    if 'logged_user' not in request.session:
        messages.error(request, "Please register or log in first!")
        return redirect('/active/home')

    context={
        'locations': Location.objects.all()


    }
    return render(request, "Dash/location.html", context)

def showlocation(request, location_id):
 
    context = {
        'this_location': Location.objects.get(id=location_id)

    }
    return render(request, 'Dash/locationinfo.html', context)

def locationform(request):
    if 'logged_user' not in request.session:
        messages.error(request, "Please register or log in first!")
        return redirect('/active/home')
        
    return render(request, 'Dash/locationform.html')
def newlocation(request):
    if request.method =="POST":
        errors = Location.objects.location_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/active/location/form')
        new_location = Location.objects.create(
            name=request.POST['name'],
            address=request.POST['address'],
            zip_code=request.POST['zip_code']

        )
        return redirect('/active/location')

def deletelocation(request, location_id):
    if 'logged_user' not in request.session:
        messages.error(request, "Please register or log in first!")
        return redirect('/active/home')

    location_delete = Location.objects.get(id=location_id)
    location_delete.delete()
    return redirect('/active/location')


def login(request):
    if 'logged_user' in request.session:
        return redirect('/active/dashboard')

    return render(request, "Dash/reglogin.html")

def create(request):

    if request.method == "POST":

        errors = User.objects.registration_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/active/login')

        hash_pw = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()).decode()

        new_user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=hash_pw
        )
        request.session['logged_user'] = new_user.id

        return redirect('/active/dashboard')
    return redirect("/active/login")

def loginuser(request):
    if request.method == "POST":
        user = User.objects.filter(email=request.POST['email'])

        if user:
            log_user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):
                request.session['logged_user'] = log_user.id
                return redirect('/active/dashboard')
        messages.error(request, "Email or password are invalid.")
    return redirect("/active/login")

def logout(request):
    request.session.flush()
    return redirect('/active/login')

def activityform(request):
    if 'logged_user' not in request.session:
        messages.error(request, "Please register or log in first!")
        return redirect('/active/home')

    context = {
        'locations': Location.objects.all()
    }
    return render(request, 'Dash/activityform.html', context)

def newactivity(request):
    if request.method =="POST":
        errors = Activity.objects.activity_validator(request.POST)

        if request.POST['activity_dropdown'] == "-1":
            messages.error(request, "Please either choose a location from the dropdown or add a new location")
        if len(errors) > 0:
            for key, value in errors.items():
                    messages.error(request, value)
            return redirect('/active/activity/form')
        else: 
            curr_location = Location.objects.get(id = request.POST['activity_dropdown'])


        current_user = User.objects.get(id = request.session['logged_user'])
        newAct = Activity.objects.create(
            name = request.POST['name'],
            activity_date = request.POST['activity_date'],
            desc = request.POST['desc'],
            activityType = request.POST['activityType'],
            user = current_user,
            location = curr_location


        )
        return redirect('/active/dashboard')

def deleteactivity(request, activity_id):
    if 'logged_user' not in request.session:
        messages.error(request, "Please register or log in first!")
        return redirect('/active/home')
    activity_delete = Activity.objects.get(id=activity_id)
    activity_delete.delete()
    return redirect('/active/dashboard')

def activity(request):
    if 'logged_user' not in request.session:
        messages.error(request, "Please register or log in first!")
        return redirect('/active/home')
    context={
        'all_activities' : Activity.objects.all(),
        'logged_user': User.objects.get(id=request.session['logged_user']),
        'other_activities': Activity.objects.exclude(user=request.session['logged_user'])

    }
    return render(request, "Dash/activity.html", context)

def joinactivity(request, activity_id):
    user = User.objects.get(id=request.session['logged_user'])
    this_activity = Activity.objects.get(id=activity_id)
    user.joined_activity.add(this_activity)
    return redirect('/active/dashboard')

def cancelactivity(request, activity_id):
    user = User.objects.get(id=request.session['logged_user'])
    this_activity = Activity.objects.get(id=activity_id)
    user.joined_activity.remove(this_activity)
    return redirect('/active/dashboard')

def editform(request, activity_id):

    context = {
        'this_activity' : Activity.objects.get(id=activity_id),
        'locations': Location.objects.all()

    }
    return render(request, 'Dash/activityedit.html', context)

def updateactivity(request, activity_id):

    if request.method =="POST":
        errors = Activity.objects.activity_validator(request.POST)

        if request.POST['activity_dropdown'] == "-1":
            messages.error(request, "Please either choose a location from the dropdown or add a new location")
        if len(errors) > 0:
            for key, value in errors.items():
                    messages.error(request, value)
            return redirect(f'/active/{activity_id}/edit')
        else: 
            curr_location = Location.objects.get(id = request.POST['activity_dropdown'])
        current_activity = Activity.objects.get(id=activity_id)
        current_activity.name = request.POST['name']
        current_activity.activity_date = request.POST['activity_date']
        current_activity.desc = request.POST['desc']
        current_activity.activityType = request.POST['activityType']
        current_activity.location = curr_location
        current_activity.save()

        return redirect('/active/dashboard')

def search_activity(request):
    if 'logged_user' not in request.session:
        messages.error(request, "Please register or log in first!")
        return redirect('/active/home')
    if request.method =="POST":
        result = request.POST['result']
        activities = Activity.objects.filter(name__contains=result)
        locations = Location.objects.filter(name__contains=result)

        return render(request, 'Dash/searchActivity.html',{'result': result, 'activities':activities, 'locations':locations})
    else:
        return render(request, 'Dash/searchActivity.html')

def activity_info(request, activity_id):
 
    context = {
        'this_activity': Activity.objects.get(id=activity_id)

    }
    return render(request, 'Dash/activityinfo.html', context)











