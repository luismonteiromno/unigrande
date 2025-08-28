from tortoise import fields, models
from datetime import datetime


class PeriodoLetivo(models.Model):
    id: int = fields.IntField(pk=True)
    ano: int = fields.IntField()
    semestre: int = fields.IntField()
    data_inicio: datetime = fields.DateField()
    data_fim: datetime = fields.DateField()

    class Meta:
        table = 'periodos_letivos'
        unique_together = (('ano', 'semestre'),)
        indexes = (('ano', 'semestre'),)


class Professor(models.Model):
    pass


class Curso(models.Model):
    pass


class Disciplina(models.Model):
    pass


class Matriz(models.Model):
    pass


class Turme(models.Model):
    pass


class Aluno(models.Model):
    pass


class Matricula(models.Model):
    pass


class Historico(models.Model):
    pass
