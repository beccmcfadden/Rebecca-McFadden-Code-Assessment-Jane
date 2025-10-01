import unittest
from ClinicScheduler import ClinicSchedule
from GetClinicSchedule import getClinicSchedule
from datetime import datetime, date, time,timedelta
from freezegun import freeze_time


"""
Test Data 
"""

# appointments for today, tomorrow, and yesterday
existingAppointments = {'Patient1': {'day': date(2025,9,30),
                                     'startTime': datetime(2025,9,30,10),
                                     'endTime': datetime(2025,9,30,11)},
                        'Patient2': {'day': date(2025,10,1),
                                     'startTime': datetime(2025,10,1,11,30),
                                     'endTime': datetime(2025,10,1,13,0)},
                        'Patient3': {'day': date(2025,9,29), # test to make sure old appointments do not cause failures
                                     'startTime': datetime(2025,9,29,9,30),
                                     'endTime': datetime(2025,9,29,10,30)}
                        }


# removing the ability to choose a date in the past, equivalence class partitions = today and tomorrow
requestedDate1 = date(2025,9,30) # requested date must be datetime object, this is "now"
requestedDate2 = date(2025,10,1) # 1 day in future
requestedTime1 = datetime(2025,9,30,9)
requestedTime2 = datetime(2025,10,1,11,30) # unavailable
requestedTime3 = datetime(2025,10,1,14,30) # edge case for 2 hour rule



"""
get sched
"""


# testing the clinic schedule, get available appointments
class TestClinicScheduler(unittest.TestCase):
    ## Return Available Times testing
    @freeze_time('2025-09-30 09:00:00')
    def test_getAvailableAppointments_initialConsultation(self):
        schedule = ClinicSchedule(requestedDate1, "initialConsultation", existingAppointments)
        availableAppts = schedule.getAvailableAppointments()[1] # 1 returns a stringified datetime list
        self.assertEqual(availableAppts, ['11:00:00', '11:30:00', '12:00:00', '12:30:00', '13:00:00', '13:30:00', '14:00:00', '14:30:00', '15:00:00', '15:30:00'])

    @freeze_time('2025-09-30 10:00:00')
    def test_getAvailableAppointments_regularAppointment(self):
        schedule = ClinicSchedule(requestedDate2, "regularAppointment", existingAppointments)
        availableAppts = schedule.getAvailableAppointments()[1]
        self.assertEqual(availableAppts,['09:00:00', '09:30:00', '10:00:00', '10:30:00', '13:00:00', '13:30:00', '14:00:00', '14:30:00', '15:00:00', '15:30:00', '16:00:00'])

    @freeze_time('2025-09-30 11:00:00')
    def test_getAvailableAppointments_checkIn(self):
        schedule = ClinicSchedule(requestedDate2, "checkIn", existingAppointments)
        availableAppts = schedule.getAvailableAppointments()[1]
        self.assertEqual(availableAppts, ['09:00:00', '09:30:00', '10:00:00', '10:30:00', '11:00:00', '13:00:00', '13:30:00', '14:00:00', '14:30:00', '15:00:00', '15:30:00', '16:00:00', '16:30:00'])

    @freeze_time('2025-09-30 20:00:00')
    def test_today_outsideClinicHours(self):
        schedule = ClinicSchedule(requestedDate1, "initialConsultation", existingAppointments)
        availableAppts = schedule.getAvailableAppointments()[1]
        self.assertEqual(availableAppts, [])

    @freeze_time("2025-09-30 14:29:00")
    def test_today_edgeCase(self): # boundary value test case
        schedule = ClinicSchedule(requestedDate1, "checkIn", existingAppointments)
        availableAppts = schedule.getAvailableAppointments()[1]
        self.assertEqual(availableAppts, ['16:30:00'])


## Booking an appointment tests
## Testing 2 hour rule, and schedule conflict
## Ideally this would be more developed with edge cases
class TestClinicBooking(unittest.TestCase):

    @freeze_time("2025-09-30 6:30:00")
    def test_book_valid_today(self):
        schedule = ClinicSchedule(requestedDate1, "checkIn", existingAppointments)
        validBookingToday = schedule.bookAppointment(requestedTime1,"Valid Booking checkIn1")
        self.assertEqual(str(validBookingToday),"{'Patient1': {'day': datetime.date(2025, 9, 30), 'startTime': datetime.datetime(2025, 9, 30, 10, 0), 'endTime': datetime.datetime(2025, 9, 30, 11, 0)}, 'Patient2': {'day': datetime.date(2025, 10, 1), 'startTime': datetime.datetime(2025, 10, 1, 11, 30), 'endTime': datetime.datetime(2025, 10, 1, 13, 0)}, 'Patient3': {'day': datetime.date(2025, 9, 29), 'startTime': datetime.datetime(2025, 9, 29, 9, 30), 'endTime': datetime.datetime(2025, 9, 29, 10, 30)}, 'Valid Booking checkIn1': {'day': datetime.date(2025, 9, 30), 'startTime': datetime.datetime(2025, 9, 30, 9, 0), 'endTime': datetime.datetime(2025, 9, 30, 9, 30)}}")

    @freeze_time("2025-09-30 17:00:00")
    def test_book_invalid_today(self):
        schedule = ClinicSchedule(requestedDate1, "regularAppointment", existingAppointments)
        invalidBookingToday = schedule.bookAppointment(datetime.now(), "Invalid Booking initialConsultation")
        self.assertEqual(invalidBookingToday, "Requested Appointment Date and Time is unavailable.")

    @freeze_time("2025-09-30 14:00:00")
    def test_book_invalid_within2hours(self):
        schedule = ClinicSchedule(requestedDate1, "initialConsultation", existingAppointments)
        invalidBooking_within2hours = schedule.bookAppointment(datetime(2025,9,30,13,30),"Invalid Booking Within2Hours")
        self.assertEqual(invalidBooking_within2hours, "Requested Appointment Date and Time is unavailable.")


## Test Return today's appointments
## Ideally this would be more developed and would test before and after of adding new appointments
class TestReturnAppointments(unittest.TestCase):
    @freeze_time("2025-10-1 9:00:00")
    def test_get_known_appointments(self):
        todaySchedule = getClinicSchedule(existingAppointments)
        self.assertEqual(str(todaySchedule), "{'Patient2': {'day': datetime.date(2025, 10, 1), 'startTime': datetime.datetime(2025, 10, 1, 11, 30), 'endTime': datetime.datetime(2025, 10, 1, 13, 0)}}")



if __name__ == '__main__':
    unittest.main()
