# -*- coding: utf-8 -*-
from django.db import models

class LivehouseRecord(models.Model):
    eventid = models.CharField(max_length=100, primary_key=True)
    datetime = models.DateField()
    ticket = models.IntegerField(max_length=10)
    ticketincome = models.IntegerField(max_length=10)
    barincome = models.IntegerField(max_length=10)
    checkincome = models.IntegerField(max_length=10)
    rentincome = models.IntegerField(max_length=10)
    otherincome = models.IntegerField(max_length=10)
    totalincome = models.IntegerField(max_length=10)

    EventTypeChoices = (
        ('mao', 'MAO安排'),
        ('siterent', '场地出租'),
        ('host', '主办方安排'),
        ('maoandhost', 'MAO&主办方一起'),
        ('other', '其他'),
    )
    eventtype = models.CharField(max_length=100, choices=EventTypeChoices)

    class Meta:
        db_table = "LivehouseRecordTable"

    def __unicode__(self):
        return self.eventid, self.eventtype
