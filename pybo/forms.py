from django import forms
from pybo.models import Question, Answer

class QuestionForm(forms.ModelForm):  # UI 나오게 하려고
    class Meta:
        model = Question
        fields = ['subject', 'content']

        labels = {
            'subject' : '제목',
            'content' : '내용',
        }



class AnswerForm(forms.ModelForm):  # UI 나오게 하려고
    class Meta:
        model = Answer
        fields = ['content']

        labels = {
            'content' : '답변 내용',
        }