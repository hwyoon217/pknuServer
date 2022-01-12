from django.contrib import messages
from django.contrib.auth.decorators import login_required  # 로그인페이지로 이동하도록 유도
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone  # 답변등록 시간 때문에 사용

from ..forms import AnswerForm
from ..models import Question, Answer


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
