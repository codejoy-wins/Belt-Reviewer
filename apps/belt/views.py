from django.shortcuts import render, redirect
from django.contrib import messages
import re
import bcrypt
from models import *

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

#request.session = {}
#request.session['bro'] = 'Hairif'
#request.session = {
#     'bro'  :  'Hairif'
# }

def index (request):
    return render(request, 'belt/index.html')

def register(request):
    #validations
    error = False
    if len(request.POST['name']) < 2:
        messages.error(request, "first name must be 2 or more characters")
        error = True
    if not EMAIL_REGEX.match(request.POST['email']):
        messages.error(request, "email is invalid")        
        error = True
    if request.POST['password'] != request.POST['c_password']:
        messages.error(request, "passwords do not match")        
        error = True
    if len(User.objects.filter(email = request.POST['email'])) > 0:
        messages.error(request, "Email Taken")
    if error:
        return redirect ('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        the_user = User.objects.create(name = request.POST['name'], alias = request.POST['alias'], email = request.POST['email'], password = hashed_pw)
        # request.session['user_id'] = the_user.id
        return redirect ('/')

def login(request):

    try:
        the_user = User.objects.get(email = request.POST['email'])
    except:
        messages.error(request, "Email or password invalid")
        return redirect ('/')

    if bcrypt.checkpw(request.POST['password'].encode(), the_user.password.encode()):
        request.session['user_id'] = the_user.id
        print "logging in"
        return redirect('/main')
    else:
        messages.error(request,"Email or password invalid")
    return redirect ('/')

def main(request):
    if not 'user_id' in request.session:
        messages.error(request, "must be logged on, dog")
        return redirect('/')
    context = {
        'user' : User.objects.get(id = request.session['user_id']),
        'books' : Book.objects.all(),
        'booksy' : Book.objects.all()[2:]      
    }
    return render (request, 'belt/main.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def add(request):
    return render(request,'belt/add.html')

def create(request):
    Book.objects.create(title = request.POST['title'], author = request.POST['author'], review = request.POST['review'], rating = request.POST['rating'], uploader = User.objects.get(id = request.session['user_id']))
    return redirect('/main')
    # user  = User.objects.get(id = request.session['user_id'])
    # x = user.name
    # print x
    # print "Created Book"
    # Book.objects.create(title = "Steven" author = "Steven Sedul", review = "ha", rating = "4", uploader = "Steven")
    # the_book = Book.objects.create(title = request.POST['title'], author = request.POST['author'], review = request.POST['review'], rating = request.POST['rating'], uploader = User.objects.get(id = request.session['user_id']))
    # Book.objects.create(title = request.POST['title'], author = request.POST['author'], review = request.POST['review'], rating = request.POST['rating'], uploader = user)
    # Book.objects.create(title = request.POST['title'], author = request.POST['author'], review = request.POST['review'], rating = request.POST['rating'] uploader = x)
    return redirect('/main')


def odell (request):
    return render(request, 'belt/odell.html')

# alt method for try
    # the_user_list = User.objects.filter(email = request.POST['email'])
    # if len(the_user_list) > 0:
    #     the_user = the_user_list[0]
    #     print the_user
    # else:
    #     messages.error(request, "Email or password invalid")
    #     return redirect ('/')