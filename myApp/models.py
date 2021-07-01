from django.db import models
import uuid, random

from django.db.models import base

class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class CategoryModel(BaseModel):
    category = models.CharField(max_length=50)
    def __str__(self):
        return self.category

class UserModel(BaseModel):
    user = models.CharField(max_length=50)
    def __str__(self):
        return self.user

class QuestionModel(BaseModel):
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    def get_answers(self):
        answers = list(AnswerModel.objects.filter(question = self))
        random.shuffle(answers)
        ans_list = []
        for ans in answers:
            ans_list.append({
                "id" : ans.id,
                "option" : ans.answer
            })
        return ans_list

class AnswerModel(BaseModel):
    question = models.ForeignKey(QuestionModel , on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)

class CreateQuizModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)

class SetQuizModel(BaseModel):
    quiz = models.ForeignKey(CreateQuizModel, on_delete=models.CASCADE)
    questions = models.ForeignKey(QuestionModel, on_delete=models.CASCADE)
    correct_answers = models.ForeignKey(AnswerModel, on_delete=models.CASCADE)

class ShareQuizModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    quiz = models.ForeignKey(CreateQuizModel, on_delete=models.CASCADE)
    questions = models.ForeignKey(QuestionModel, on_delete=models.CASCADE)
    selected_answers = models.ForeignKey(AnswerModel, on_delete=models.CASCADE)

class ScoreModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    quiz = models.ForeignKey(CreateQuizModel, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
