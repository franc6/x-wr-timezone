"""This test converts example calendars"""
import pytest


def assert_has_line(bytes, content, message):
    lines = message_lines = [line for line in bytes.decode("UTF-8").splitlines() if content[0] in line]
    for c in content:
        lines = [line for line in lines if c in line]
    assert lines, message + " One of these lines should contain {}: {}".format(content, message_lines)


def test_input_to_output(to_standard, calendar_pair):
    """Test the calendars which are a pair of input and output."""
    output = to_standard(calendar_pair.input.as_icalendar())
    assert output == calendar_pair.output.as_icalendar(), calendar_pair.message


def test_output_stays_the_same(to_standard, output_calendar):
    assert output_calendar.is_corrected_output()
    output = to_standard(output_calendar.as_icalendar())
    assert output == output_calendar.as_icalendar(), "A calendar that was modified one should stay as it is."


def RDATE(dt):
    return ("rdate-hackerpublicradio.in.ics", ("RDATE", "TZID=Europe/London", dt), "RDATE is converted with value " + dt)


@pytest.mark.parametrize("calendar_name,content,message", [
# DTSTART;TZID=America/New_York:20211222T120000
# DTEND;TZID=America/New_York:20211222T130000
    ("single-events-DTSTART-DTEND.in.ics", ("DTSTART", "TZID=America/New_York", ":20211222T120000"), "DTSTART should be converted."),
    ("single-events-DTSTART-DTEND.in.ics", ("DTEND", "TZID=America/New_York", ":20211222T130000"), "DTEND should be converted."),
    ("single-events-DTSTART-DTEND.out.ics", ("DTSTART", "TZID=America/New_York", ":20211222T120000"), "DTSTART stays the same in already converted calendar."),
# DTSTART;TZID=America/New_York:20211222T210000
# DTEND;TZID=America/New_York:20211222T220000
    ("single-events-DTSTART-DTEND.in.ics", ("DTSTART", "TZID=America/New_York", ":20211222T210000"), "DTSTART should be converted."),
    ("single-events-DTSTART-DTEND.in.ics", ("DTEND", "TZID=America/New_York", ":20211222T220000"), "DTEND should be converted."),
    RDATE("20130803T190000"),
    RDATE("20130831T190000"),
    RDATE("20131005T190000"),
    RDATE("20131102T190000"),
    RDATE("20131130T190000"),
    RDATE("20140104T190000"),
    RDATE("20140201T190000"),
    RDATE("20140301T190000"),
    RDATE("20140405T190000"),
    RDATE("20140503T190000"),
    RDATE("20140531T190000"),
    RDATE("20140705T190000"),
])
def test_conversion_changes_the_time_zone(to_standard, calendars, calendar_name, content, message):
    calendar = calendars[calendar_name]
    new_calendar = to_standard(calendar.as_icalendar())
    output_bytes = new_calendar.to_ical()
    assert_has_line(output_bytes, content, message)
