from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer
from django.utils import timezone   # 답변등록 시간 때문에 사용
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator   # 화면에 페이지네이터 출력
from django.contrib.auth.decorators import login_required   # 로그인페이지로 이동하도록 유도
from django.contrib import messages


#from django.http import HttpResponse


# Create your views here.
def index(request):
    """
    질문 목록 출력
    """
    page = request.GET.get('page', '1')

    question_list = Question.objects.order_by('-create_date') # - 붙이면 내림차순 변경

    # 페이징 처리
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {'question_list' : page_obj}  # 딕셔너리 형태 (key : value)
    return render(request, 'pybo/question_list.html',context)

def detail(request, question_id):
    """
    질문 내용 출력
    """
    question = get_object_or_404(Question, pk = question_id)  # - 붙이면 내림차순 변경
    context = {'question': question}  # 딕셔너리 형태 (key : value)
    return render(request, 'pybo/question_detail.html', context)    #화면보여주는것


@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    답변 등록
    """
    question = get_object_or_404(Question, pk = question_id)  # - 붙이면 내림차순 변경

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit = False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id = question.id)   # 호출
    else:
        form = AnswerForm()     # 객체 생성 >> 다른 언어는 new 필수

    context = {'question' : question, 'form' : form}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def question_create(request):
    """
    pybo 질문 등록
    """
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit = False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()     # 객체 생성 >> 다른 언어는 new 필수

    context = {'form':form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')   # 로그인해야 수정가능하므로
def question_modify(request, question_id):
    """
    질문 수정
    """
    question = get_object_or_404(Question, pk = question_id)
    if request.user != question.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id = question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit = False)
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id = question.id)   # 호출
    else:
        form = QuestionForm(instance=question)

    context = {'form' : form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')   # 로그인해야 삭제가능하므로
def question_delete(request, question_id):
    """
    질문 삭제
    """
    question = get_object_or_404(Question, pk = question_id)
    if request.user != question.author:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('pybo:detail', question_id = question.id)
    question.delete()
    return redirect('pybo:index')



@login_required(login_url='common:login')   # 로그인해야 수정가능하므로
def answer_modify(request, answer_id):
    """
    답변 수정
    """
    answer = get_object_or_404(Answer, pk = answer_id)
    if request.user != answer.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id = answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit = False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pybo:detail', question_id = answer.question.id)   # 호출
    else:
        form = AnswerForm(instance=answer)

    context = {'answer' : answer, 'form' : form}
    return render(request, 'pybo/answer_form.html', context)


@login_required(login_url='common:login')   # 로그인해야 수정가능하므로
def answer_delete(request, answer_id):
    """
    답변 삭제
    """
    answer = get_object_or_404(Answer, pk = answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제 권한이 없습니다.')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id = answer.question.id)

