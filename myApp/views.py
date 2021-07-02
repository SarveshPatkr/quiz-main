import json
from django.shortcuts import redirect, render
from django.views.generic.base import RedirectView
from .models import*
from django.http import JsonResponse
from rest_framework.decorators import api_view


@api_view(['POST'])
def create_quiz(request):
    print("inside")
    result = {'message' : 'something went wrong' , 'status' : False}
    category_obj = list(CategoryModel.objects.all())
    random.shuffle(category_obj)
    categories_list = []
    for cat in category_obj:
        categories_list.append({
            'id' : cat.id,
            'category' : cat.category,
        })
    try:
        data = request.data
        print(data)
        name = data.get('name')
        category = data.get('cat_id')

        if category is None or name is None:
            result['message'] = 'category and user_name is required'
            raise Exception('category and user_name is required')

        user, _ = UserModel.objects.get_or_create(user=name)
        try:
            category_obj = CategoryModel.objects.get(id = category)
        except Exception as e:
            result['message'] = 'invalid category id'
            raise Exception('invalid category id')

        create_quiz,_ = CreateQuizModel.objects.get_or_create(user=user,category=category_obj)

        result['message'] = 'Your quiz is created'
        result['data'] = {'quiz_id' : create_quiz.id , 'category' : category_obj.category }
        result['status'] = True

    except Exception as e:
        print(e)

    # return JsonResponse({'result':result} , status=  200, safe = False)
    a = result['data'].get('quiz_id')
    print(a)
    a = str(a)
    red = "/set-quiz/" + a
    return redirect(red)


@api_view(['GET'])
def  home(request):
    data = {
        "categories": [
            {
                "id": "23790389-4fb4-4e83-9bfc-57b4c5c5f31c",
                "category": "Education"
            },
            {
                "id": "f193cd5f-9420-421c-96f3-a5dc8ca3882c",
                "category": "Friendship"
            }
        ]
    }
    js_data = json.dumps(data)
    return render(request, 'myApp/CreateQuiz.html', {"data": js_data} ,status=  200)

@api_view(['GET'])
def set_quiz(request,quiz_id):
    return render(request, quiz_id,'myApp/CreateQuiz.html')


@api_view(['POST'])
def set_quiz(request, quiz_id):
    result = {'message' : 'something went wrong' , 'status' : False}
    quiz_obj = CreateQuizModel.objects.get(id=quiz_id)
    question_obj = list(QuestionModel.objects.filter(category=quiz_obj.category.id))
    random.shuffle(question_obj)
    questionsanswers = []
    for quest in question_obj:
        questionsanswers.append({
            'id' : quest.id,
            'question' : quest.question,
            'options' : quest.get_answers()
        })
    try:
        data = request.data

        quest_id = data.get('quest_id')
        ans_id = data.get('ans_id')

        if quest_id is None or ans_id is None:
            result['message'] = 'quest_id and ans_id is required'
            raise Exception('quest_id and ans_id is required')

        try:
            question = QuestionModel.objects.get(id = quest_id)
            answer = AnswerModel.objects.get(id = ans_id)
        except Exception as e:
            print(e)
            result['message'] = 'invalid question id or answer id'

        setquiz_obj = SetQuizModel.objects.create(
            quiz = quiz_obj,
            questions =  question,
            correct_answers = answer
        )

        result['message'] = 'Quiz Set'
        result['data'] = {'questions' : setquiz_obj.questions.question , 'correct_answers' : setquiz_obj.correct_answers.answer }
        result['status'] = True

    except Exception as e:
        print(e)

    return JsonResponse({'status' : 200 , 'questions' : questionsanswers, 'result':result} , safe = False)


def share_quiz(request,quiz_id):
    return render(request, 'myApp/ShareQuiz.html', {"quiz_id":quiz_id})


@api_view(['POST'])
def quiz(request, quiz_id):
    result = {'message' : 'something went wrong' , 'status' : False}
    quiz_obj = CreateQuizModel.objects.get(id = quiz_id)

    question_obj = list(QuestionModel.objects.filter(category=quiz_obj.category.id))
    random.shuffle(question_obj)
    questionsanswers = []
    for quest in question_obj:
        questionsanswers.append({
            'id' : quest.id,
            'question' : quest.question,
            'options' : quest.get_answers()
        })

    try:
        data = request.data
        name = data.get('name')
        quiz_player, _ = UserModel.objects.get_or_create(user=name)
        
        quest_id = data.get('quest_id')
        ans_id = data.get('ans_id')
        
        ShareQuizModel.objects.get_or_create(
            user = quiz_player,
            quiz = quiz_obj,
            questions = QuestionModel.objects.get(id=quest_id),
            selected_answers = AnswerModel.objects.get(id=ans_id)
        )
        score_obj, _ = ScoreModel.objects.get_or_create(user=quiz_player, quiz=quiz_obj)

        original_quiz = SetQuizModel.objects.filter(quiz=quiz_obj, questions=QuestionModel.objects.get(id=quest_id)).first()
        shared_quiz = ShareQuizModel.objects.filter(user=quiz_player, quiz=quiz_obj, questions=QuestionModel.objects.get(id=quest_id)).first()
        
        if original_quiz.correct_answers == shared_quiz.selected_answers :
            score_obj.score += 1
        else:
            pass
        
        result['message'] = 'Quiz Answered'
        result['data'] = {'shared_QuizID' : shared_quiz.id, 'score' : score_obj.score }
        result['status'] = True

    except Exception as e:
        print(e)

    return JsonResponse({'status' : 200, 'result':result, 'questions' : questionsanswers} , safe = False)
