from django.utils import timezone
from datetime import datetime, time, timedelta

class TodaysDate:

    def __init__(self):
        ''' current time, month, year and midnight naive'''
        self.now = timezone.now() 
        self.month = self.now.month
        self.year = self.now.year
        self.midnight_naive = datetime.combine(self.now.date(), time(0,0))   
        # self.midnight_aware = timezone.make_aware(self.today_midnight)
        # self.local_time = timezone.localtime(self.midnight_aware)

    ''' 
        make_aware method that converts naive datetime 
        to become timezone aware
    '''
    def make_aware(self, date_naive):
        self.aware = timezone.make_aware(date_naive)
        return self.aware
    ''' 
        makes naive midnight time to become aware while
        calling make_aware
    '''
    def midnight_today_aware(self):
        self.today_midnight_aware = self.make_aware(self.midnight_naive)
        return self.today_midnight_aware

    '''
        localize for the local timezone
    '''
    def localize_time(self):
        return timezone.localtime(self.midnight_today_aware())


class OtherDateFilters(TodaysDate):   

    def yesterday(self):
        return self.localize_time() - timedelta(1)
    
    def monday(self):
        today = self.now.weekday()
        return self.localize_time() - timedelta(today)
    
    def monthStart(self):       
        firstday_aware = self.make_aware(datetime(self.year, self.month, 1))
        return firstday_aware

    def janFirst(self):
        janFirst_aware = self.make_aware(datetime(self.year, 1, 1))
        return janFirst_aware

