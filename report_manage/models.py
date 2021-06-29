from django.db import models

# Create your models here.
from django.db.models import DO_NOTHING
from django.utils import timezone

from testing_manage.models import CustomUsers

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

    def to_dict(self):
        return {
            'fatal_exception': self.fatal_exception,
            'tombstone': self.tombstone,
            'vm_exitin': self.vm_exitin,
            'shutting_down_vm': self.shutting_down_vm,
            'activity_pause_timeout': self.activity_pause_timeout,
            'app_not_response': self.app_not_response,
            'null_pointer_exception': self.null_pointer_exception,
            'illegal_state_exception': self.illegal_state_exception,
            'format_exception': self.format_exception,
            'not_found_exception': self.not_found_exception,
            'init_before_start_services': self.init_before_start_services,
            'out_of_memory': self.out_of_memory,
            'anr_in': self.anr_in,
            'exit_zygote': self.exit_zygote,
            'sv_gpio_probe_start': self.sv_gpio_probe_start,
            'kernel_panic': self.kernel_panic,
            'kernel_bug': self.kernel_bug,
            'causing_watchdog_bite': self.causing_watchdog_bite,
            'waring': self.waring,
        }

    def sum(self):
        return self.fatal_exception + self.tombstone + self.vm_exitin + self.shutting_down_vm + \
               self.activity_pause_timeout + self.app_not_response + self.null_pointer_exception + \
               self.illegal_state_exception + self.format_exception + self.not_found_exception + \
               self.init_before_start_services + self.out_of_memory + self.anr_in + self.exit_zygote + self.kernel_bug + \
               self.kernel_panic + self.causing_watchdog_bite + self.waring


class CarInfoModel(models.Model):
    name = models.CharField('汽车名称', max_length=32, unique=True, null=False, blank=False, default='')
    code = models.CharField('汽车类型编码', max_length=16, unique=True, blank=False, null=False, default='')
    alias = models.CharField('汽车别名', max_length=32, unique=True, blank=True, null=True, default='')
    is_delete = models.BooleanField('是否删除', null=False, blank=False, default=False)

    class Meta:
        db_table = 'car_info'
        permissions = ()
        ordering = ['-id']

    def __str__(self):
        return self.name


class DevicePositionModel(models.Model):
    name = models.CharField('位置名称', max_length=32, unique=True, null=False, blank=False, default='')
    code = models.CharField('位置编码', max_length=16, unique=True, blank=False, null=False, default='')
    alias = models.CharField('位置别名', max_length=32, unique=True, blank=True, null=True, default='')
    is_delete = models.BooleanField('是否删除', null=False, blank=False, default=False)

    class Meta:
        db_table = 'device_position'
        permissions = ()
        ordering = ['-id']

    def __str__(self):
        return self.name


class CarDevicePositionModel(models.Model):
    position = models.ForeignKey(DevicePositionModel, on_delete=DO_NOTHING, null=False, blank=False, default=0)
    car = models.ForeignKey(CarInfoModel, on_delete=DO_NOTHING, null=False, blank=False, default=0)
    is_delete = models.BooleanField('是否删除', null=False, blank=False, default=False)

    class Meta:
        db_table = 'car_device_position'
        permissions = ()


class ModeInfoModel(models.Model):
    mode = models.CharField('编译方式', max_length=16, unique=True, null=False, blank=False, default='')
    code = models.CharField('编译方式编码', max_length=16, unique=True, blank=False, null=False, default='')
    alias = models.CharField('编译方式别名', max_length=32, unique=True, blank=True, null=True, default='')
    is_delete = models.BooleanField('是否删除', null=False, blank=False, default=False)

    class Meta:
        db_table = 'mode_info'
        permissions = ()
        ordering = ['-id']

    def __str__(self):
        return self.mode


class TestTypeInfoModel(models.Model):
    type = models.CharField('测试类型', max_length=32, unique=True, null=False, blank=False, default='')
    code = models.CharField('测试类型编码', max_length=16, unique=True, blank=False, null=False, default='')
    alias = models.CharField('测试类型别名', max_length=32, unique=True, blank=True, null=True, default='')
    is_delete = models.BooleanField('是否删除', null=False, blank=False, default=False)

    class Meta:
        db_table = 'test_type_info'
        permissions = ()
        ordering = ['-id']


class ErrorInfoModel(models.Model):
    """
    异常表
    """
    error_name = models.CharField('错误名称', max_length=128, null=False, blank=False, default='')
    is_delete = models.BooleanField('是否删除', null=False, blank=False, default=False)

    class Meta:
        db_table = 'error_info'
        permissions = ()
        ordering = ['-id']
        verbose_name = '异常类型管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.error_name


