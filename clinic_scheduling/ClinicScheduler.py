from datetime import datetime, timedelta, time, date
from clinicScheduleConfig import clinicOpen, clinicClose, getAppointmentDuration, appointmentIncrements

"""
Scheduling application for a physiotherapy clinic 

Schedule functions: 
- Provide the patient with a list of available appointment times. 
  Inputs are the appointment type and a date, either today or in the future. 
  The 2 hour booking deadline applies for today’s appointments.
- Allow the patient to book an appointment.
- Provide the practitioner with a list of scheduled appointments for the current day.
"""




"""

Booked appointments and existing appointments dictionary format: 

existingAppointments = {appt1: {'day': day,
                                'startTime': startTime,
                                'endTime': endTime,
                                'patientName': patientName}
                        appt2: {'day': day,
                                'startTime': startTime,
                                'endTime': endTime,
                                'patientName': patientName}
                        }
"""

# to interact with the clinic schedule, a date, appointment type, and existing appointment data must be passed
class ClinicSchedule:
    def __init__(self, appointmentDate, appointmentType, existingAppointments): # patient inputs
        self.appointmentDate = appointmentDate
        self.appointmentType = appointmentType
        self.duration = getAppointmentDuration(self.appointmentType)
        self.existingAppointments = existingAppointments
        # clinic hours hardcoded
        # self.clinicOpen = time(9)
        # self.clinicClose = time(17)

    # function to check for conflicts for requesting available appointment times and booking,
    # so requesting available appointment times and booking can be used without each other
    def checkForConflicts(self, startingTime):

        conflict = False  # initialize as no conflicts, change flag to True if conflict found for this slot

        # get ending time for the slot we are currently looking at
        slotEndTime = startingTime + self.duration

        # check appointments do not overlap, existing appts stored as dict
        for bookedAppt in self.existingAppointments:
            # ignore if requested and booked appt have different days
            if self.existingAppointments[bookedAppt]['day'] != self.appointmentDate:
                continue
            # check if the intervals overlap
            if not (startingTime >= self.existingAppointments[bookedAppt]['endTime'] or slotEndTime <=
                    self.existingAppointments[bookedAppt]['startTime']):
                # if not (slotEndTime <= self.existingAppointments[bookedAppt]['startTime'] or startingTime >= self.existingAppointments[bookedAppt]['endTime']):
                conflict = True

        # check if appointment is within 2 hour cutoff time for day-of only
        if self.appointmentDate == date.today() and startingTime < datetime.now() + timedelta(hours=2):
            conflict = True
        if conflict == False:  # if none of the constraints have been hit, this is a valid timeslot
            return startingTime.time()
        else:
            return False


    ### list available appointments based on a date, appointment type, and existing appointments
    def getAvailableAppointments(self): #return all available appointment times, given date and appointment type

        #initialize list of appts to return
        availableAppointments = []

        # #starting/ending time and date
        startingTime = datetime.combine(self.appointmentDate, clinicOpen)
        endingTime = datetime.combine(self.appointmentDate, clinicClose)

        # # for a given day & appt type, iterate through each potential slot and add to available times if no rules are broken
        while startingTime + self.duration <= endingTime:
            isSlotAvailable = self.checkForConflicts(startingTime) #returns time if no conflicts, false if conflict
            if isSlotAvailable:
                availableAppointments.append(isSlotAvailable)

            # Appointments must start on the hour or half hour
            startingTime += timedelta(minutes = appointmentIncrements)

        formattedAvailableAppointments = [str(i) for i in availableAppointments]
        return availableAppointments, formattedAvailableAppointments


    ### Book appointment
    def bookAppointment(self, requestedTime, patientName):
        # check for conflicts
        if self.checkForConflicts(requestedTime): # if no conflict, add to schedule
            self.existingAppointments[patientName] = {'day':self.appointmentDate,
                                                 'startTime': requestedTime,
                                                 'endTime': requestedTime + self.duration
                                                 }
            return self.existingAppointments
        else: # do not add requested appointment to schedule, return error message
            return "Requested Appointment Date and Time is unavailable."



