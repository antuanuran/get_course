import pytest
from rest_framework.test import APIClient

from apps.courses.models import Course
from apps.purchases.models import Purchase
from apps.users.models import User

pytestmark = pytest.mark.django_db


@pytest.fixture
def course_builder(demo_author, demo_product):
    def wrapper(n: int, is_sellable: bool = True) -> list[Course]:
        start_index = Course.objects.count()
        return Course.objects.bulk_create(
            [
                Course(
                    author=demo_author,
                    product=demo_product,
                    name=f"course-{start_index + i}",
                    price=100,
                    is_sellable=is_sellable,
                )
                for i in range(n)
            ]
        )

    return wrapper


def test_list_courses_anonymous(course_builder):
    course_builder(10, is_sellable=True)
    course_builder(10, is_sellable=False)

    client = APIClient()
    response = client.get("/api/v1/courses/")
    assert response.status_code == 200
    data = response.json()["courses"]
    assert len(data) == 10


def test_list_courses_logged(course_builder):
    course_builder(10, is_sellable=True)
    course_builder(10, is_sellable=False)
    client = APIClient()

    user = User.objects.create_user(email="demo@test.com")
    user_token = user.generate_token()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + user_token)
    response = client.get("/api/v1/courses/")
    assert response.status_code == 200


def purcheses_build(user, product):
    course = Course.objects.create(author=user, product=product, price=100)
    Purchase.objects.create(user=user, course=course)


def test_ping_purcheses(demo_author, demo_product):
    client = APIClient()
    user = demo_author
    product = demo_product

    user_token = user.generate_token()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + user_token)

    purcheses_build(user, product)

    response = client.get("/api/v1/purchases/")
    assert response.status_code == 200

    data = response.json()["purchases"]
    assert len(data) == 1
