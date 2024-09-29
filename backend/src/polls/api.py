from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate, PageNumberPagination

from polls.api_schemas import BasePollSchema, ExistingPollSchema
from polls.models import Poll
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


@router.get("/{poll_id}", response={200: ExistingPollSchema, 404: str}, auth=AuthBearer())
def get_poll(request, poll_id: int):
    poll = get_object_or_404(Poll, id=poll_id)
    return ExistingPollSchema.model_validate(poll)


@router.get("/", response=list[ExistingPollSchema], auth=AuthBearer())
@paginate(PageNumberPagination, page_size=1)
def list_polls(request):
    return Poll.objects.all()
