# -*- coding: utf-8 -*-
from django.db import models

class PogoLog(models.Model):
    eventid = models.CharField(max_length=100)
    songid = models.CharField(max_length=100)
    songname = models.CharField(max_length=100)
    singerid = models.CharField(max_length=100)
    timestamp = models.DateTimeField(max_length=100)
    pogonum = models.IntegerField(max_length=10)

    class Meta:
        db_table = "PogoLogTable"

    def __unicode__(self):
        return self.eventid, self.songname