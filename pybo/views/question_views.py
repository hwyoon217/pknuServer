from django.contrib import messages
from django.contrib.auth.decorators import login_required  # 로그인페이지로 이동하도록 유도
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone  # 답변등록 시간 때문에 사용

from ..forms import QuestionForm
from ..models import Question


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