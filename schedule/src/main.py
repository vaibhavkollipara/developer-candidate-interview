__author__ = 'Vaibhav Kollipara'
__doc__ = """
Contains all classes required to store parsed data and has conflicts check functionality
"""

from util import *
from abc import ABCMeta, abstractmethod


class InstructorAvailability:
    """
    Class to represent Instructor Availability Information
    """

    def __init__(self):
        # Used lists because an instructor may have multiple private and group lessons
        self.privateLessons = []
        self.groupLessons = []

    def add_private_lesson(self, session):
        self.privateLessons.append(session)

    def add_group_lesson(self, session):
        self.groupLessons.append(session)

    def tryAddRequest(self, request):
        # Checks for time and duration conflicts and try to add participant to session
        lessons = None
        if request.training_type == "Group Lesson":
            lessons = self.groupLessons
        elif request.training_type == "Private Lesson":
            lessons = self.privateLessons
        for lesson in lessons:
            if lesson.isAvailable(request.session) and lesson.isDurationMatching(request.duration):
                if not lesson.isFull():
                    lesson.addParticipant()
                    return True
        return False


class ParticipantAvailability:
    """
    Class to represent information reagarding student availability
    """

    def __init__(self):
        # reservedSlots has information of time the student is already comitted to
        self.reservedSlots = []

    def hasConflict(self, requestSession):
        # checks time conflict with reserved slots
        for session in self.reservedSlots:
            if not session.hasConflict(requestSession):
                return True
        return False

    def addSession(self, requestSession):
        # adds session to reserved slots
        self.reservedSlots.append(requestSession)


class Request():
    """
    Class to represent request information
    """

    def __init__(self, id, name, training_type, instructor, startDate, endDate, startTime, endTime):
        self.id = id
        self.name = name
        self.training_type = training_type
        self.instructor = instructor
        # use same base Session which makes easy calculate conflicts
        self.session = ParticipantSession(startDate, endDate, startTime, endTime)
        self.duration = getTimeDifferenceInMinutes(self.session.startTime, self.session.endTime)

    def __str__(self):
        return "{} : {}".format(self.student, self.instructor)

    def __repr__(self):
        return "{} : {}".format(self.student, self.instructor)


class Session():
    """
    Class to represent date and timings of Lesson
    """

    def __init__(self, startDate, endDate, startTime, endTime):
        self.startDate = getDateFromString(startDate)
        self.endDate = getDateFromString(endDate)
        self.startTime = getTimeFromString(startTime)
        self.endTime = getTimeFromString(endTime)

    def __str__(self):
        return "{} : {}".format(self.startDate, self.endDate)

    def __repr__(self):
        return "{} : {}".format(self.startDate, self.endDate)


class ParticipantSession(Session):
    """
    Class to represent Participant's registered lessons information
    """

    def __init__(self, startDate, endDate, startTime, endTime):
        super().__init__(startDate, endDate, startTime, endTime)

    def isDateConflicting(self, requestSession):
        if (requestSession.endDate < self.startDate) or (requestSession.startDate > self.endDate):
            return False

        return True

    def isTimeConflicting(self, requestSession):
        if (requestSession.startTime < self.startTime) or (requestSession.endTime > self.endTime):
            return False

        return True

    def hasConflict(self, requestSession):
        # checks time confilict with existing request session
        return self.isDateConflicting(requestSession) or self.isTimeConflicting(requestSession)


class InstuctorSession(Session, metaclass=ABCMeta):
    """
    Extended Session to represent additional information about maxParticipants, duration etc
    """

    def __init__(self, maxParticipants, startDate, endDate, startTime, endTime, duration):
        super().__init__(startDate, endDate, startTime, endTime)
        self.maxParticipants = maxParticipants
        (value, desc) = duration.split()
        self.duration = getDurationInMinutes(value, desc)
        self.participants_count = 0

    def isFull(self):
        # checks whether maximum capacity is reached in session
        return self.participants_count == self.maxParticipants

    @abstractmethod
    def isDurationMatching(self, requestDuration):
        pass

    def addParticipant(self):
        # add a new participant to session
        self.participants_count += 1

    def isAvailable(self, requestSession):
        return (requestSession.startDate >= self.startDate and requestSession.endDate <= self.endDate and requestSession.startTime >= self.startTime and requestSession.endTime <= self.endTime)


class PrivateSession(InstuctorSession):
    """
    Extended Instructor Session,
    Has additional functionality to check matching duration for Private Lesson
    """

    def __init__(self, maxParticipants, startDate, endDate, startTime, endTime, duration):
        super().__init__(maxParticipants, startDate, endDate, startTime, endTime, duration)

    def isDurationMatching(self, requestDuration):
        return requestDuration <= self.duration and int(self.duration % requestDuration) == 0

    def __str__(self):
        return "Private : [{} : {}]".format(self.startDate, self.endDate)

    def __repr__(self):
        return "Private : [{} : {}]".format(self.startDate, self.endDate)


class GroupSession(InstuctorSession):
    """
    Extended Instructor Session,
    Hass additional functionality to check matching duration for Group Lesson
    """

    def __init__(self, maxParticipants, startDate, endDate, startTime, endTime, duration):
        super().__init__(maxParticipants, startDate, endDate, startTime, endTime, duration)

    def isDurationMatching(self, requestDuration):
        return self.duration == requestDuration

    def __str__(self):
        return "Group : [{} : {}]".format(self.startDate, self.endDate)

    def __repr__(self):
        return "Group : [{} : {}]".format(self.startDate, self.endDate)
