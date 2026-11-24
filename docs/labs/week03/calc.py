"""아주 작은 계산기. 3주차 실습(PR·Actions)에서 쓰는 예제예요."""


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("0 으로 나눌 수 없어요")
    return a / b
