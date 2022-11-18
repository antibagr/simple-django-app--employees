from __future__ import annotations

import datetime as dt
import json
import random
from typing import TypeAlias

DataList: TypeAlias = list[dict[str, int | str | dict]]

APP_NAME = "employees"

FIRST_NAMES = (
    "John",
    "Andy",
    "Joe",
    "Sarah",
    "Jake",
    "Michael",
    "Ellen",
    "Tiffany",
    "Alice",
    "Joseph",
    "Jack",
    "John",
)
LAST_NAMES = (
    "Johnson",
    "Smith",
    "Williams",
    "Baxter",
    "Jennings",
    "Dennis",
    "Montoya",
    "Travis",
    "Leach",
    "Tucker",
    "Dixon",
)
POSITIONS = [
    "Developer",
    "Engineer",
    "HR",
    "Assistant",
    "DevOps",
    "QA",
    "Accountant",
    "Researcher",
]

DEPARTMENTS = [
    ("Evil Inc", 1, None),
    ("Gaming", 2, 1),
    ("Arcades", 3, 2),
    ("Shooters", 4, 2),
    ("Gambling/Casino", 5, 2),
    ("Online", 6, 2),
    ("Free-To-Play", 7, 6),
    ("Facebook RPG", 8, 6),
    ("DeFi Gaming", 9, 6),
    ("NTF Cards", 10, 9),
    ("NTF Development", 11, 10),
    ("NTF Product", 12, 10),
    ("Cloud Solutions", 13, 1),
    ("Data Science SAAS", 14, 13),
    ("ML", 15, 14),
    ("Computer Vision", 16, 15),
    ("Text-to-Speach", 17, 15),
    ("DevOps", 18, 16),
    ("CV Development", 19, 16),
    ("CV Product", 20, 16),
    ("QA", 21, 19),
    ("RnD", 22, 19),
    ("Algorhythms & Math", 23, 22),
    ("Quant", 24, 22),
    ("Engineers", 25, 22),
]


def get_departments() -> DataList:
    data = []
    model = f"{APP_NAME}.department"
    for department in DEPARTMENTS:
        data.append(
            {
                "model": model,
                "pk": department[1],
                "fields": {
                    "name": f"{department[0]} Department",
                    "head_department": department[2],
                },
            }
        )
    return data


def get_positions() -> DataList:
    data = []
    model = f"{APP_NAME}.position"
    for pk, p in enumerate(POSITIONS, start=1):
        data.append(
            {
                "model": model,
                "pk": pk,
                "fields": {"name": p},
            }
        )
    return data


def generate_employees() -> DataList:
    data = []
    model = f"{APP_NAME}.employee"
    for pk in range(50_000):
        data.append(
            {
                "model": model,
                "pk": pk,
                "fields": {
                    "first_name": random.choice(FIRST_NAMES),
                    "last_name": random.choice(FIRST_NAMES),
                    "family_name": None,
                    "position": random.randint(1, len(POSITIONS)),
                    "employment_date": dt.datetime.today().strftime("%Y-%m-%d"),
                    "salary": random.randint(1000, 10_0000),
                    "department": random.choice(DEPARTMENTS)[1],
                },
            }
        )
    return data


def fill_data() -> None:
    data = get_departments() + get_positions() + generate_employees()
    with open("data.json", "w") as f:
        f.write(json.dumps(data))


if __name__ == "__main__":
    fill_data()
