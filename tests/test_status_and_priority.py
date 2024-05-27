from rich import console, table
from rich.table import Table
import os
import json
import re
import uuid
import datetime
from enum import Enum
import bcrypt
import pytest
from main import CreateTask

def test_status_and_priority1():
    task1 = CreateTask("t1", "skeuhfuwsei")
    assert task1.status == task1.Status.BACKLOG
    assert task1.priority == task1.Priority.LOW
    task1.next_status()
    task1.next_priority()
    assert task1.status == task1.Status.TODO
    assert task1.priority == task1.Priority.MEDIUM
    task1.previous_status()
    task1.previous_priority()
    assert task1.status == task1.Status.BACKLOG
    assert task1.priority == task1.Priority.LOW

def test_status_and_priority2():
    task2 = CreateTask("t2", "nfeowioe")
    assert task2.status == task2.Status.BACKLOG
    assert task2.priority == task2.Priority.LOW
    task2.next_status()
    task2.next_status()
    task2.next_priority()
    task2.next_priority()
    assert task2.status == task2.Status.DOING
    assert task2.priority == task2.Priority.HIGH
    task2.previous_status()
    task2.previous_priority()
    assert task2.status == task2.Status.TODO
    assert task2.priority == task2.Priority.MEDIUM
