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
        managed = True
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BaseAllstopswithroute(models.Model):
    stop_sequence = models.CharField(max_length=10, blank=True, null=True)
    route_number = models.ForeignKey('BaseRoutes', models.DO_NOTHING, blank=True, null=True)
    stop = models.ForeignKey('BaseStops', models.DO_NOTHING, blank=True, null=True)
    stop_headsign = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'base_allstopswithroute'


class BaseCurrentweather(models.Model):
    dt = models.CharField(primary_key=True, max_length=45)
    temp = models.CharField(max_length=10, null=True)
    feels_like = models.CharField(max_length=45, blank=True, null=True)
    temp_min = models.CharField(max_length=45, blank=True, null=True)
    temp_max = models.CharField(max_length=45, blank=True, null=True)
    pressure = models.CharField(max_length=45, blank=True, null=True)
    humidity = models.CharField(max_length=45, blank=True, null=True)
    wind_speed = models.CharField(max_length=45, blank=True, null=True)
    wind_deg = models.CharField(max_length=45, blank=True, null=True)
    clouds_all = models.CharField(max_length=45, blank=True, null=True)
    weather_main = models.CharField(max_length=45, blank=True, null=True)
    weather_description = models.CharField(max_length=45, blank=True, null=True)
    weather_icon = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'base_currentweather'


class BaseForecastweather(models.Model):
    dt = models.CharField(primary_key=True, max_length=45)
    dt_iso = models.CharField(max_length=45, blank=True, null=True)
    temp = models.CharField(max_length=45, blank=True, null=True)
    temp_min = models.CharField(max_length=45, blank=True, null=True)
    temp_max = models.CharField(max_length=45, blank=True, null=True)
    pressure = models.CharField(max_length=45, blank=True, null=True)
    humidity = models.CharField(max_length=45, blank=True, null=True)
    wind_speed = models.CharField(max_length=45, blank=True, null=True)
    wind_deg = models.CharField(max_length=45, blank=True, null=True)
    clouds_all = models.CharField(max_length=45, blank=True, null=True)
    weather_id = models.CharField(max_length=45, blank=True, null=True)
    weather_main = models.CharField(max_length=45, blank=True, null=True)
    weather_description = models.CharField(max_length=45, blank=True, null=True)
    weather_icon = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'base_forecastweather'


class BaseRoutes(models.Model):
    route_id = models.CharField(primary_key=True, max_length=20)
    route_name = models.CharField(max_length=45, blank=True, null=True)
    route_description = models.CharField(max_length=45, blank=True, null=True)
    route_direction = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'base_routes'


class BaseStops(models.Model):
    stop_id = models.CharField(primary_key=True, max_length=20)
    stop_name = models.CharField(max_length=45, blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    stop_number = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'base_stops'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'django_session'
