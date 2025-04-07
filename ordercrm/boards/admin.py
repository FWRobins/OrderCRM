from django.contrib import admin
from .models import Board, Label, Card, Column, Invite

# Register your models here.
@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
    list_filter = (
        'created',
    )
    list_per_page = 100
    ordering = ("-created", )


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
    list_filter = (
        'created',
    )
    list_per_page = 100
    ordering = ("-created", )


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
    list_filter = (
        'created',
    )
    list_per_page = 100
    ordering = ("-created", )

class CardTabularInlineAdmin(admin.TabularInline):
    fields = (
        'title',
        'due_date',
        'order',
        'archived',
    )
    model = Card
    show_change_link = True
    extra = 1


@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
    list_filter = (
        'created',
    )
    list_per_page = 100
    ordering = ("-created", )
    inlines = (
        CardTabularInlineAdmin,
    )

class InviteTabularInlineAdmin(admin.TabularInline):
    fields = (
        'user',
    )
    model = Invite
    show_change_link = True
    extra = 1


class ColumnTabularInlineAdmin(admin.TabularInline):
    fields = (
        'title',
        'order',
    )
    model = Column
    show_change_link = True
    extra = 1


class LabelTabularInlineAdmin(admin.TabularInline):
    fields = (
        'title',
        'color',
    )
    model = Label
    show_change_link = True
    extra = 1


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'owner', 'created')
    list_filter = (
        'created',
    )
    list_per_page = 100
    ordering = ("-created", )
    inlines = (
        InviteTabularInlineAdmin,
        ColumnTabularInlineAdmin,
        LabelTabularInlineAdmin
    )