from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import User
from django.contrib import auth
from django.utils import timezone
from django.contrib.auth import get_user_model

# SMTP 관련 인증
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from .token import users_activation_token


#messages 출력하기위해
from django.contrib import messages
from tkinter import Button, messagebox


# 홈 #

def home(request):
    return HttpResponse('<u>Home</u>')



def back(request):
    return HttpResponse('<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><font size ="10"><p><hi><center><b><u>아래 사이트를 클릭 후 재로그인해주세요.</u><br> -Petdada- <br> <font size ="15"><a href="/member/login/">LOGIN</a>')   

#회원가입#

def signup(request):
    if request.method=="POST":
        if User.objects.filter(username=request.POST['username']).exists(): #아이디 중복 체크
             return render(request, 'member/signup_error.html')
        if request.POST['password1'] ==request.POST['password']:   
            print(request.POST)
            username=request.POST["username"] #아이디
            first_name=request.POST["first_name"] #이름
            password=request.POST["password"] #비밀번호
            email=request.POST["email"] #이메일
    
            users_user=User.objects.create_user(username,email,password) 
            users_user.first_name=first_name
            users_user.is_active = True
            users_user.save()
            current_site = get_current_site(request) 
            message = render_to_string('activation.html', {
                'user': users_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(users_user.pk)),
                'token': users_activation_token.make_token(users_user),
            })
            mail_title = "계정 본인확인 이메일"
            mail_to = request.POST["email"]
            email = EmailMessage(mail_title, message, to=[mail_to])
            email.send()
            return render(request,"signup2.html")
        else:
            return render(request,"signup3.html")  
    
    return render(request,"signup.html")

# 이메일 인증 ( 계정 활성화 )
def activate(request, uid64, token ,*args, **kwargs):
    try:
        uid = force_text(urlsafe_base64_decode(uid64))
        users_user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExsit):
        users_user = None
    if users_user is not None and users_activation_token.check_token(users_user, token):
        users_user.is_active = True
        users_user.save()
        auth.login(request, users_user)
        return redirect("/users/login")
    else:
        return render(request, 'home.html', {'error' : '계정 활성화 오류'})
    return 



# 로그인 #

def login(request):
    # 포스트 
    if request.method == 'POST':
        # 정보 가져와서 
        username = request.POST['username']
        password = request.POST['password']
        
        
        # 로그인
        user = auth.authenticate(request, username=username, password=password)
        print(user)

        # 성공
        if user is not None:
            auth.login(request, user)
            request.session['id'] = user.id
            return redirect('/users/home/')
        # 실패
        else:
            return render(request, 'back.html')
            #return render(request, 'member/error.html',  {'error': 'username or password is incorrect.'}))
    else:
        return render(request, 'login.html')


