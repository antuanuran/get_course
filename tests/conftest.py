import pytest

from apps.courses.models import Category, Course, Product
from apps.users.models import User


@pytest.fixture
def demo_author():
    return User.objects.create_user(email="demo-author@test.com")


@pytest.fixture
def demo_category():
    return Category.objects.create(name="demo-category")


@pytest.fixture
def demo_product(demo_category):
    return Product.objects.create(name="demo-product", category=demo_category)


@pytest.fixture
def course_create(demo_author, demo_product):
    Course.objects.create(author=demo_author, product=demo_product, name="course_1", price=100)
