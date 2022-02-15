from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models


class Trade(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    type = models.CharField(max_length=4, validators=[RegexValidator(regex='^(buy|sell)$')])
    user_id = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    symbol = models.CharField(max_length=10)
    shares = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)],)
    price = models.FloatField(validators=[MinValueValidator(0)])
    timestamp = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    class Meta:
        ordering = ['id']

    def __str__(self) -> str:
        return f'{self.user_id}: {self.symbol}-{self.shares}'
