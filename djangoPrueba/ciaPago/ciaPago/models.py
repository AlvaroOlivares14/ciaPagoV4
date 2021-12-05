# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_flag = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

"""-----------------------------------------------------------------
                        Tablas personalizadas
--------------------------------------------------------------------"""

class Comunero(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(primary_key=True, max_length=30, null=False)
    telefonocelular1 = models.IntegerField(db_column='telefonoCelular1', blank=True, null=True)  # Field name made lowercase.
    telefonocelular2 = models.IntegerField(db_column='telefonoCelular2', blank=True, null=True)  # Field name made lowercase.
    telefonocelular3 = models.IntegerField(db_column='telefonoCelular3', blank=True, null=True)  # Field name made lowercase.
    telefonofijo = models.IntegerField(db_column='telefonoFijo', blank=True, null=True)  # Field name made lowercase.
    email1 = models.CharField(max_length=256, blank=True, null=True)
    email2 = models.CharField(max_length=256, blank=True, null=True)
    calle = models.CharField(max_length=256, blank=True, null=True)
    ciudad = models.CharField(max_length=256, blank=True, null=True)
    numerocalle = models.IntegerField(db_column='numeroCalle', blank=True, null=True)  # Field name made lowercase.
    comuna = models.CharField(max_length=256, blank=True, null=True)
    ubicacion = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.rut

    class Meta:
        managed = False
        db_table = 'comunero'
        verbose_name_plural = 'Comuneros'



class Cuotassociales(models.Model):
    idcuota = models.CharField(primary_key=True, db_column='idCuota', max_length=256, null=False)  # Field name made lowercase.
    valor = models.IntegerField(null=False)
    fechaemicion = models.CharField(db_column='fechaEmicion', max_length=256, null=False)  # Field name made lowercase.
    fechavencimiento = models.CharField(db_column='fechaVencimiento', max_length=256, null=False)  # Field name made lowercase.
    estadocuota = models.IntegerField(db_column='estadoCuota', null=False)  # Field name made lowercase.
    fk_rut = models.ForeignKey(Comunero, models.DO_NOTHING, db_column='fk_rut', null=False)
    fk_idtransaccion = models.ForeignKey('Pagos', models.DO_NOTHING, db_column='fk_idTransaccion', blank=True, null=True)  # Field name made lowercase.
    fk_idcasub3 = models.ForeignKey('Pozoasociado', models.DO_NOTHING, db_column='fk_idCasub3', null=False)  # Field name made lowercase.

    def __str__(self):
        return self.idcuota

    class Meta:
        managed = False
        db_table = 'cuotasSociales'
        verbose_name_plural = 'Cuotas sociales'


class Derechopozo(models.Model):
    idderecho = models.AutoField(primary_key=True, db_column='idDerecho', blank=True, null=False)  # Field name made lowercase.
    fk_rut = models.ForeignKey(Comunero, models.DO_NOTHING, db_column='fk_rut', null=False)
    fk_idcasub = models.ForeignKey('Pozoasociado', models.DO_NOTHING, db_column='fk_idCasub', null=False)  # Field name made lowercase.

    def __str__(self):
        return str(self.idderecho)

    class Meta:
        managed = False
        db_table = 'derechoPozo'
        verbose_name_plural = 'Derechos a pozo (relacion)'


class PagoPozo(models.Model):
    idpagopozo = models.AutoField(primary_key=True, db_column='idPagoPozo', blank=True, null=False)  # Field name made lowercase.
    fk_idtransaccion2 = models.ForeignKey('Pagos', models.DO_NOTHING, db_column='fk_idTransaccion2', null=False)  # Field name made lowercase.
    fk_idcasub2 = models.ForeignKey('Pozoasociado', models.DO_NOTHING, db_column='fk_idCasub2', null=False)  # Field name made lowercase.

    def __str__(self):
        return str(self.idpagopozo)

    class Meta:
        managed = False
        db_table = 'pago_pozo'
        verbose_name_plural = 'Pagos pozo (relacion)'


class Pagos(models.Model):
    idtransaccion = models.CharField(primary_key=True, db_column='idTransaccion', max_length=256, null=False)  # Field name made lowercase.
    fecha = models.CharField(max_length=256, null=False)
    valor = models.IntegerField(null=False)

    """def __str__(self):
        return (self.idtransaccion, self.fecha, self.valor)
    """

    class Meta:
        managed = False
        db_table = 'pagos'
        verbose_name_plural = 'Pagos'


class Pozoasociado(models.Model):
    idcasub = models.CharField(primary_key=True, db_column='idCasub', max_length=256, null=False)  # Field name made lowercase.
    coordenadaeste = models.TextField(db_column='coordenadaEste', null=False)  # Field name made lowercase. This field type is a guess.
    coordenadanorte = models.TextField(db_column='coordenadaNorte', null=False)  # Field name made lowercase. This field type is a guess.
    caudal = models.TextField(null=False)  # This field type is a guess.

    def __str__(self):
        return self.idcasub

    class Meta:
        managed = False
        db_table = 'pozoAsociado'
        verbose_name_plural = 'Pozos asociados'
