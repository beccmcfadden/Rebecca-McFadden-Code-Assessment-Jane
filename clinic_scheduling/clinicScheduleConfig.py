"""
Configuration items specific to a clinic
"""
from datetime import time, timedelta

#Opening Hours
clinicOpen = time(9)
clinicClose = time(17)


#function to store appointment types & durations, translate appointment type to duration
def getAppointmentDuration(appointmentType):
    appointmentDurations = {"initialConsultation": timedelta(minutes=90),
                            "regularAppointment": timedelta(minutes = 60),
                            "checkIn": timedelta(minutes=30)}
    #assuming appointment type would be hardcoded/unable to enter invalid type on UI
    return appointmentDurations[appointmentType]


# Appointment Increments
appointmentIncrements = 30
