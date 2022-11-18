from django.contrib import admin
from employees.models import Department, Employee, Position


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    ...


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    ...


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    ...
