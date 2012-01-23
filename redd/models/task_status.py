#!/usr/bin/env python

from celery import states
from django.db import models
from djcelery.models import TASK_STATE_CHOICES

from redd.models import User

class TaskStatus(models.Model):
    """
    An object to track the status of a Celery task, as the
    data available in AsyncResult is not sufficient.
    """
    task_name = models.CharField(max_length=255,
        help_text='Identifying name for this task.')
    status = models.CharField(max_length=50, default=states.PENDING, choices=TASK_STATE_CHOICES,
        help_text='Current state of this task.')
    message = models.CharField(max_length=255, blank=True,
        help_text='A human-readable message indicating the progress of this task.')
    start = models.DateTimeField(null=True,
        help_text='Date and time that this task began processing.')
    end = models.DateTimeField(null=True,
        help_text='Date and time that this task ceased processing (either complete or failed).')
    traceback = models.TextField(blank=True, null=True, default=None,
        help_text='Traceback that exited this task, if it failed.')
    creator = models.ForeignKey(User, null=True, related_name='tasks',
        help_text='The user who initiated this task.')

    class Meta:
        app_label = 'redd'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __unicode__(self):
        return self.task_name

