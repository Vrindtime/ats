# personality/views.py
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Choice, PersonalityUserResponse, Category, PersonalityResult
from .forms import QuestionForm, ChoiceForm
from home.models import TestTaker
from django.contrib.auth.decorators import login_required

@login_required
def personality_dashboard(request):
    questions = Question.objects.all()
    return render(request, 'personality/dashboard.html', {'questions': questions})

@login_required
def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('personality_dashboard')
    else:
        form = QuestionForm()
    return render(request, 'personality/add_question.html', {'form': form})

@login_required
def add_choice(request, question_id):
    question = Question.objects.get(id=question_id)

    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice_text = form.cleaned_data['text']

            # Check if choice already exists for this question
            if question.choice_set.filter(text__iexact=choice_text).exists():
                form.add_error('text', 'This choice already exists for the question.')
            else:
                choice = form.save(commit=False)
                choice.question = question
                choice.save()
                return redirect('add_choice', question_id=question_id)
    else:
        form = ChoiceForm()

    existing_choices = question.choice_set.all()

    return render(request, 'personality/add_choice.html', {
        'form': form,
        'question': question,
        'existing_choices': existing_choices
    })

@login_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            # Check if category already exists
            # to prevent categories with the same name but different cases (e.g., "openness" vs."Openness"),
            # use iexact in the filter:
            if Category.objects.filter(name__iexact=name).exists():
                messages.error(request, f'Category "{name}" already exists!')
            else:
                Category.objects.create(name=name)
                messages.success(request, f'Category "{name}" added successfully!')
                return redirect('personality_dashboard')

    categories = Category.objects.all()
    return render(request, 'personality/add_category.html', {
        'categories': categories
    })
@login_required
def edit_question(request,id):
    question = get_object_or_404(Question,id=id)
    if request.method == 'POST':
        form = QuestionForm(request.POST,instance=question)
        if form.is_valid():
            form.save()
            return redirect('personality_dashboard')
    else:
        form = QuestionForm(instance=question)
    return render(request, 'personality/add_question.html', {'form': form})

@login_required
def delete_question(request,id):
    question = get_object_or_404(Question, id=id)
    question.delete()
    return redirect('personality_dashboard')


def delete_choice(request,id):
    choice = get_object_or_404(Choice,id=id)
    # Retrieve question ID before deletion
    question_id = choice.question.id
    choice.delete()
    return redirect('add_choice', question_id=question_id)

def personality_test(request):
    # Get the test-taker's ID from the session.
    test_taker_id = request.session.get('test_taker_id')
    if not test_taker_id:
        messages.error(request, "Test-taker ID is missing.")
        return redirect('start_test')  # Adjust as needed

    test_taker = get_object_or_404(TestTaker, id=test_taker_id)

    if request.method == 'POST':
        # Process and save responses for each question.
        # Assume form fields are named like "q<question.id>"
        questions = Question.objects.order_by('?')[:10]  # You might want to persist the same 10 questions during the test.
        for question in questions:
            choice_id = request.POST.get(f'q{question.id}')
            if choice_id:
                try:
                    choice = Choice.objects.get(id=choice_id)
                except Choice.DoesNotExist:
                    continue  # Skip if choice is not found
                PersonalityUserResponse.objects.create(
                    test_taker=test_taker,
                    question=question,
                    choice=choice
                )

        # After saving responses, compute aggregated scores.
        responses = PersonalityUserResponse.objects.filter(test_taker=test_taker)
        categories = Category.objects.all()

        # Initialize accumulators.
        category_totals = {category.name: 0 for category in categories}
        category_counts = {category.name: 0 for category in categories}

        # Sum up the scores for each category.
        for response in responses:
            cat_name = response.question.category.name
            category_totals[cat_name] += response.choice.score
            category_counts[cat_name] += 1

        # Compute average score per category.
        averaged_scores = {}
        for cat_name in category_totals:
            if category_counts[cat_name] > 0:
                averaged_scores[cat_name] = round(category_totals[cat_name] / category_counts[cat_name], 2)
            else:
                averaged_scores[cat_name] = 0

        # Compute overall total score (for example, the sum of averages).
        total_score = sum(averaged_scores.values())

        # Save (or update) the final PersonalityResult for this test-taker.
        PersonalityResult.objects.update_or_create(
            test_taker=test_taker,
            defaults={
                'scores': averaged_scores,
                'total_score': total_score,
                'approved': total_score >= 5  # Example: approval if total_score is 15 or higher.
            }
        )

        # Redirect to the next test section.
        return redirect('aptitude_test')

    # For GET requests: show 10 random personality questions.
    questions = Question.objects.order_by('?')[:10]
    context = {
        'questions': questions,
        'test_taker_id': test_taker_id,
    }
    return render(request, 'personality/test.html', context)