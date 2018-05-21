from django.db import models


class Repository(models.Model):
    url = models.URLField(verbose_name="URL репозитория")
    username = models.CharField(max_length=150, verbose_name=u"Имя пользователя Gitlab")
    repository = models.CharField(max_length=150, verbose_name=u"Название репозитория")
    last_activity = models.DateTimeField(auto_now_add=True,
                                         verbose_name=u"Время последней активности")
    user_id = models.IntegerField(verbose_name="ID пользователя")

    class Meta:
        ordering = ('username', 'repository',)
