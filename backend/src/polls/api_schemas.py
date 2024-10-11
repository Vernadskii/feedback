from datetime import datetime, date

from ninja import Schema
from pydantic import field_validator, model_validator

from polls.models import Poll, PollQuestion


class BasePollSchema(Schema):
    title: str
    channel: int
    status: int
    date_start: date
    date_finish: date

    communications_total: int

    # noinspection PyNestedDecorators
    @field_validator('channel')
    @classmethod
    def channel_must_be_valid(cls, channel: int):
        allowed_channels: list[int] = Poll.poll_channels()
        if channel not in allowed_channels:
            raise ValueError(f'Invalid channel value: {channel}. Allowed values are {allowed_channels}.')
        return channel

    # noinspection PyNestedDecorators
    @field_validator('status')
    @classmethod
    def status_must_be_valid(cls, status: int):
        allowed_status: list[int] = Poll.poll_statuses()
        if status not in allowed_status:
            raise ValueError(f'Invalid status value: {status}. Allowed values are {allowed_status}.')
        return status

    @model_validator(mode='after')
    def validate_start_and_end_dates(self):
        if self.date_start > self.date_finish:
            raise ValueError("date_start cannot be later than date_finish.")
        return self


class ExistingPollSchema(BasePollSchema):
    """Schema for returning a poll data after its creating."""
    id: int
    stats_sent: int
    modified: datetime
    author_id: int


# Questions

class QuestionSchema(Schema):
    title: str
    question_type: int
    is_required: bool
    image: str | None = None
    has_skip_answer: bool

    # noinspection PyNestedDecorators
    @field_validator('question_type')
    @classmethod
    def question_type_must_be_valid(cls, _type: int):
        allowed_types: list[int] = [_type[0] for _type in PollQuestion.TYPES]
        if _type not in allowed_types:
            raise ValueError(f'Invalid question_type value: {_type}. Allowed values are {allowed_types}.')
        return _type

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Тест вопроса",
                    "question_type": 1,
                    "is_required": True,
                    "has_skip_answer": True,
                }
            ]
        }
    }
