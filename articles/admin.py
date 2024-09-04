from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        main_scopes_count = 0
        for form in self.forms:
            if form.cleaned_data.get('is_main'):
                main_scopes_count += 1
                if main_scopes_count > 1:
                    raise ValidationError('Может быть только один основной тег.')
        if main_scopes_count == 0:
            raise ValidationError('Должен быть хотя бы один основной тег.')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass