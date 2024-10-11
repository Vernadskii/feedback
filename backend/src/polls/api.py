from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate, PageNumberPagination

from polls.api_schemas import BasePollSchema, ExistingPollSchema, QuestionSchema
from polls.models import Poll, PollQuestion
from users.auth import AuthBearer

router = Router(tags=["polls"])


@router.post("/", response={201: ExistingPollSchema, 400: str}, auth=AuthBearer())
def create_poll(request, payload: BasePollSchema):
    try:
        poll = Poll.objects.create(author_id=request.auth.pk, **payload.dict())
        poll.save()
    except Exception as e:
        return 400, f"An unexpected error occurred: {str(e)}"
    return 201, ExistingPollSchema.model_validate(poll)


@router.put("/{poll_id}", response={200: ExistingPollSchema, 400: str}, auth=AuthBearer())
def update_poll(request, poll_id: int, payload: BasePollSchema):
    poll = get_object_or_404(Poll, pk=poll_id)
    try:
        # Update the instance
        for attr, value in payload.dict().items():
            setattr(poll, attr, value)
        poll.save()
    except Exception as e:
        return 400, f"An unexpected error occurred: {str(e)}"
    return 200, ExistingPollSchema.model_validate(poll)


@router.get("/{poll_id}", response={200: ExistingPollSchema, 404: str}, auth=AuthBearer())
def get_poll(request, poll_id: int):
    poll = get_object_or_404(Poll, id=poll_id)
    return ExistingPollSchema.model_validate(poll)


@router.get("/", response=list[ExistingPollSchema], auth=AuthBearer())
@paginate(PageNumberPagination, page_size=15)
def list_polls(request, status: int = 0):
    if status == 0:
        return Poll.objects.all()
    elif status in Poll.poll_statuses


# Questions

@router.post("/{poll_id}/questions", response={201: str, 400: str}, auth=AuthBearer())
def create_questions(request, poll_id: int, questions: list[QuestionSchema]):
    """Добавление вопросов для опроса."""
    try:
        for question in questions:
            _question = PollQuestion.objects.create(poll_id=poll_id, **question.dict())
            _question.save()
    except Exception as e:
        return 400, f"An unexpected error occurred: {str(e)}"
    return 201, "Created"


@router.get("/{poll_id}/questions", response={200: list[QuestionSchema], 400: str}, auth=AuthBearer())
def list_questions(request, poll_id: int):
    """Список вопросов для опроса."""
    questions = PollQuestion.objects.filter(poll_id=poll_id)
    result = [QuestionSchema.model_validate(question) for question in questions]
    return result
