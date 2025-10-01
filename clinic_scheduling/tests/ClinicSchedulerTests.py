import unittest
from ClinicScheduler import ClinicSchedule
from GetClinicSchedule import getClinicSchedule
from datetime import datetime, date, time,timedelta
from freezegun import freeze_time


"""
Test Data 
"""

# appointments for today, tomorrow, and yesterday
existingAppointments = {'Patient1': {'day': date.today(),
                                     'startTime': datetime.combine(date.today(), time(10)),
                                     'endTime': datetime.combine(date.today(), time(11))},
                        'Patient2': {'day': date.today() + timedelta(days=1),
                                     'startTime': datetime.combine(date.today() + timedelta(days=1), time(11,30)),
                                     'endTime': datetime.combine(date.today() + timedelta(days=1), time(13, 0))},
                        'Patient2': {'day': date.today() + timedelta(days=-1),
                                     'startTime': datetime.combine(date.today() + timedelta(days=-1), time(9,30)),
                                     'endTime': datetime.combine(date.today() + timedelta(days=-1), time(10,30))}
                        }


# removing the ability to choose a date in the past, equivalence class partitioning would be today and tomorrow
requestedDate1 = date.today() # requested date must be datetime object
requestedDate2 = date.today() + timedelta(days=1)
requestedTime1 = datetime.now().replace(minute=0,second=0,microsecond=0) + timedelta(hours=1) # within 2 hours
requestedTime2 = datetime.combine(date.today() + timedelta(days=1), time(11,30)) # unavailable
requestedTime3 = datetime.combine(date.today() + timedelta(days=1), time(14,30))






# schedule = ClinicSchedule(requestedDate, "initialConsultation", existingAppointments)
# print(schedule.getAvailableAppointments())

# requestedTime = datetime(2025,10,1,10)
# print(schedule.bookAppointment(requestedTime,"New Patient"))

# print(schedule.getBookedAppointments())


"""
get sched
"""
# print(getClinicSchedule(existingAppointments))
# schedule = ClinicSchedule(requestedDate1, "initialConsultation", existingAppointments)
# availableAppts = schedule.getAvailableAppointments()
# print(availableAppts)
# import sys
# sys.exit()


class TestClinicScheduler(unittest.TestCase):
    ## Return Available Times testing
    @freeze_time('09:00:00')
    def test_getAvailableAppointments_initialConsultation(self):
        schedule1 = ClinicSchedule(requestedDate1, "initialConsultation", existingAppointments)
        availableAppts = schedule1.getAvailableAppointments()
        self.assertEqual(str(availableAppts), "([datetime.time(11, 0), datetime.time(11, 30), datetime.time(12, 0), datetime.time(12, 30), datetime.time(13, 0), datetime.time(13, 30), datetime.time(14, 0), datetime.time(14, 30), datetime.time(15, 0), datetime.time(15, 30)], ['11:00:00', '11:30:00', '12:00:00', '12:30:00', '13:00:00', '13:30:00', '14:00:00', '14:30:00', '15:00:00', '15:30:00'])")

    @freeze_time('10:00:00')
    def test_getAvailableAppointments_regularAppointment(self):
        schedule2 = ClinicSchedule(requestedDate2, "regularAppointment", existingAppointments)
        availableAppts = schedule2.getAvailableAppointments()
        self.assertEqual(str(availableAppts), "([datetime.time(9, 0), datetime.time(9, 30), datetime.time(10, 0), datetime.time(10, 30), datetime.time(11, 0), datetime.time(11, 30), datetime.time(12, 0), datetime.time(12, 30), datetime.time(13, 0), datetime.time(13, 30), datetime.time(14, 0), datetime.time(14, 30), datetime.time(15, 0), datetime.time(15, 30), datetime.time(16, 0)], ['09:00:00', '09:30:00', '10:00:00', '10:30:00', '11:00:00', '11:30:00', '12:00:00', '12:30:00', '13:00:00', '13:30:00', '14:00:00', '14:30:00', '15:00:00', '15:30:00', '16:00:00'])")

    @freeze_time('11:00:00')
    def test_getAvailableAppointments_checkIn(self):
        schedule3 = ClinicSchedule(requestedDate2, "checkIn", existingAppointments)
        availableAppts = schedule3.getAvailableAppointments()
        self.assertEqual(str(availableAppts), "([datetime.time(9, 0), datetime.time(9, 30), datetime.time(10, 0), datetime.time(10, 30), datetime.time(11, 0), datetime.time(11, 30), datetime.time(12, 0), datetime.time(12, 30), datetime.time(13, 0), datetime.time(13, 30), datetime.time(14, 0), datetime.time(14, 30), datetime.time(15, 0), datetime.time(15, 30), datetime.time(16, 0), datetime.time(16, 30)], ['09:00:00', '09:30:00', '10:00:00', '10:30:00', '11:00:00', '11:30:00', '12:00:00', '12:30:00', '13:00:00', '13:30:00', '14:00:00', '14:30:00', '15:00:00', '15:30:00', '16:00:00', '16:30:00'])")

    @freeze_time('20:00:00')
    def test_today_outsideClinicHours(self):
        schedule4 = ClinicSchedule(requestedDate1, "initialConsultation", existingAppointments)
        availableAppts = schedule4.getAvailableAppointments()
        self.assertEqual(str(availableAppts),"([], [])")

    @freeze_time("14:29:00")
    def test_today_edgeCase(self): # boundary value test case
        schedule5 = ClinicSchedule(requestedDate1, "checkIn", existingAppointments)
        availableAppts = schedule5.getAvailableAppointments()
        self.assertEqual(str(availableAppts),"([datetime.time(16, 30)], ['16:30:00'])")


