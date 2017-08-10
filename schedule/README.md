# Algorithm Description

<ul>
    <li>Initially parse data and store information in objects</li>
    <li>For each request</li>
        <ul>
            <li>Get student availability information</li>
            <li>If student is available at the requested time</li>
                <ul>
                    <li>Get instructor availabity information</li>
                    <li>If Instructor sessions match and durations match</li>
                        <ul>
                            <li>Approve Request and add session information to particiant reserved sessions</li>
                        </ul>
                    <li>Else</li>
                        <ul>
                            <li>Log Instructor Not availabe conflict</li>
                        </ul>
                </ul>
            <li>Else</li>
                <ul>
                    <li>Log student not available conflict</li>
                </ul>
        </ul>

</ul>

# Development Environment

<ul>
    <li>Operating System : Windows 10</li>
    <li>Language : Python 3</li>
    <li>IDE : Sublime Text 3</li>
</ul>

# Requirements
<ul>
    <li>Python 3</li>
</ul>

# Folder Structure

* schedule
    *---src
        *---main.py
        *---test.py
        *---util.py
    * ---input.csv
    * ---instructor_availability.csv


# Execution Instructions

> cd schedule\src
if python 3 is default version
    > python test.py
else
    > python3 test.py

