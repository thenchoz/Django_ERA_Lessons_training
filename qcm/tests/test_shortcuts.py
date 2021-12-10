"""
Django shortcut fct for tests for qcm app.
"""

from random import randrange

from ..models import Branch, Question, QuestionsSubset


def create_branch(branch_name):
    """usage fct
    create a branch with branch_name as name
    """
    return Branch.objects.create(name=branch_name)


def create_questions_subset(questions_subset_name, branch_id=None):
    """usage fct
    create a questions subset with questions_subset_name as name
    using the branch corresponding to branch_id
    empty basic branch if branch_id is None
    """
    if branch_id is None:
        branch = create_branch(branch_name="empty name")
    else:
        branch = Branch.objects.get(id=branch_id)
    return branch.questionssubset_set.create(name=questions_subset_name)


def create_question(question_text, questions_subset_id=None):
    """usage fct
    create a question with question_text as text
    using the questions_subset corresponding to questions_subset_id
    empty basic branch and questions_subset if questions_subset_id is None
    """
    if questions_subset_id is None:
        questions_subset = create_questions_subset(questions_subset_name="empty name")
    else:
        questions_subset = QuestionsSubset.objects.get(id=questions_subset_id)
    return questions_subset.question_set.create(question_text=question_text)


def create_choice(choice_text, is_true=False, question_id=None):
    """usage fct
    create a choice with choie_text as text and is_true as boolean
    using the question corresponding to question_id
    empty basic branch, questions_subset and question if quesion_id is None
    """
    if question_id is None:
        question = create_question(question_text="empty text")
    else:
        question = Question.objects.get(id=question_id)
    return question.choice_set.create(choice_text=choice_text, is_true=is_true)


def create_questions_subset_training(user, questions_subset_id=None):
    """usage fct
    create a training
    using the questions_subset corresponding to questions_subset_id
    empty basic branch and questions_subset if questions_subset_id is None
    """
    if questions_subset_id is None:
        questions_subset = create_questions_subset(questions_subset_name="empty name")
    else:
        questions_subset = QuestionsSubset.objects.get(id=questions_subset_id)
    return questions_subset.training_set.create(user=user)


def create_branch_training(user, branch_id=None):
    """usage fct
    create a training
    using the questions_subset corresponding to questions_subset_id
    empty basic branch and questions_subset if questions_subset_id is None
    """
    if branch_id is None:
        branch = create_branch(branch_name="empty name")
    else:
        branch = Branch.objects.get(id=branch_id)
    return branch.training_set.create(user=user)


def create_random_questions(questions_subset):
    """useage fct
    create random nb of questions for a given subset
    return list with all questions
    """

    nb_questions = randrange(1, 100)
    questions = []
    for i in range(nb_questions):
        question = questions_subset.question_set.create(
            question_text="random " + str(i)
        )
        questions.append(question)

    return questions
