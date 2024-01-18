# import csv
# from .models import Category, Product, Teacher, Version, Course, Course_version
# from django.core.exceptions import ValidationError
#
#
# def import_data(data_stream, data_format, owner_id):
#     if data_format == "csv":
#         csv_data = csv.DictReader(data_stream, delimiter=",")
#         for entity in csv_data:
#             category, _ = Category.objects.get_or_create(name=entity["category"])
#             product, _ = Product.objects.get_or_create(name=entity["product"], category_id=category.id)
#
#             course = Course.objects.filter(upc=entity["product_id"], level=entity["version"]).first()
#
#             if course:
#                 course.product = product
#                 course.level = entity["version"]
#                 course.save(update_fields=["product", "level"])
#
#             else:
#                 course = Course.objects.create(product_id=product.id,
#                 level=entity["version"], upc=entity["product_id"],)
#
#     else:
#         raise ValidationError(f" format: '{data_format}' not supported")
