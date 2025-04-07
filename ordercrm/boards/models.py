from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Board(TimeStampedModel):
    title = models.CharField(max_length=128)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.owner} > {self.title}"

    def save(self, *args, **kwargs):
        if self.order is None:
            max_order = Board.objects.filter(
                owner=self.owner).aggregate(
                models.Max('order'))['order__max']
            if max_order is None:
                max_order = 0
            self.order = max_order

        super().save(*args, **kwargs)


class Column(TimeStampedModel):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="columns")
    title = models.CharField(max_length=64)
    order = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.board.owner} > {self.board.title} > {self.title}"

    def save(self, *args, **kwargs):
        if self.order is None:
            max_order = Column.objects.filter(
                board=self.board).aggregate(
                models.Max('order'))['order__max']
            if max_order is None:
                max_order = 0
            self.order = max_order

        super().save(*args, **kwargs)


class Label(TimeStampedModel):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    color = models.CharField(max_length=10)
    title = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.board.title} > {self.title}"


class Card(TimeStampedModel):
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name="cards")
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    labels = models.ManyToManyField(Label, related_name="cards", blank=True)
    order = models.IntegerField(null=True, blank=True)
    archived = models.BooleanField(default=False)
    cover = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f"{self.column.board.owner} > {self.column.board.title} > {self.column.title} > {self.title}"

    def save(self, *args, **kwargs):
        if self.order is None:
            max_order = Card.objects.filter(
                column=self.column).aggregate(
                models.Max('order'))['order__max']
            if max_order is None:
                max_order = 0
            self.order = max_order

        super().save(*args, **kwargs)


class Invite(TimeStampedModel):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.board.owner} > {self.board.title} > {self.user}"