"""
Returns the booked for appointments for the current day, provided with a dict of all booked appointments.
"""

from datetime import datetime


def getClinicSchedule(existingAppointments):
    appointmentsToday = {}
    for appointment in existingAppointments:
        if existingAppointments[appointment]['day'] == datetime.today().date():
            appointmentsToday[appointment] = existingAppointments[appointment]

    if not appointmentsToday:
        return "No Appointments Today."
    else:
        return appointmentsToday


