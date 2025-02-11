import uuid
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AptitudeQuestionForm, AptitudeCategoryForm, get_choice_formset
from .models import AptitudeCategory, AptitudeQuestions, Choice, AptitudeResponse
from home.models import TestTaker


# Create your views here.
@login_required
def dashboard(request):
    # Use select_related for efficiency
    # questions = AptitudeQuestions.objects.select_related('category').all()
    questions = AptitudeQuestions.objects.all()
    print(questions)
    context = {
        'questions': questions
    }
    return render(request, 'aptitude_dashboard.html', context)

@login_required
def add_aptitude_questions(request):
    ChoiceFormSet = get_choice_formset(extra=4)  # Always 4 choices for new questions
    if request.method == 'POST':
        question_form = AptitudeQuestionForm(request.POST)
        choice_formset = ChoiceFormSet(request.POST)

        if question_form.is_valid() and choice_formset.is_valid():
            # Save Question first
            question = question_form.save()

            # Get choices but don't save them yet
            if choice_formset.is_valid():
                choices = choice_formset.save(commit=False)

                # Associate each choice with the question and save
                for choice in choices:
                    if choice.text:  # Only save non-empty choices
                        choice.question = question
                        choice.save()

            return redirect('aptitude_dashboard')  # Redirect to dashboard after saving

        else:
            print('DEBUG: Question Form Error:', question_form.errors)
            print('DEBUG: Choice Form Set Error:', choice_formset.errors)

    else:
        question_form = AptitudeQuestionForm()
        choice_formset = ChoiceFormSet()

    return render(request, 'add_aptitude_questions.html', {
        'question_form': question_form,
        'choice_formset': choice_formset
    })

@login_required
def add_aptitude_category(request):
    if request.POST:
        category = AptitudeCategoryForm(request.POST)
        if category.is_valid():
            category.save()
            return redirect('aptitude_dashboard')
    form = AptitudeCategoryForm()
    Categories = AptitudeCategory.objects.all().values()
    context = {
        'form': form,
        'Categories': Categories
    }
    return render(request, 'add_aptitude_category.html', context)

@login_required
def edit_aptitude(request, id):
    ChoiceFormSet = get_choice_formset(extra=0)  # No extra fields when editing
    question = get_object_or_404(AptitudeQuestions, id=id)  # Fetch the question object

    if request.method == 'POST':
        question_form = AptitudeQuestionForm(request.POST, instance=question)
        choice_formset = ChoiceFormSet(request.POST, instance=question)  # Link choices to the question

        if question_form.is_valid() and choice_formset.is_valid():
            question = question_form.save()  # Save the question

            # Save choices
            choices = choice_formset.save(commit=False)

            # Reset existing correct choices
            question.choices.update(is_correct=False)

            for choice in choices:
                if choice.text:  # Only process non-empty choices
                    choice.question = question
                    choice.save()

            # Set the correct choice based on the is_correct field in the form
            for choice in choices:
                if choice.is_correct:
                    break

            return redirect('aptitude_dashboard')  # Redirect after saving
        else:
            print(f'Question Valid: {question_form.is_valid()} ; Choice Valid: {choice_formset.is_valid()}')
            print(question_form.errors)
            print(choice_formset.errors)

    else:
        question_form = AptitudeQuestionForm(instance=question)
        choice_formset = ChoiceFormSet(instance=question)  # Load existing choices

    context = {
        'question_form': question_form,
        'choice_formset': choice_formset,
    }
    return render(request, 'add_aptitude_questions.html', context)


@login_required
def delete_aptitude(request, id):
    AptitudeQuestions.objects.filter(id=id).delete()
    return redirect('aptitude_dashboard')



def aptitude_test(request):
    # Fetch random questions (e.g., 10 questions)
    questions = AptitudeQuestions.objects.order_by('?')[:10]
    context = {
        'questions': questions,
    }
    return render(request, 'aptitude_test_page.html', context)


def submit_test(request):
    test_taker_id = request.session.get('test_taker_id')
    if request.method == 'POST':
        score = 0
        total_questions = 0
        score_category = {}  # Store scores per category
        selected_answers = []

        # Iterate through all questions
        for question in AptitudeQuestions.objects.all():
            total_questions += 1
            selected_choice_id = request.POST.get(f'question_{question.id}')

            if selected_choice_id:
                selected_choice = Choice.objects.get(id=selected_choice_id)
                selected_answers.append(selected_choice)

                if selected_choice.is_correct:
                    score += 1
                    category_name = question.category.name
                    # Update category-wise score
                    if category_name in score_category:
                        score_category[category_name] += 1
                    else:
                        score_category[category_name] = 1
                    # Save response in the database

        # test_taker_uuid = uuid.UUID(test_taker_id)
        test_taker = TestTaker.objects.get(id=test_taker_id)
        response = AptitudeResponse.objects.create(
            test_taker=test_taker,
            score=score,
            score_category=score_category
        )

        response.selected_answer.set(selected_answers)  # Save selected answers

        # Store test completion in session (preventing back navigation)
        request.session['test_completed'] = True
        return redirect('result')

    else:
        # This else will likely never be executed as it is a post function
        return redirect('aptitude_test')