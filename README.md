Clinic Scheduling Application

1. Clone the repo:
    git clone https://github.com/beccmcfadden/Rebecca-McFadden-Code-Assessment-Jane.git
    cd clinic-scheduler
2. Install Dependencies:
   pip install -r requirements.txt
4. To Run Tests:
   python -m unittest tests/ClinicSchedulerTests.py

Assumptions:
- Data storage: Existing appointments to be stored as a dict
- Invalid parameters/inputs:
    - Unable to enter an incorrect appointment type
    - Unable to enter appointment time in the past
- No limit on how far in the future appointments can be scheduled
- Not accounting for multiple timezones: keeping datetime default, my PC is in EST
- Using freezegun for time-sensitive testing

Files:

- config.py for all hardcoded values for clinic:
    - Opening Hours
    - Appointment types & durations
    - Appointment increments/allowed start times

- ClinicScheduler.py
    - Handles the user requesting availabe appontments for a specific day
    - Handles user requesting to book an appointment

- GetClinicSchedule.py
    - Returns the list of the current day's appointments


