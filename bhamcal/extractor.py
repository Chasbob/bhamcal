import re
from datetime import datetime

import pytz
from bs4 import BeautifulSoup

import spacy
import re

from .event import CalendarEvent

DEFAULT_TIMEZONE = pytz.timezone('Europe/London')

nlp = spacy.load("en_core_web_sm")
match = re.compile(r"PUNCT|NUM|SYM")

def extract(frame):
    soup = BeautifulSoup(frame, 'html.parser')
    spreadsheets = soup.find_all('table', class_='spreadsheet')

    for spreadsheet in spreadsheets:
        rows = spreadsheet.find_all('tr')[1:]
        for row in rows:
            yield extract_event(row)

def extract_event(table_row):
    entries = table_row.find_all('td')
    entries = [entry.string.strip() for entry in entries]

    # extract data from table
    day = entries[0]
    title = entries[1].strip()
    event_type = entries[2]
    start_time = entries[3]
    end_time = entries[4]
    location = entries[5]
    lecturer = entries[6]
    department = entries[7]

    # process subject title
    match = re.match("(.+)\((\d+)\)/", title)
    if match:
        name = match.group(1)
        code = match.group(2)
    else:
        match = re.match("(.+)/", title)
        if match:
            name = match.group(1)
            code = name.upper().replace(' ', '')
        else:
            name = title
            code = title.upper().replace(' ', '')

    name = clean_subject(title)

    # build description
    description = ""
    description += 'With: ' + lecturer + '\n'
    description += 'Activity: ' + title + '\n'
    description += 'Type: ' + event_type + '\n'
    description += 'Department: ' + department

    return CalendarEvent(
        start=extract_datetime(day, start_time),
        end=extract_datetime(day, end_time),
        subject=name,
        subject_code=code,
        event_type=event_type,
        location=location,
        description=description
    )

def extract_datetime(date, time):
    dt = datetime.strptime(date + " " + time, "%d %b %Y %H:%M")
    dt = DEFAULT_TIMEZONE.localize(dt)
    dt = dt.astimezone(pytz.utc)
    return dt

# Remove module codes, LM and/or LH and extended.
CODE_STRIPPER  = re.compile(
    r"(?P<code>\([0-9]+/[0-9]+\))|(?P<prefix>LM/LH|LH/LM|LH|LM|LI)|(?P<extended>\(Extended\)?)"
)
# Remove duplicates in the case of the name being present twice on some extended modules.
REMOVE_DOUBLES = re.compile(
    r"(?P<one>^.*/)"
)

def clean_subject(title: str) -> str:
    title = re.sub(r'\n', '', title)
    title = re.sub(r'(\(|\)|\/)', r' \1 ', title)
    doc = nlp(title)
    out = []
    for token in doc:
        if not(re.match(match, token.pos_)):
            if not(token.shape_.isupper()) and token.text != 'Extended' and token.text.strip() != '':
                out.append(token.text)
    # Check if the first 2 tokens are a subset of rest of the tokens
    if len(out) >= 4:
        if set(out[:2]).issubset(set(out[2:])):
            out = out[2:]
    # Else check if the first token is a subset of the rest of the tokens
    elif len(out) >= 2:
        if set(out[:1]).issubset(set(out[1:])):
            out = out[1:]
    return ' '.join(out)