### Booking an appointment tests
class TestClinicBooking(unittest.TestCase):
    @freeze_time("06:30:00")
    def test_book_valid_today(self):
        schedule6 = ClinicSchedule(requestedDate1, "initialConsultation", existingAppointments)
        validBookingToday = schedule6.bookAppointment(requestedTime1,"Valid Booking initialConsultation1")
        self.assertEqual(str(validBookingToday),"{'Patient1': {'day': datetime.date(2025, 9, 30), 'startTime': datetime.datetime(2025, 9, 30, 10, 0), 'endTime': datetime.datetime(2025, 9, 30, 11, 0)}, 'Patient2': {'day': datetime.date(2025, 9, 29), 'startTime': datetime.datetime(2025, 9, 29, 9, 30), 'endTime': datetime.datetime(2025, 9, 29, 10, 30)}, 'Valid Booking initialConsultation1': {'day': datetime.date(2025, 9, 30), 'startTime': datetime.datetime(2025, 9, 30, 22, 0), 'endTime': datetime.datetime(2025, 9, 30, 23, 30)}}")

    @freeze_time("17:00:00")
    def test_book_invalid_today(self):
        schedule7 = ClinicSchedule(requestedDate1, "regularAppointment", existingAppointments)
        invalidBookingToday = schedule7.bookAppointment(datetime.now(), "Invalid Booking initialConsultation")
        self.assertEqual(invalidBookingToday, "Requested Appointment Date and Time is unavailable.")


## Return today's appointments
## Ideally this would be more developed and would test before and after of adding new appointments
class TestReturnAppointments(unittest.TestCase):
    def test_get_known_appointments(self):
        todaySchedule = getClinicSchedule(existingAppointments)
        self.assertEqual(str(todaySchedule), "{'Patient1': {'day': datetime.date(2025, 9, 30), 'startTime': datetime.datetime(2025, 9, 30, 10, 0), 'endTime': datetime.datetime(2025, 9, 30, 11, 0)}, 'Valid Booking initialConsultation1': {'day': datetime.date(2025, 9, 30), 'startTime': datetime.datetime(2025, 9, 30, 22, 0), 'endTime': datetime.datetime(2025, 9, 30, 23, 30)}}")



if __name__ == '__main__':
    unittest.main()
