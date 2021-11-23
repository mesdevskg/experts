from django.contrib import admin

from items.models import Book, Expert, History


class ReadOnlyAdminMixin:
    @staticmethod
    def has_add_permission(_):
        return False

    @staticmethod
    def has_change_permission(_, __=None):
        return False

    @staticmethod
    def has_delete_permission(_, __=None):
        return False


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass


@admin.register(Expert)
class ExpertAdmin(admin.ModelAdmin):
    list_filter = 'book',
    readonly_fields = 'created',


@admin.register(History)
class HistoryAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    fields = 'winner', 'book', 'okuu_kitep', 'sector_knigi', 'created'
    list_filter = 'book', '_type'
