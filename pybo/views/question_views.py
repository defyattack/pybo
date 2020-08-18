from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question,Category

@login_required(login_url='common:login')
def question_create(request):
    """
    pybo 질문 등록
    """
    categorys = Category.objects.order_by('-id')

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user  # 현재 로그인 User 모델의 객체
            question.create_date = timezone.now()
            question.save()
            #return redirect('pybo:index')
            return redirect('{}?ca={}'.format(resolve_url('pybo:index'),question.cate_id))
    else:
        form = QuestionForm()
    context = {'form':form, 'cate_list':categorys}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    pybo 질문 수정
    """
    categorys = Category.objects.order_by('-id')
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail',question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form':form, 'cate_list':categorys}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    pybo 질문 삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')
