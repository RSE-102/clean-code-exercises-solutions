# This solution separates the ordering of debtors as well
# as the formatting of how their debt should be displayed
# in the report into two separate functions.

from dataclasses import dataclass
from typing import Iterable


@dataclass
class Debtor:
    """Stores the information on a person owing us money"""
    name: str
    debt: float


def list_debtors(debtors: Iterable[Debtor]) -> None:
    for debtor in debtors:
        print(f"{debtor.name}: {_format_debt(debtor.debt)}")


def payday(debtors: Iterable[Debtor]) -> None:
    list_debtors(_order_by_descending_debt(debtors))


def _order_by_descending_debt(debtors: Iterable[Debtor]) -> Iterable[Debtor]:
    return reversed(sorted(debtors, key=lambda debtor: debtor.debt))


def _format_debt(debt: float) -> str:
    return str(debt) if debt <= 100.0 else f"!!!{debt}!!!"


if __name__ == "__main__":
    payday([
        Debtor("Person1", 100.0),
        Debtor("Person2", 200.0),
        Debtor("Person3", 10.0),
        Debtor("Person4", 50.0),
        Debtor("Person5", 1250.0)
    ])
