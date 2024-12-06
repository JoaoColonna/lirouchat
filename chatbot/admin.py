from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Mensagem, Conversa, TipoMensagem, Teste

class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff', 'age')

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'age')
        }),
        ('Permissions', {
            'fields': (
                    'is_active', 'is_staff', 'is_superuser',
                    'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        })
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'age')
        }),
        ('Permissions', {
            'fields': (
                    'is_active', 'is_staff', 'is_superuser',
                    'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        })
    )

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ('id', 'conteudo', 'criada_em', 'conversa', 'usuario', 'is_user', 'id_tipo_mensagem__nome')
    search_fields = ('conteudo', 'usuario__username')
    list_filter = ('criada_em', 'conversa')

@admin.register(Conversa)
class ConversaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'criada_em')
    search_fields = ('nome',)
    list_filter = ('criada_em',)

@admin.register(TipoMensagem)
class TipoMensagemAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)

@admin.register(Teste)
class TesteAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'texto')
    search_fields = ('nome', 'texto')