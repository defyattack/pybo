from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import CommentForm
from ..models import Question, Answer, Comment


@login_required(login_url='common:login')
def comment_create_que(request, question_id):
    """
    pybo 질문에 대한 댓글 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user #현재 로그인 User 모델의 객체
            comment.create_date = timezone.now()
            comment.question = question
            comment.save()
            #return redirect('pybo:detail', question_id=question.id)
            return redirect('{}#comment_{}'.format(resolve_url('pybo:detail', question_id=comment.question.id), comment.id))
    else:
        form = CommentForm()

    context = {'question_id':question.id, 'form':form}
    return render(request,'pybo/comment_form.html', context)

@login_required(login_url='common:login')
def comment_modify_que(request, comment_id):
    """
    pybo 질문에 대한 댓글 수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id=comment.question.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            #return redirect('pybo:detail',question_id=comment.question.id)
            return redirect('{}#comment_{}'.format(resolve_url('pybo:detail', question_id=comment.question.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'question_id':comment.question.id, 'form':form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete_que(request, comment_id):
    """
    pybo 질문에 대한 댓글 삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '삭제권한이 없습니다.')
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.question.id)

"""
pybo 답변에 대한 댓글 부분
"""

@login_required(login_url='common:login')
def comment_create_ans(request, answer_id):
    """
    pybo 답변에 대한 댓글 등록
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user #현재 로그인 User 모델의 객체
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.save()
            #return redirect('pybo:detail', question_id=comment.answer.question.id)
            return redirect('{}#comment_{}'.format(resolve_url('pybo:detail', question_id=comment.answer.question.id), comment.id))
    else:
        form = CommentForm()

    context = {'question_id':answer.question.id, 'form':form}
    return render(request,'pybo/comment_form.html', context)

@login_required(login_url='common:login')
def comment_modify_ans(request, comment_id):
    """
    pybo 답변에 대한 댓글 수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id=comment.answer.question.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            #return redirect('pybo:detail',question_id=comment.answer.question.id)
            return redirect('{}#comment_{}'.format(resolve_url('pybo:detail', question_id=comment.answer.question.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'question_id':comment.answer.question.id, 'form':form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete_ans(request, comment_id):
    """
    pybo 답변에 대한 댓글 삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '삭제권한이 없습니다.')
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.answer.question.id)