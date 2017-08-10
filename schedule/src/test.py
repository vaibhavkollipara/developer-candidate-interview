__author__ = 'Vaibhav Kollipara'
__doc__ = """
A Scheduler which takes instructor availabilities and lesson requests data and try to schedule them and detect conflicts
"""

from main import *
import csv


class Scheduler:

    def __init__(self, instructor_availability_file, requests_file):
        # Takes input files as parameters

        # dict makes the search and fetch easy
        self.instructor_availability = self.__initlizeInstructorSchedules(instructor_availability_file)
        self.requests = self.__initilizeRequests(requests_file)
        self.participants_availability = {} # dict makes the search and fetch easy

    def __initlizeInstructorSchedules(self, instructor_availability_file):
        # parse instructor availability file
        instructor_availability = {}
        with open(instructor_availability_file) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:

                if not row['Name'].upper() in instructor_availability.keys():
                    instructor_availability[row['Name'].upper()] = InstructorAvailability()

                availability = instructor_availability[row['Name'].upper()]

                if row['Training Type'] == 'Group Lesson':
                    availability.add_group_lesson(GroupSession(
                                                                row['Max Participants'],
                                                                row['Start Date'],
                                                                row['End Date'],
                                                                row['Start Time'][:8],
                                                                row['End Time'][:8],
                                                                row['Duration']
                                                            ))
                elif row['Training Type'] == 'Private Lesson':
                    availability.add_private_lesson(PrivateSession(
                                                                row['Max Participants'],
                                                                row['Start Date'],
                                                                row['End Date'],
                                                                row['Start Time'][:8],
                                                                row['End Time'][:8],
                                                                row['Duration']
                                                            ))

        return instructor_availability

    def __initilizeRequests(self, requests_file):
        # parse request file
        requests = []
        with open(requests_file) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                requests.append(Request(
                                            row['Request ID'],
                                            row['Name'].upper(),
                                            row['Training Type'],
                                            row['With'].upper(),
                                            row['Start Date'],
                                            row['End Date'],
                                            row['Start Time'][:8],
                                            row['End Time'][:8],
                                ))
        return requests

    def display(self):
        # displays the parsed content
        for k, v in self.instructor_availability.items():
            print(k)
            print(v.privateLessons)
            print(v.groupLessons)

        for request in self.requests:
            print(request)

    def schedule(self):
        for request in self.requests:

            if request.name not in self.participants_availability.keys():
                self.participants_availability[request.name] = ParticipantAvailability()

            participant_availability = self.participants_availability[request.name]

            if participant_availability.hasConflict(request.session):
                self.log("Student Not Available", request.id)
            else:
                instructor_availability = self.instructor_availability.get(request.instructor,None)
                if not instructor_availability:
                    self.log("Invalid Instructor",request.id)
                    continue
                if not instructor_availability.tryAddRequest(request):
                    self.log("Instructor Not Available",request.id)
                else:
                    participant_availability.addSession(request.session)
                    # print("{} : Approved".format(request.id))


    def log(self,message,requestId):
        print("\nRequest Id : {}\nReason for Conflict : {}\n".format(requestId, message))


if __name__ == '__main__':
    s = Scheduler('../instructor_availability.csv','../input.csv')
    # display
    s.schedule()


