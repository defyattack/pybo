from django.contrib.auth import authenticate, login, logout, forms, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from common.forms import UserForm,UserUpdateForm,UserBasicForm
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from common.comm_mod import pass_rand,page_navi
from django.core.mail import EmailMessage

from pybo.models import Category,Question,Answer,Comment

def signup(request):
    """
    계정생성
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request,user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form':form})

@login_required
def user_mod(request):
    """
    계정수정
    """
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save(commit=False)
            """
            비밀번호 체크하기
            """
            username = form.cleaned_data.get('username')
            raw_password = request.POST.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                form.save()
                messages.info(request, '이메일이 수정 되었습니다.')
            else:
                #return HttpResponse("비밀번호가 틀렸습니다.")
                messages.error(request, '비밀번호가 틀렸습니다.')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'common/user_mod.html', {'form':form})


@login_required
def pass_mod_p(request):
    """
    비밀번호 수정 처리
    """
    if request.method == "POST":
        form = forms.PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # 수정후 자동 로그인
            messages.success(request, '비밀번호가 변경 되어 다시 로그인 했습니다.')
            return redirect('common:pass_mod_p')
        else:
            messages.error(request,"비밀번호 수정 에러!")
    else:
        form = forms.PasswordChangeForm(request.user)
    return render(request, 'common/pass_mod_p.html', {'form': form})


def pass_mod_req(request):
    """
    비밀번호 분실 요청
    """
    if request.method == "POST":
        form = UserBasicForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            member = User.objects.filter(Q(username=username),Q(email=email))
            if member:
                new_pass = pass_rand(8)
                member[0].set_password(new_pass) # 암호화
                member[0].save()

                subj = "안녕하세요. 파이보 입니다. "+username+" 회원님께서 요청하신 내용 입니다."
                cont = "요청하신 임시 비밀번호는 "+new_pass+" 입니다. 로그인 후에 꼭 변경해 주세요."
                smail = EmailMessage(
                    subj,
                    cont,
                    to=[email]
                )
                succ = smail.send()
                # 발송 에러남 : 구글 gmail stmp 이용 발송시 보안수준이 낮은 앱의 엑세스 허용 해야 함. https://myaccount.google.com/lesssecureapps

                if succ:
                    messages.info(request, '임시 비밀번호 정보를 가입하신 이메일주소로 발송 했습니다.')
                else:
                    messages.info(request, member[0].password+"  ,  "+new_pass)

                # 랜덤한 비밀번호 생성 (8자리 문자열), db 저장 , 이메일 발송 -> 결과 리턴 후 발송완료 메세지
                # messages.info(request, '가입하신 이메일을 발송 했습니다.')
            else:
                messages.error(request, '일치하는 사용자가 없습니다. 다시 확인해 주세요.')
            form = UserBasicForm()
    else:
        form = UserBasicForm()
    return render(request, 'common/pass_mod_req.html', {'form':form})

@login_required
def user_info(request):
    """
    사용자 정보
    """
    qpage = request.GET.get('qpage','1')
    apage = request.GET.get('apage','1')
    cpage = request.GET.get('cpage','1')

    #member = User.objects.filter(Q(username=request.user))
    member = User.objects.get(username=request.user)

    question_list = Question.objects.filter(author_id=request.user).order_by('-id')
    answer_list = Answer.objects.filter(author_id=request.user).order_by('-id')
    comment_list = Comment.objects.filter(author_id=request.user).order_by('-id')

    page_obj1 = page_navi(question_list, qpage, 2)
    page_obj2 = page_navi(answer_list, apage, 5)
    page_obj3 = page_navi(comment_list, cpage, 5)
    
    context = {'member':member,'question_list': page_obj1, 'answer_list': page_obj2, 'comment_list': page_obj3,
               'qpage': qpage, 'apage': apage, 'cpage': cpage}

    return render(request, 'common/user_info.html', context)

def page_not_found(request, exception):
    """
    404 Page not found
    """
    return render(request, 'common/404.html', {})