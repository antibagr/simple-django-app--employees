from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Position(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self) -> str:
        return str(self.name)


class Department(models.Model):
    name = models.CharField(max_length=128, unique=True)
    head_department = models.ForeignKey(
        "self", on_delete=models.PROTECT, blank=True, null=True
    )

    def get_all_head_departments(self) -> list[Department]:
        if self.head_department is not None:
            return [
                self.head_department
            ] + self.head_department.get_all_head_departments()
        return []

    def __str__(self) -> str:
        return str(self.name)

    def clean(self) -> None:
        head_departments = self.get_all_head_departments()
        if self in head_departments:
            raise ValidationError("Cyclic dependency detected")
        if len(head_departments) > 5:
            raise ValidationError("Too many nested head departments")
        return super().clean()


class Employee(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    family_name = models.CharField(max_length=30, null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.PROTECT)
    employment_date = models.DateField(null=False, blank=False, default=timezone.now)
    salary = models.SmallIntegerField(default=10_000)
    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, related_name="employees"
    )

    def clean(self):
        if self.employment_date > timezone.now().date():
            raise ValidationError("Employement date can't be in the future")

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name}"
