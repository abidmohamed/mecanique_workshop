from .models import Rdv
from datetime import datetime, timedelta
from calendar import HTMLCalendar


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, rdvs):
        rdvs_per_day = rdvs.filter(rdv_date__day=day)
        d = '<ul class="list-group">'

        for rdv in rdvs_per_day:
            d += f'<li class="list-group-item list-group-item-success"> {rdv.get_absolute_url()}_{rdv.rdv_time} </li>'
        d += '</ul>'
        if day != 0:
            return f"<td class=''><span class='date'>{day}</span><ul class='list-group'> {d} </ul></td>"
        return '<td class="text-dark"></td>'

    # formats a week as a tr
    def formatweek(self, theweek, rdvs):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, rdvs)
        return f'<tr class="text-dark"> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        events = Rdv.objects.filter(rdv_date__year=self.year, rdv_date__month=self.month)

        cal = f'<br><table border="0" cellpadding="0" cellspacing="0" class="calendar text-dark">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'

        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        cal += f'</table>\n'
        return cal