class ErrorLevelModel(models.Model):
    """
    异常等级表
    """
    level = models.IntegerField('异常级别', null=False, blank=False, unique=True, default=0)
    is_delete = models.BooleanField('是否删除', null=False, blank=False, default=False)

    class Meta:
        db_table = 'error_level'
        permissions = ()
        ordering = ['-level']
        verbose_name = '异常级别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'异常等级：{self.level}'


class ErrorNameLevelModel(models.Model):
    """
    异常等级
    """
    error_name = models.OneToOneField(ErrorInfoModel, unique=True, on_delete=DO_NOTHING, null=False, blank=False,
                                      default=0)
    level = models.ForeignKey(ErrorLevelModel, null=False, blank=False, on_delete=DO_NOTHING, default=0)
    is_delete = models.BooleanField('是否删除', null=False, blank=False, default=False)

    class Meta:
        db_table = 'error_name_level'
        permissions = ()
        ordering = ['level']
        verbose_name = '异常级别管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.error_name)


class TestVersionModel(models.Model):
    """
    测试版本
    """
    version = models.CharField('测试版本编号', max_length=255, null=False, blank=False, default='')
    code = models.CharField('唯一编号', max_length=128, unique=True, null=False, blank=False, default='')
    position = models.ForeignKey(DevicePositionModel, on_delete=DO_NOTHING, default=0)
    car = models.ForeignKey(CarInfoModel, on_delete=DO_NOTHING, default=0)
    mode = models.ForeignKey(ModeInfoModel, on_delete=DO_NOTHING, default=0)
    date = models.DateTimeField('日期', null=True)
    is_delete = models.BooleanField('是否删除', null=False, blank=False, default=False)

    class Meta:
        db_table = 'test_version'
        permissions = ()
        ordering = ['-id']

    def __str__(self):
        return self.code


class LevelErrorNumberModel(models.Model):
    """
    等级异常个数
    """
    error_level = models.ForeignKey(ErrorLevelModel, on_delete=DO_NOTHING, null=False, blank=False, default=1)
    number = models.IntegerField('异常数量', null=False, blank=False, default=0)
    test_version = models.ForeignKey(TestVersionModel, on_delete=DO_NOTHING, null=False, blank=False, default=0)
    is_delete = models.BooleanField('是否删除', null=False, blank=False, default=False)

    class Meta:
        db_table = 'error_level_number'
        permissions = ()
        ordering = ['-id']

    def to_dict(self):
        return {
            'error_level': self.error_level.level,
            'error_number': self.number,
            'test_version': self.test_version.code,
        }

    def to_test_version(self):
        return self.test_version.version

    def to_version_code(self):
        return self.test_version.code

    def to_level(self):
        return str(self.error_level.level)


class ReportOriginModel(models.Model):
    user = models.ForeignKey(CustomUsers, on_delete=DO_NOTHING, default=0)
    test_version = models.ForeignKey(TestVersionModel, on_delete=DO_NOTHING, default=0)
    test_type = models.ForeignKey(TestTypeInfoModel, on_delete=DO_NOTHING, default=0)
    device = models.CharField('设备编号', max_length=128, null=False, blank=False, default='')
    test_start_time = models.DateTimeField('测试开始时间')
    test_end_time = models.DateTimeField('测试结束时间')
    report_status = models.IntegerField('统计状态', choices=REPORT_STATUS, default=0)
    create_time = models.DateTimeField('记录创建时间', default=timezone.now)
    is_delete = models.BooleanField('是否删除', null=False, blank=False, default=False)

    class Meta:
        db_table = 'report_origin'


class ReportErrorOriginModel(AbsReportErrorModel):
    report_origin = models.ForeignKey(ReportOriginModel, on_delete=DO_NOTHING)
    # report_origin_id = models.IntegerField('reportOriginID', null=False, blank=False, default=0)
    is_delete = models.BooleanField('是否删除', null=False, blank=False, default=False)

    class Meta:
        db_table = 'report_error_origin'
        ordering = ['-id']
        permissions = ()


class ReportTotalModel(models.Model):
    test_version = models.ForeignKey(TestVersionModel, on_delete=DO_NOTHING, default=0)
    test_type = models.ForeignKey(TestTypeInfoModel, on_delete=DO_NOTHING, default=0)
    create_time = models.DateTimeField('记录创建时间', default=timezone.now)
    is_delete = models.BooleanField('是否删除', null=False, blank=False, default=False)

    class Meta:
        db_table = 'report_total'
        ordering = ['-create_time']
        permissions = ()


class ReportErrorTotalModel(AbsReportErrorModel):
    report_total = models.ForeignKey(ReportTotalModel, on_delete=DO_NOTHING, default=0)
    # report_total_id = models.IntegerField('reportDayID', null=False, blank=False, default=0)
    is_delete = models.BooleanField('是否删除', null=False, blank=False, default=False)

    class Meta:
        db_table = 'report_error_total'
        ordering = ['-id']
        permissions = ()
