import logging
import time
from collections import defaultdict

from django.shortcuts import render
from employees.models import Department

logger = logging.getLogger(__name__)


class HTMLListDepartmentSerializer:
    """
    Serializer creates a nested tree representation of departments with each
    head-department being a node, and each subdivision being its offspring.
    Employees are also considered as a child node.

    {
        "Foo Department": {
            "employees": []
            "departments": {
                "Bar Department": {
                    "departments": {...}, "employees": {...}
                }
            }
        }
    }
    """

    subdivisions: dict[Department, list[Department]]

    def __init__(self, departments: list[Department]) -> None:
        self.subdivisions = self._get_subdivisions(departments)

    def _get_subdivisions(
        self, departments: list[Department]
    ) -> dict[Department, list[Department]]:
        subdivisions = defaultdict(list)
        for department in departments:
            subdivisions[department.head_department].append(department)
        return subdivisions

    def _serialize(self, department: Department) -> dict[str, dict]:
        serialized = {
            "employees": department.employees.all() if department is not None else None,
            "departments": {},
        }
        for subdivision in self.subdivisions[department]:
            serialized["departments"][subdivision.name] = self._serialize(subdivision)
        return serialized

    def serialize(self) -> dict[str, dict]:
        return self._serialize(None)["departments"]


def department_tree(request):
    start = time.perf_counter()
    all_departaments = Department.objects.prefetch_related(
        "head_department", "employees"
    ).all()
    end = time.perf_counter()
    logger.debug("SQL Execution Time: %s" % (end - start))

    start = time.perf_counter()
    serializer = HTMLListDepartmentSerializer(all_departaments)
    context = serializer.serialize()
    end = time.perf_counter()
    logger.debug("Serializing time: %s" % (end - start))

    return render(request, "employees_base.html", context={"departments": context})
