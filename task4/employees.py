#!/usr/bin/env python3

import fdb
import pickle
import random

from dataclasses import dataclass


fdb.api_version(630)

EMPLOYEE = fdb.Subspace(('employee',))
DEPARTMENT_INDEX = fdb.Subspace(('department_idx',))


@dataclass
class Employee:
    first_name: str
    last_name: str
    department_code: str
    salary: int


@fdb.transactional
def put_employee(tr, id, employee):
    tr[EMPLOYEE[id]] = pickle.dumps(employee)
    tr[DEPARTMENT_INDEX[employee.department_code][id]] = b''


@fdb.transactional
def get_employee(tr, id):
    return pickle.loads(bytes(tr[EMPLOYEE[id]]))


@fdb.transactional
def get_employee_ids_by_department(tr, department_code):
    return [
        DEPARTMENT_INDEX.unpack(key)[1]
        for key, _ in tr[DEPARTMENT_INDEX[department_code].range()]
    ]


if __name__ == '__main__':
    db = fdb.open()

    del db[EMPLOYEE.range()]
    del db[DEPARTMENT_INDEX.range()]

    # Generate employees and put them into the DB
    for id in range(1000):
        first_name = random.choice([
            'Anton',
            'Valery',
            'Ivan',
            'Alexandr',
            'Vasiliy',
            'Egor',
            'Fyodor',
            'Valentin',
            'Yevgeniy',
            'Gennadiy'
        ])

        last_name = random.choice([
            'Ivanov',
            'Petrov',
            'Sidorov',
            'Agapkin',
            'Zheltorotov',
            'Bezrukov',
            'Dlinnonogov',
            'Vasiliev',
            'Gavrilov',
            'Stepanov'
        ])

        department_code = random.randint(1, 32)

        salary = random.randint(100000, 1000000)

        put_employee(db, id, Employee(first_name, last_name, department_code, salary))
    
    # Get employee by id
    print('Employee with id=5:', get_employee(db, 5))

    # Get all employees by department code
    print('All employees in department 15:')
    for id in get_employee_ids_by_department(db, 15):
        print('   ', get_employee(db, id))
