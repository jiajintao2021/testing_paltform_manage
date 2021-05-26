from django.db import models

# Create your models here.
from django.utils import timezone

REPORT_TYPE_CHOICE = {
    (0, '未知'),
    (1, 'Monkey'),
}

REPORT_STATUS_CHOICE = {
    (0, '未知'),
    (1, '未统计'),
    (2, '已统计'),
}


class AbsReportModel(models.Model):
    user_id = models.IntegerField(
        '用户id', null=False, blank=False, default=0, help_text='默认0， admin代表未知')
    is_active = models.BooleanField('是否有效', default=True, help_text='是否有效')
    status = models.IntegerField(
        '状态', choices=REPORT_STATUS_CHOICE, default=0, help_text='统计状态')
    code = models.CharField('保留字段', max_length=32, null=False, default='', help_text='保留字段')
    type = models.IntegerField('报告类型', choices=REPORT_TYPE_CHOICE, default=0)
    create_time = models.DateTimeField('创建时间', default=timezone.now, help_text='落库时间，不是统计时间')

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


class LatestReportModel(AbsReportModel):
    class Meta:
        db_table = 'latest_report'
        permissions = ()
        ordering = ['-create_time']
        verbose_name = '最新的报告'
        verbose_name_plural = verbose_name


class YearReportModel(AbsReportModel):

    class Meta:
        db_table = 'year_report'
        permissions = ()
        ordering = ['-create_time']
        verbose_name = '年报告'
        verbose_name_plural = verbose_name


class MonthReportModel(AbsReportModel):

    class Meta:
        db_table = 'month_report'
        permissions = ()
        ordering = ['-create_time']
        verbose_name = '月报告'
        verbose_name_plural = verbose_name


class DayReportModel(AbsReportModel):

    class Meta:
        db_table = 'day_report'
        permissions = ()
        ordering = ['-create_time']
        verbose_name = '日报告'
        verbose_name_plural = verbose_name
