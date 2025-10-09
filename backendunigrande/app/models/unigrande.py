from tortoise import fields, models
from datetime import datetime


class PeriodoLetivo(models.Model):
    """
    Classe que representa a tabela PeriodoLetivo no banco de dados
    """
    id: int = fields.IntField(primary_key=True)
    ano: int = fields.IntField()
    semestre: int = fields.IntField()
    data_inicio: datetime = fields.DateField()
    data_fim: datetime = fields.DateField()

    class Meta:
        table = 'periodos_letivos'
        unique_together = (('ano', 'semestre'),)
        indexes = (('ano', 'semestre'),)


class Professor(models.Model):
    """
    Classe que representa a tabela Professor no banco de dados
    """
    id: int = fields.IntField(primary_key=True)
    matricula: int = fields.IntField()
    nome_professor: str = fields.CharField(max_length=255)
    endereco: str = fields.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    email: str = fields.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
    )

    class Meta:
        table = 'professores'
        unique_together = (('matricula', 'nome_professor'),)
        indexes = (('matricula', 'nome_professor'),)


class Curso(models.Model):
    """
    Classe que representa a tabela Curso no banco de dados
    """
    codigo_curso: int = fields.IntField(primary_key=True)
    nome_curso: str = fields.CharField(max_length=255)
    total_creditos: int = fields.IntField()
    idt_professor: fields.ForeignKeyField['Professor'] = fields.ForeignKeyField(
        'models.Professor',
        related_name='cursos',
        null=True,
        on_delete=fields.SET_NULL,
    )

    class Meta:
        table = 'cursos'
        unique_together = (('codigo_curso', 'nome_curso'),)
        indexes = (('codigo_curso', 'nome_curso'),)


class Disciplina(models.Model):
    """
    Classe que representa a tabela Disciplina no banco de dados
    """
    codigo_disciplina: int = fields.IntField(primary_key=True)
    nome_disciplina: str = fields.CharField(max_length=255)
    creditos: int = fields.IntField()
    tipo_disciplina: str = fields.CharField(max_length=255)
    horas_obrigatorias: int = fields.IntField()
    limite_faltas: int = fields.IntField()

    class Meta:
        table = 'disciplinas'
        unique_together = (('codigo_disciplina', 'nome_disciplina'),)
        indexes = (('codigo_disciplina', 'nome_disciplina'),)


class Matriz(models.Model):
    """
    Classe que representa a tabela Matriz no banco de dados
    """
    codigo_disciplina: fields.ForeignKeyField['Disciplina'] = fields.ForeignKeyField(
        'models.Disciplina',
        related_name='matrizes',
        on_delete=fields.CASCADE,
    )
    codigo_curso: fields.ForeignKeyField['Curso'] = fields.ForeignKeyField(
        'models.Curso',
        related_name='matrizes',
        on_delete=fields.CASCADE,
    )
    periodo_letivo: fields.ForeignKeyField['PeriodoLetivo'] = fields.ForeignKeyField(
        'models.PeriodoLetivo',
        related_name='matrizes',
        on_delete=fields.CASCADE,
    )

    class Meta:
        table = 'matrizes'
        unique_together = (
            ('codigo_disciplina', 'codigo_curso', 'periodo_letivo'),
        )
        indexes = (
            ('codigo_disciplina', 'codigo_curso', 'periodo_letivo'),
        )


class Turma(models.Model):
    """
    Classe que representa a tabela Turma no banco de dados
    """
    ano: fields.ForeignKeyField['PeriodoLetivo'] = fields.ForeignKeyField(
        'models.PeriodoLetivo',
        related_name='turmas_ano',
        on_delete=fields.CASCADE,
    )
    semestre: fields.ForeignKeyField['PeriodoLetivo'] = fields.ForeignKeyField(
        'models.PeriodoLetivo',
        related_name='turmas_semestre',
        on_delete=fields.CASCADE,
    )
    codigo_disciplina: fields.ForeignKeyField['Disciplina'] = fields.ForeignKeyField(
        'models.Disciplina',
        related_name='turmas',
        on_delete=fields.CASCADE,
    )
    vagas: int = fields.IntField()
    idt_professor: fields.ForeignKeyField['Professor'] = fields.ForeignKeyField(
        'models.Professor',
        related_name='turmas',
        on_delete=fields.CASCADE,
    )

    class Meta:
        table = 'turmas'
        unique_together = (
            ('ano', 'codigo_disciplina', 'idt_professor'),)
        indexes = (
            ('ano', 'codigo_disciplina', 'idt_professor'),
        )


