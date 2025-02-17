from __future__ import annotations

import abc
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import UUID


class Notification(abc.ABC):

    @classmethod
    def slug(cls) -> str:
        return ''.join([
            f'-{x}' if x.isupper() else x for x in cls.__name__
        ]).lower().lstrip('-')


@dataclass
class Welcome(Notification):
    user_id: str
    email: str


@dataclass
class Invite(Notification):
    invite_id: UUID
    org_name: str
    user_name: Optional[str]  # None means this is a new user
    user_email: str
    console_url: str


@dataclass
class JobNotification(Notification, abc.ABC):
    job_id: str


@dataclass
class JobCannotStartLackResources(JobNotification):
    ...


@dataclass
class JobTransition(JobNotification):
    job_id: str
    status: str
    transition_time: datetime
    reason: Optional[str] = None
    description: Optional[str] = None
    exit_code: Optional[int] = None
    prev_status: Optional[str] = None
    prev_transition_time: Optional[datetime] = None


class QuotaResourceType(str, Enum):
    NON_GPU = "non_gpu"
    GPU = "gpu"


@dataclass
class JobCannotStartQuotaReached(Notification):
    user_id: str
    resource: QuotaResourceType
    quota: float
    cluster_name: str


@dataclass
class QuotaWillBeReachedSoon(Notification):
    user_id: str
    resource: QuotaResourceType
    used: float
    quota: float
    cluster_name: str


@dataclass
class JobCannotStartNoCredits(Notification):
    user_id: str
    cluster_name: Optional[str] = None


@dataclass
class CreditsWillRunOutSoon(Notification):
    user_id: str
    cluster_name: str
    credits: Decimal


@dataclass
class OrgCreditsWillRunOutSoon(Notification):
    org_name: str
    credits: Decimal
    seconds_left: int
    """An integer, representing an interval in seconds, which organization has,
    before the balance reaches zero
    """


@dataclass
class OrgCreditsDepleted(Notification):
    org_name: str
    credits: Decimal


@dataclass
class OrgBalanceTopUp(Notification):
    org_name: str


@dataclass
class AlertManagerNotification(Notification):
    class Status(str, Enum):
        RESOLVED = "resolved"
        FIRING = "firing"

    @dataclass
    class Alert:
        status: AlertManagerNotification.Status
        labels: dict[str, str]
        annotations: dict[str, str]

    version: str
    group_key: str
    status: Status
    group_labels: dict[str, str]
    common_labels: dict[str, str]
    common_annotations: dict[str, str]
    alerts: list[Alert]
