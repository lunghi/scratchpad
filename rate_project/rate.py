import dataclasses
from datetime import datetime
from decimal import Decimal
from typing import Iterable, TypeVar

Amount = Decimal


@dataclasses.dataclass
class Rate:
    start_date: datetime
    end_date: datetime
    amount: Amount
    priority: int


RateMatrix = Iterable[Rate]


def applicable_rates(m: RateMatrix, d: datetime) -> RateMatrix:
    # return (_ for _ in filter(lambda _: _.start_date <= d <= _.end_date, m))
    return (_ for _ in m if _.start_date <= d <= _.end_date)


def sort_by_priority_desc(m: RateMatrix) -> RateMatrix:
    return sorted(m, key=lambda _: _.priority, reverse=True)


T = TypeVar('T')


def first_or_none(a: Iterable[T]) -> T | None:
    for _ in a:
        return _


def first_amount_or_none(m: RateMatrix) -> Amount | None:
    if r := first_or_none(m):
        return r.amount


def active_rate_amount(m: RateMatrix, d: datetime) -> Amount | None:
    return first_amount_or_none(sort_by_priority_desc(applicable_rates(m, d)))


EPOCH: datetime = datetime(2023, month=1, day=1)


def pin_date(d: datetime) -> datetime:
    return max(EPOCH, d)


def offer_start_rate(m: RateMatrix, d: datetime) -> Amount | None:
    return active_rate_amount(m, max(EPOCH, d))
