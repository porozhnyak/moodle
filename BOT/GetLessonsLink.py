
import datetime
import time
import LessonsLink 


# today = datetime.datetime.today().isoweekday()# Выводит номер дня недели (1-Понедельник ... 7-Воскресенье)
# TimeNow = datetime.datetime.today().strftime('%H:%M')


def GetLessonsLink(today, TimeNow):

    # today = 4
    # TimeNow = "02:36"
    # num = Lessons_lib.items()

    try:
        return LessonsLink.Lessons_lib[str(today)][TimeNow]
    except KeyError:
        pass

# print(GetLessonsLink(today, TimeNow))