class Aluno(models.Model):
    """
    Classe que representa a tabela Aluno no banco de dados
    """
    matricula_aluno: int = fields.IntField(primary_key=True)
    nome_aluno: str = fields.CharField(max_length=255)
    total_creditos: int = fields.IntField()
    data_nascimento: datetime = fields.DateField()
    mgp: int = fields.IntField()
    codigo_curso: fields.ForeignKeyField['Curso'] = fields.ForeignKeyField(
        'models.Curso',
        related_name='alunos',
        on_delete=fields.CASCADE
    )

    class Meta:
        table = 'alunos'
        unique_together = (('matricula_aluno', 'nome_aluno'),)
        indexes = (('matricula_aluno', 'nome_aluno'),)


class Matricula(models.Model):
    """
    Classe que representa a tabela Matricula no banco de dados
    """
    ano: fields.ForeignKeyField['PeriodoLetivo'] = fields.ForeignKeyField(
        'models.PeriodoLetivo',
        related_name='matriculas_ano',
        on_delete=fields.CASCADE,
    )
    semestre: fields.ForeignKeyField['PeriodoLetivo'] = fields.ForeignKeyField(
        'models.PeriodoLetivo',
        related_name='matriculas_semestre',
        on_delete=fields.CASCADE,
    )
    matricula_aluno: fields.ForeignKeyField['Aluno'] = fields.ForeignKeyField(
        'models.Aluno',
        related_name='matriculas',
        on_delete=fields.CASCADE,
    )
    codigo_disciplina: fields.ForeignKeyField['Disciplina'] = fields.ForeignKeyField(
        'models.Disciplina',
        related_name='matriculas',
        on_delete=fields.CASCADE,
    )
    nota_1: int = fields.IntField()
    nota_2: int = fields.IntField()
    nota_3: int = fields.IntField()
    faltas_1: int = fields.IntField()
    faltas_2: int = fields.IntField()
    faltas_3: int = fields.IntField()

    class Meta:
        table = 'matriculas'
        unique_together = (
            ('ano', 'semestre', 'matricula_aluno', 'codigo_disciplina'),
        )
        indexes = (
            ('ano', 'semestre', 'matricula_aluno', 'codigo_disciplina'),
        )


class Historico(models.Model):
    """
    Classe que representa a tabela Historico no banco de dados
    """
    ano: fields.ForeignKeyField['PeriodoLetivo'] = fields.ForeignKeyField(
        'models.PeriodoLetivo',
        related_name='historicos_ano',
        on_delete=fields.CASCADE,
    )
    semestre: fields.ForeignKeyField['PeriodoLetivo'] = fields.ForeignKeyField(
        'models.PeriodoLetivo',
        related_name='historicos_semestre',
        on_delete=fields.CASCADE,
    )
    matricula_aluno: fields.ForeignKeyField['Aluno'] = fields.ForeignKeyField(
        'models.Aluno',
        related_name='historicos',
        on_delete=fields.CASCADE,
    )
    codigo_disciplina: fields.ForeignKeyField['Disciplina'] = fields.ForeignKeyField(
        'models.Disciplina',
        related_name='historicos',
        on_delete=fields.CASCADE,
    )
    situacao: str = fields.CharField(max_length=255)
    media: float = fields.FloatField()
    faltas: int = fields.IntField()

    class Meta:
        table = 'historicos'
        unique_together = (
            ('ano', 'semestre', 'matricula_aluno', 'codigo_disciplina'),
        )
        indexes = (
            ('ano', 'semestre', 'matricula_aluno', 'codigo_disciplina'),
        )
