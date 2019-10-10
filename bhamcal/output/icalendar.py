from collections import Counter


def iCalendar(filename, events, recur):
    codes = Counter()
    counts = Counter(events)
    if recur:
        events = list(set(events))
    with open(filename, 'w') as output:
        header = [
            'BEGIN:VCALENDAR',
            'VERSION:2.0',
            'PRODID:-//University of Birmingham//Web timetables//EN'
        ]
        output.write('\r\n'.join(header) + '\r\n')

        for event in events:
            uid_prefix = event.subject_code + '/' + event.event_type[:3].upper()
            codes[uid_prefix] += 1
            if recur:
                recurrence = "RRULE:FREQ=WEEKLY;BYDAY=" + str(event.start.strftime("%a")).upper()[:2] + ";COUNT=" + str(
                    counts[event])
            else:
                recurrence = ""
            vevent = [
                "BEGIN:VEVENT",
                "UID:" + uid_prefix + str(codes[uid_prefix]),
                "SUMMARY:" + event.subject,
                "DTSTAMP:" + format_date(event.start),
                "DTSTART:" + format_date(event.start),
                "DTEND:" + format_date(event.end),
                "DESCRIPTION:" + event.description.replace('\n', r'\n'),
                "LOCATION:" + event.location,
                recurrence,
                "END:VEVENT"
            ]
            output.write('\r\n'.join(vevent) + '\r\n')

        output.write('END:VCALENDAR')

def format_date(date):
    return date.strftime("%Y%m%dT%H%M%SZ")
