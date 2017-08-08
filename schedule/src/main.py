from util import *
from abc import ABCMeta, abstractmethod


class Instructor:

    def __init__(self, name):
        self.name = name
        self.availability = Availability()

    def addGroupLesson(session):
        self.availability.add_group_lesson(session)

    def addPrivateLesson(session):
        self.availability.add_private_lesson(session)

    def getAvailability(self):
        return self.availability


class Availability:

    def __init__(self):
        self.privateLessons = []
        self.groupLessons = []

    def add_private_lesson(session):
        self.privateLessons.append(session)

    def add_group_lesson(session):
        self.groupLessons.append(session)


class Session(metaclass=ABCMeta):

    def __init__(self, maxParticipants, startDate, endDate, startTime, endTime, duration):
        self.maxParticipants = maxParticipants
        self.startDate = getDateFromString(startDate)
        self.endDate = getDateFromString(endDate)
        self.startTime = getTimeFromString(startTime)
        self.endTime = getTimeFromString(endTime)
        (value, desc) = duration.split()
        self.duration = getDurationInMinutes(value, desc)
        self.no_of_slots_a_day = int(getTimeDifferenceInMinutes(self.startTime, self.endTime) / self.duration)
        self.slots = []
        self.__createSlots()

    def __createSlots(self):
        total_days = (self.startDate - self.endDate).days
        for day in range(total_days + 1):
            dayDate = self.startDate + datetime.timedelta(days=day)
            startDateTime = datetime.datetime.combine(dayDate, self.startTime)
            for _ in range(no_of_slots_a_day):
                endDateTime = startDateTime + datetime.timedelta(minutes=duration)
                self.slots.append(Slot(startDateTime, endDateTime, self.maxParticipants))
                startDateTime = endDateTime

    @abstractmethod
    def addParticipant(self, participant):
        pass


class PrivateSession(Session):

    def __init__(self, maxParticipants, startDate, endDate, startTime, endTime, duration):
        super().__init__(maxParticipants, startDate, endDate, startTime, endTime, duration)

    def addParticipant(self, participant):
        print("Private Session Add Participant")


class GroupSession(Session):

    def __init__(self, maxParticipants, startDate, endDate, startTime, endTime, duration):
        super().__init__(maxParticipants, startDate, endDate, startTime, endTime, duration)

    def addParticipant(self, participant):
        print("Group Session Add Participant")


class Slot:

    def __init__(self, startDateTime, endDateTime, maxParticipants):
        self.startDateTime = startDateTime
        self.endDateTime = endDateTime
        self.maxParticipants = maxParticipants
        self.participants = []

    def __isFull():
        return self.participants.length == self.maxParticipants

    def addParticipant(participant):
        if not self.__isFull():
            self.participants.append(participant)
        else:
            raise CustomException("Slot Full")


class Participant:
    pass


class CustomException(Exception):
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)
