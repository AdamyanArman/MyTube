from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Account
from django.contrib.auth import login as auth_login, logout as auth_logout


# Create your views here.
def home(request):
    user_id=request.session.get('user_id')

    if user_id:
        return render(request, 'profile.html')

    return render(request, 'base.html')



def register(request):
    if request.method=='POST':
        phone=request.POST.get('phone')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')

        if phone is None or password1 is None or password2 is None:
            return JsonResponse({'message': 'Phone and password is required!'}, status=400)

        if password1!=password2: return JsonResponse({'message': 'Password is different!'}, status=400)

        if Account.objects.filter(phone=phone).exists():
            return JsonResponse({'message': 'Phone is already registered!'}, status=400)


        user=Account(phone=phone)
        user.set_password(password1)

        user.save()
        request.session['user_id']=user.id

        return render(request, 'profile.html')

    return render(request, 'register.html')



def login(request):
    if request.method=='POST':
        phone=request.POST.get('phone')
        password=request.POST.get('password')

        if phone is None or password is None:
            return JsonResponse({'message': 'Phone and password is required!'}, status=400)

        user=Account.objects.get(phone=phone)

        if user.check_password(password):
            request.session['user_id']=user.id
            return render(request, 'profile.html')



    return render(request, 'login.html')




def logout(request):
    request.session.flush()
    return redirect('login')