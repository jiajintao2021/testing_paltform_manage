from django.db import models

# Create your models here.
from django.utils import timezone

REPORT_STATUS = (
    (0, '未知'),
    (1, '未统计'),
    (2, '已统计'),
)


class AbsReportErrorModel(models.Model):
    """
    错误基类
    """
    fatal_exception = models.IntegerField('FATAL EXCEPTION', null=False, blank=False, default=0)
    tombstone = models.IntegerField('Tombstone', null=False, blank=False, default=0)
    vm_exitin = models.IntegerField('Tombstone', null=False, blank=False, default=0)
    shutting_down_vm = models.IntegerField('Shutting down VM', null=False, blank=False, default=0)
    activity_pause_timeout = models.IntegerField(
        'Activity pause timeout', null=False, blank=False, default=0, help_text='Activity pause timeout')
    app_not_response = models.IntegerField(
        'Application is not responding', null=False, blank=False, default=0, help_text='Application is not responding')
    null_pointer_exception = models.IntegerField(
        'NullPointerException', null=False, blank=False, default=0, help_text='NullPointerException'
    )
    illegal_state_exception = models.IntegerField(
        'IllegalStateException', null=False, blank=False, default=0, help_text='IllegalStateException'
    )
    format_exception = models.IntegerField(
        'FormatException', null=False, blank=False, default=0, help_text='FormatException'
    )
    not_found_exception = models.IntegerField(
        'NotFoundException', null=False, blank=False, default=0, help_text='NotFoundException'
    )
    init_before_start_services = models.IntegerField(
        'InitBeforeStartServices', null=False, blank=False, default=0, help_text='InitBeforeStartServices'
    )
    out_of_memory = models.IntegerField(
        'outOfMemory', null=False, blank=False, default=0, help_text='outOfMemory'
    )
    anr_in = models.IntegerField(
        'ANR in', null=False, blank=False, default=0, help_text='ANR in'
    )
    exit_zygote = models.IntegerField(
        'Exit zygote', null=False, blank=False, default=0, help_text='Exit zygote'
    )
    sv_gpio_probe_start = models.IntegerField(
        'sv_gpio_probe start', null=False, blank=False, default=0, help_text='sv_gpio_probe start'
    )
    kernel_panic = models.IntegerField(
        'Kernel panic', null=False, blank=False, default=0, help_text='Kernel panic'
    )
    kernel_bug = models.IntegerField(
        'kernel BUG at', null=False, blank=False, default=0, help_text='kernel BUG at'
    )
    causing_watchdog_bite = models.IntegerField(
        'Causing a watchdog bite', null=False, blank=False, default=0, help_text='Causing a watchdog bite'
    )
    waring = models.IntegerField(
        'WARNING', null=False, blank=False, default=0, help_text='WARNING'
    )

    class Meta:
        abstract = True


class CarInfoModel(models.Model):
    name = models.CharField('汽车名称', max_length=32, unique=True, null=False, blank=False, default='')
    code = models.CharField('汽车类型编码', max_length=16, unique=True, blank=False, null=False, default='')
    alias = models.CharField('汽车别名', max_length=32, unique=True, blank=True, null=True, default='')

    class Meta:
        db_table = 'car_info'
        permissions = ()
        ordering = ['-id']


class DevicePositionModel(models.Model):
    name = models.CharField('位置名称', max_length=32, unique=True, null=False, blank=False, default='')
    code = models.CharField('位置编码', max_length=16, unique=True, blank=False, null=False, default='')
    alias = models.CharField('位置别名', max_length=32, unique=True, blank=True, null=True, default='')

    class Meta:
        db_table = 'device_position'
        permissions = ()
        ordering = ['-id']


class ModeInfoModel(models.Model):
    mode = models.CharField('编译方式', max_length=16, unique=True, null=False, blank=False, default='')
    code = models.CharField('编译方式编码', max_length=16, unique=True, blank=False, null=False, default='')
    alias = models.CharField('编译方式别名', max_length=32, unique=True, blank=True, null=True, default='')

    class Meta:
        db_table = 'mode_info'
        permissions = ()
        ordering = ['-id']


class TestTypeInfo(models.Model):
    type = models.CharField('测试类型', max_length=32, unique=True, null=False, blank=False, default='')
    code = models.CharField('测试类型编码', max_length=16, unique=True, blank=False, null=False, default='')
    alias = models.CharField('测试类型别名', max_length=32, unique=True, blank=True, null=True, default='')

    class Meta:
        db_table = 'test_type_info'
        permissions = ()
        ordering = ['-id']


class TestVersionModel(models.Model):
    """
    测试版本
    """
    version = models.CharField('测试版本编号', max_length=255, null=False, blank=False, default='')
    code = models.CharField('唯一编号', max_length=128, unique=True, null=False, blank=False, default='')
    position_id = models.IntegerField('设备类型', null=False, blank=False, default=0)
    car_id = models.IntegerField('汽车类型', null=False, blank=False, default=0)
    mode_id = models.IntegerField('编译模式', null=False, blank=False, default=0)
    date = models.DateTimeField('日期', null=True)

    class Meta:
        db_table = 'test_version'
        permissions = ()
        ordering = ['-id']


class ReportOriginModel(models.Model):
    user_id = models.IntegerField('用户ID', null=False, blank=False, default=0)
    test_version_id = models.IntegerField('测试版本ID', null=False, blank=False, default=0)
    test_type_id = models.IntegerField('测试类型ID', null=False, blank=False, default=0)
    device = models.CharField('设备编号', max_length=128, null=False, blank=False, default='')
    test_start_time = models.DateTimeField('测试开始时间')
    test_end_time = models.DateTimeField('测试结束时间')
    report_status = models.IntegerField('统计状态', choices=REPORT_STATUS, default=0)
    create_time = models.DateTimeField('记录创建时间', default=timezone.now)

    class Meta:
        db_table = 'report_origin'


class ReportErrorOriginModel(AbsReportErrorModel):
    report_origin_id = models.IntegerField('reportOriginID', null=False, blank=False, default=0)

    class Meta:
        db_table = 'report_error_origin'
        ordering = ['-id']
        permissions = ()


class ReportErrorTotalModel(AbsReportErrorModel):
    report_total_id = models.IntegerField('reportDayID', null=False, blank=False, default=0)

    class Meta:
        db_table = 'report_error_total'
        ordering = ['-id']
        permissions = ()


class ReportTotalModel(models.Model):
    test_version_id = models.IntegerField('测试版本ID', null=False, blank=False, default=0)
    test_type_id = models.IntegerField('测试类型ID', null=False, blank=False, default=0)
    create_time = models.DateTimeField('记录创建时间', default=timezone.now)

    class Meta:
        db_table = 'report_total'
        ordering = ['-id']
        permissions = ()
