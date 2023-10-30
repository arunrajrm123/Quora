from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import re
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
@never_cache
def register_user(request):
    if 'email' in request.session:
        return render(request, 'home.html')
    if request.method == 'POST':  
        name = request.POST.get('name')
        email=request.POST.get("email")
        password = request.POST.get('password')
        print(name,email,password)
        user = Uuser.objects.filter(name=name, password=password,email=email).first()
        print(user)
        if user:
            request.session['email']=email
            return redirect(home)
        else:
            print(password,name,email)
            error = {}
            us=Uuser.objects.all()
            user=None
            l=[em.email for em in us]
            if not name:
                error["name"] = 'Name is required'
            if len(name) < 4:
                    error["name"] = 'Name must be longer than 4 characters'
            if not re.match(r'^[\w-]+(\.[\w-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*(\.[a-zA-Z]{2,})$', email):
                error['email'] = 'Enter a valid email address'
            if email in l:
                error['email'] = 'Email already exists'
            if len(password) < 4:
                error["password"] = 'Password should contain at least 4 characters or numbers'
            if not error:
                
                    user = Uuser.objects.create(name=name, password=password,email=email)
                    request.session['email']=email
                    return redirect("home")  
            else:
                return render(request,'register.html',{'error':error,"user":user}) 
    return render(request, 'register.html')

def post_question(request):
    if request.method == 'POST':
        email = request.session.get('email')
        text = request.POST.get('text')
        question = Question.objects.create(text=text, user=Uuser.objects.get(email=email))
        return redirect('home')
    all_questions = Question.objects.all()
    return render(request, 'Question.html', {'qu': all_questions})

@never_cache
def home(request):
    if "email" in request.session:
        print("enterd")
        questions = Question.objects.all()
        question_answers = []  # Create an empty list to store answers for each question

        for question in questions:
            answers = Answer.objects.filter(question=question)
            question_answers.append((question, answers))  # Append the question and its answers to the list
        return render(request, 'home.html', {'question_answers': question_answers})
    else:
        return render(request, 'register.html')



def answer_question(request, id):
    question = Question.objects.get(pk=id)
    if request.method == 'POST':
        text = request.POST.get('text')
        email = request.session.get('email')
        print(text,email)
        Answer.objects.create(text=text, question=question, user=Uuser.objects.get(email=email))
        return redirect('home')
    return render(request, 'Answer.html', {'id': question.id})



def like_answer(request, answer_id):
    answer = Answer.objects.get(pk=answer_id)
    email = request.session.get('email')
    user = Uuser.objects.get(email=email)

    try:
        # Check if the user has already liked this answer
        like = Like.objects.get(answer=answer, user=user)
        # If the like exists, delete it (unlike)
        like.delete()
    except Like.DoesNotExist:
        # If the like does not exist, create it (like)
        Like.objects.create(answer=answer, user=user)

    # Calculate the total likes for the answer
    total_likes = answer.like_set.count()

    # Return the total likes as a JSON response
    return JsonResponse({'likes': total_likes})


@never_cache
def logout(request):
    if "email" in request.session:
      request.session.flush()     
      return redirect(register_user)
    else:
      return redirect(register_user)
    