relative_dateranges
===================

Given a string such as today, next_week, previous_6_months, returns an inclusive daterange describing the requested time period.

e.g. if today's date is 18th March 2014, 'previous_week' will return 9th to 15th March inclusive, 'this_week' will return 16th through 22nd inclusive, 'next_week' will return 23rd through 29th inclusive.

Treats weeks as starting on Sunday and ending on Saturday, because Americans are odd.

Example usage:

	>>> from relative_dateranges import parse_relative_daterange
	>>> parse_relative_daterange('today')
	(datetime.date(2014, 3, 18), datetime.date(2014, 3, 18))
	>>> parse_relative_daterange('this_week')
	(datetime.date(2014, 3, 16), datetime.date(2014, 3, 22))
	>>> parse_relative_daterange('next_week')
	(datetime.date(2014, 3, 23), datetime.date(2014, 3, 29))
	>>> parse_relative_daterange('previous_week')
	(datetime.date(2014, 3, 9), datetime.date(2014, 3, 15))
	>>> parse_relative_daterange('next_2_months')
	(datetime.date(2014, 4, 1), datetime.date(2014, 5, 31))
	>>> parse_relative_daterange('previous_4_years')
	(datetime.date(2010, 1, 1), datetime.date(2013, 12, 31))
