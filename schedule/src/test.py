from main import *
import csv
from collections import defaultdict


class Process:

    def __init__(self, instructor_availability_file, requests_file):
        self.instructor_availability = self.__initlizeInstructorSchedules(instructor_availability_file)
        self.requests = self.__initilizeRequests(requests_file)
        self.participants_availability = {}

    def __initlizeInstructorSchedules(self, instructor_availability_file):
        instructor_availability = {}
        with open(instructor_availability_file) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                availability = None
                if row['Name'].upper() in instructor_availability.keys():
                    availability = instructor_availability[row['Name'].upper()]
                else:
                    availability = InstructorAvailability()
                    instructor_availability[row['Name'].upper()] = availability
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
        for k, v in self.instructor_availability.items():
            print(k)
            print(v.privateLessons)
            print(v.groupLessons)

        for request in self.requests:
            print(request)

    def schedule(self):
        for request in self.requests:
            if request.name in self.participants_availability.keys():
                participant_availability = self.participants_availability[request.name]
            else:
                participant_availability = ParticipantAvailability()
                self.participants_availability[request.name] = participant_availability

            if participant_availability.hasConflict(request.session):
                self.log("Student Not Available", request.id)
            else:
                instructor_availability = self.instructor_availability[request.instructor]
                if not instructor_availability.tryAddRequest(request):
                    self.log("Instructor Not Availabe",request.id)
                else:
                    participant_availability.addSession(request.session)


    def log(self,message,requestId):
        print("\nRequest Id : {}\nReason for Conflict : {}\n".format(requestId, message))


if __name__ == '__main__':
    p = Process('../instructor_availability.csv','../input.csv')
    p.schedule()


