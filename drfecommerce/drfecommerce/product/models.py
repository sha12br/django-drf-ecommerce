from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


# OopCompanion:suppressRename

# Create your models here.


class Category(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)
    """
    The above means for example
    ------------------
    name,       parent
    ------------------
    clothes,    NULL
    shoes,      clothes
    
    if we delete clothes which is a Parent Category, then we should delete the sub-cat first
    """

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    # if there is a FK reference then this field will be called brand -> brand_id
    # this means that if a brand is deleted from Brand table , corresponding products are deleted from Product table
    category = TreeForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    # category -> category_id ; since FK reference
    # null=True, blank=True -> A Product may not be a part of Category

    def __str__(self):
        return self.name
