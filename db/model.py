from tortoise import fields, models


class Student(models.Model):
    id = fields.CharField(pk=True, max_length=11)
    name = fields.CharField(max_length=12)
    addr = fields.CharField(max_length=50, default='武汉市')
    valid = fields.BooleanField(default=True)
    last_check = fields.DatetimeField()
