from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    age = models.PositiveSmallIntegerField(null=True, blank=True)

class Conversa(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='conversas')
    titulo = models.CharField(max_length=255)
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class Mensagem(models.Model):
    conversa = models.ForeignKey(Conversa, on_delete=models.CASCADE, related_name='mensagens')
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='mensagens', null=True)
    conteudo = models.TextField()
    criada_em = models.DateTimeField(auto_now_add=True)
    is_user = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.usuario.username}: {self.conteudo[:50]}'