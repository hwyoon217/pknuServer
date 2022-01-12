from django.core.paginator import Paginator   # 화면에 페이지네이터 출력
from django.shortcuts import render, get_object_or_404, redirect

from ..models import Question, Answer
from django.db.models import Q, Count




# Create your views here.
def index(request):
    """
    질문 목록 출력
    """
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    so = request.GET.get('so', 'recent')

    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter','-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer','-create_date')
    else:
        question_list = Question.objects.order_by('-create_date')          # - 붙이면 내림차순 변경



    if kw:

        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(author__username__icontains=kw) |  # 질문 작성자 검색
            Q(answer__author__username__icontains=kw)   # 답변 작성자 검색
        ).distinct()


    # 페이징 처리
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {'question_list' : page_obj, 'page':page, 'kw':kw, 'so':so}  # 딕셔너리 형태 (key : value)
    return render(request, 'pybo/question_list.html',context)

def detail(request, question_id):
    """
    질문 내용 출력
    """
    question = get_object_or_404(Question, pk = question_id)  # - 붙이면 내림차순 변경
    context = {'question': question}  # 딕셔너리 형태 (key : value)
    return render(request, 'pybo/question_detail.html', context)    #화면보여주는것
