from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Book(models.Model):
    name = models.CharField(_('book'), max_length=255, unique=True)

    class Meta:
        verbose_name = _('Book')
        verbose_name_plural = _('Books')

    def __str__(self):
        return self.name


class Expert(models.Model):
    book = models.ForeignKey('Book', models.DO_NOTHING)
    full_name = models.CharField(_('full name'), max_length=255)
    created = models.DateTimeField(_('joined time'), auto_now_add=True)

    class Meta:
        verbose_name = _('Expert')
        verbose_name_plural = _('Experts')

    def __str__(self):
        return self.full_name


class History(models.Model):
    TYPE_CHOICES = (
        ('илимий', 'илимий'),
        ('илимий-педагогикалык', 'илимий-педагогикалык'),
        ('антидискриминациялык жана гендердик', 'антидискриминациялык жана гендердик')
    )
    created = models.DateTimeField(_('created time'), auto_now_add=True)
    winner = models.ForeignKey('Expert', models.SET_NULL, null=True, verbose_name=_('Winner'))
    book = models.ForeignKey('Book', models.DO_NOTHING)
    _type = models.CharField(_('Type'), max_length=255, choices=TYPE_CHOICES)
    okuu_kitep = models.ForeignKey('users.User', models.SET_NULL, null=True,
                                    related_name='history1', verbose_name=_('Okuu Kitep'))
    sector_knigi = models.ForeignKey('users.User', models.SET_NULL, null=True,
                                    related_name='history2', verbose_name=_('Sector Knigi'))
    document = models.TextField(_('document'))

    class Meta:
        verbose_name = _('History')
        verbose_name_plural = _('Histories')
        ordering = '-created',

    def clean(self):
        if self.okuu_kitep == self.sector_knigi:
            raise ValidationError(_('commission one and commission two can\'t be same'))

    def __str__(self):
        return f'{self.winner.full_name} {self.created.strftime("%d %b %Y %H:%M:%S")}'
