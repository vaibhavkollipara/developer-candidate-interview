from util import *


class InstructorAvailability:
    """
    Class to maintain Instructor Availability Information
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
            if not lesson.hasTimeConflict(request.session) and not lesson.hasDurationConflict(request.duration):
                if not lesson.isFull():
                    lesson.addParticipant()
                    return True
        return False


class Session():
    """
        Class to maintain date and timings of session
    """

    def __init__(self, startDate, endDate, startTime, endTime):
        self.startDate = getDateFromString(startDate)
        self.endDate = getDateFromString(endDate)
        self.startTime = getTimeFromString(startTime)
        self.endTime = getTimeFromString(endTime)

    def hasTimeConflict(self, requestSession):
        # checks date time conflict with given session
        pass
        """
            Todo
        """

    def __str(self):
        return "{} : {}".format(self.startDate, self.endDate)


class InstuctorSession(Session):
    """
        Extends from Session
        Has an additional information about maxParticipants and duration
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

    def hasDurationConflict(self):
        pass

    def addParticipant(self):
        # add a new participant to session
        self.participants_count += 1


class PrivateSession(InstuctorSession):
    """
        Has own method for checking duration conflicts
    """

    def __init__(self, maxParticipants, startDate, endDate, startTime, endTime, duration):
        super().__init__(maxParticipants, startDate, endDate, startTime, endTime, duration)

    def hasDurationConflict(self, requestDuration):
        # checks duration conflict
        return (requestDuration % self.duration) != 0

    def __str__(self):
        return "Private : [{} : {}]".format(self.startDate, self.endDate)

    def __repr__(self):
        return "Private : [{} : {}]".format(self.startDate, self.endDate)


class GroupSession(InstuctorSession):
    """
        Has own method for checking duration conflicts
    """

    def __init__(self, maxParticipants, startDate, endDate, startTime, endTime, duration):
        super().__init__(maxParticipants, startDate, endDate, startTime, endTime, duration)

    def hasDurationConflict(self, requestDuration):
        # checks duration conflict
        return requestDuration != self.duration

    def __str__(self):
        return "Group : [{} : {}]".format(self.startDate, self.endDate)

    def __repr__(self):
        return "Group : [{} : {}]".format(self.startDate, self.endDate)


class ParticipantAvailability:
    """
        Class to maintain information reagarding student availability
    """

    def __init__(self):
        # reservedSlots has information of time the student is already comitted to
        self.reservedSlots = []

    def hasConflict(self, requestSession):
        # checks time conflict with reserved slots
        for session in self.reservedSlots:
            if session.hasTimeConflict(requestSession):
                return True
        return False

    def addSession(self, session):
        # adds session to reserved slots
        self.reservedSlots.append(session)


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
        self.session = Session(startDate, endDate, startTime, endTime)
        self.duration = getTimeDifferenceInMinutes(self.session.startTime, self.session.endTime)

    def __str__(self):
        return "{} : {}".format(self.student, self.instructor)
