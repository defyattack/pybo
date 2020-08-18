from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from ..models import Category,Question,Answer,Comment

import logging
logger = logging.getLogger('pybo')

def index(request):
    """
    pybo 질문 목록 출력
    """

    logger.info("INFO 레벨로 출력")

    #최근 답변 5개
    new_answer = Answer.objects.order_by('id')[:5]

    #최근 댓글 5개
    new_comment = Comment.objects.order_by('id')[:5]

    page = request.GET.get('page','1')
    kw = request.GET.get('kw','')
    so = request.GET.get('so', 'recent')
    ca = request.GET.get('ca', '')

    categorys = Category.objects.order_by('-id')

    if not ca:
        question_list = Question.objects.select_related('cate').filter(cate_id=1)
        ca = 1
    elif ca == 'all':
        question_list = Question.objects.select_related('cate')
    else:
        question_list =  Question.objects.select_related('cate').filter(cate_id=ca)

    if so == 'recommend':
        question_list = question_list.annotate(num_voter=Count('voter')).order_by('-num_voter','-id')
    elif so == 'popular':
        question_list = question_list.annotate(num_answer=Count('answer')).order_by('-num_answer','-id')
    else: #recent
        question_list = question_list.order_by('-id')

    if kw: #검색키워드
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()

    import math

    paginator = Paginator(question_list,10)
    page_obj = paginator.get_page(page)
    page_obj.e_number = math.ceil(page_obj.paginator.count / page_obj.paginator.per_page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so, 'ca':ca, 'cate_list':categorys,'new_answer':new_answer,'new_comment':new_comment}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    """
    pybo 질문 내용출력
    """
    page = request.GET.get('page', '1')
    so = request.GET.get('so', 'recent')

    question = get_object_or_404(Question, pk=question_id)

    # 조회수 증가
    view_cnt = 'view_count(%d)'%question.id
    if view_cnt not in request.session._session:
        request.session[view_cnt] = True
        question.cnt = question.cnt + 1
        question.save()

    if so == 'recommend':
        answer = Answer.objects.filter(question_id=question_id).annotate(num_voter=Count('voter')).order_by('-num_voter','-id')
    else: #recent
        answer = Answer.objects.filter(question_id=question_id).order_by('-id')

    import math

    paginator = Paginator(answer,3)
    page_obj = paginator.get_page(page)
    page_obj.e_number = math.ceil(page_obj.paginator.count / page_obj.paginator.per_page)

    context = {'question': question,'answer_list': page_obj, 'page': page, 'so': so}
    return render(request, 'pybo/question_detail.html', context)