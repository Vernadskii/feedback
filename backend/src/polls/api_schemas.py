from datetime import datetime, date

from ninja import Schema
from pydantic import field_validator, model_validator

from polls.models import Poll


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
        allowed_channels: list[int] = [ch[0] for ch in Poll.CHANNELS]
        if channel not in allowed_channels:
            raise ValueError(f'Invalid channel value: {channel}. Allowed values are {allowed_channels}.')
        return channel

    # noinspection PyNestedDecorators
    @field_validator('status')
    @classmethod
    def status_must_be_valid(cls, status: int):
        allowed_status: list[int] = [status[0] for status in Poll.STATUSES]
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
