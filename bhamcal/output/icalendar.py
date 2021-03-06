from collections import Counter

def iCalendar(events):
    codes = Counter()

    ical = '\r\n'.join([
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//University of Birmingham//Web timetables//EN'
    ])

    for event in events:
        uid_prefix = event.subject_code + '/' + event.event_type[:3].upper()
        codes[uid_prefix] += 1

        vevent = [
            "BEGIN:VEVENT",
            "UID:" + uid_prefix + str(codes[uid_prefix]),
            "SUMMARY:" + event.subject,
            "DTSTAMP:" + format_date(event.start),
            "DTSTART:" + format_date(event.start),
            "DTEND:" + format_date(event.end),
            "DESCRIPTION:" + event.description.replace('\n', r'\n'),
            "LOCATION:" + event.location,
            "END:VEVENT"
        ]
        vevent = '\r\n'.join(vevent)
        ical += '\r\n' + vevent

    ical += '\r\nEND:VCALENDAR'

    return ical

def format_date(date):
    return date.strftime("%Y%m%dT%H%M%SZ")
