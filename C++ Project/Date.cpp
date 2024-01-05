/*
*****************************************************************************
File : Date.cpp
Full Name  : Harnoor Kaur Dran
Email : hkdran@outlook.com
*****************************************************************************
*/
#include <iomanip>
#include "Date.h"

namespace sdds {
	bool Date::validDate() {
		int maxDay = ut.daysOfMon(month, year);
		bool valid{ true };

		if (year<CURRENT_YEAR || year> MAX_YEAR)
		{
			m_state = "Invalid year in date";
			m_state.setStatus(1);
			valid = false;
		}
		if (month <= INVALID_DATE || month >= MONTH_THIRTEEN)
		{
			m_state = "Invalid month in date";
			m_state.setStatus(2);
			valid = false;
		}
		if (day < FIRST_VALID_DAY || day > maxDay) {
			m_state = "Invalid day in date";
			m_state.setStatus(3);
			valid = false;
		}

		return valid;
	}
	bool Date::validDateWithParameters(int year, int month, int day)
	{
		if (year<CURRENT_YEAR || year> MAX_YEAR)
		{
			m_state = "Invalid year in date";
			m_state.setStatus(1);
			return false;
		}
		if (month <= INVALID_DATE || month >= MONTH_THIRTEEN)
		{
			m_state = "Invalid month in date";
			m_state.setStatus(2);
			return false;
		}
		int maxDay = ut.daysOfMon(month, year);
		if (day < FIRST_VALID_DAY || day > maxDay) {
			m_state = "Invalid day in date";
			m_state.setStatus(3);
			return false;
		}
		return true;
	}
	int Date::uniqueValue() const
	{
		return year * 372 + month * 31 + day;
	}
	Date::Date(int f_year, int f_month, int f_day)
	{
		if (validDateWithParameters(f_year, f_month, f_day))
		{
			year = f_year;
			month = f_month;
			day = f_day;
		}

	}
	bool Date::operator=(const Date& other)
	{
		if (this != &other) {
			year = other.year;
			month = other.month;
			day = other.day;
			m_formatted = other.m_formatted;
		}
		return *this;
	}
	bool Date::operator==(const Date& other) const
	{
		return uniqueValue() == other.uniqueValue();
	}
	bool Date::operator!=(const Date& other) const
	{
		return uniqueValue() != other.uniqueValue();
	}
	bool Date::operator<(const Date& other) const
	{
		return uniqueValue() < other.uniqueValue();
	}
	bool Date::operator>(const Date& other) const
	{
		return uniqueValue() > other.uniqueValue();
	}
	bool Date::operator<=(const Date& other) const
	{
		return uniqueValue() <= other.uniqueValue();
	}
	bool Date::operator>=(const Date& other) const
	{
		return uniqueValue() >= other.uniqueValue();
	}
	const sdds::Status& Date::state() const
	{
		return m_state;
	}
	Date& Date::formatted(bool isFormatted)
	{
		m_formatted = isFormatted;
		return *this;
	}
	Date::operator bool() const
	{
		return m_state;
	}
	std::ostream& Date::write(std::ostream& COUT) const
	{
		if (m_formatted)
		{	
			COUT << year << '/' << std::setw(2) << std::setfill('0') << month << '/';
		}
		else {		  
			COUT << std::setw(2) << std::setfill('0') << (year % 100) << std::setw(2) << std::setfill('0') << month;
		}

		COUT << std::setw(2) << std::setfill('0') << day;

		return COUT;
	}

	std::istream& Date::read(std::istream& CIN)
	{
		int receivedDate{};
		CIN >> receivedDate;
		if (receivedDate >= 1000 && receivedDate <= 9999)
		{
			year = (receivedDate / 10000) + 2000;
			month = (receivedDate / 100) % 1000;
			day = receivedDate % 100;
		}
		else if (receivedDate >= 100000 && receivedDate <= 999999)
		{
			year = receivedDate / 10000;
			month = (receivedDate / 100) % 100;
			day = receivedDate % 100;
			year += 2000;
		}
		if (receivedDate < 100)
		{
			year = 2023;
			month = 0;
			day = receivedDate % 100;
		}


		if (!validDate())
			CIN.setstate(std::ios::badbit);

		return CIN;
	}


	std::ostream& operator<<(std::ostream& os, const Date& date)
	{
		return date.write(os);
	}
	std::istream& operator>>(std::istream& is, Date& date)
	{
		return date.read(is);
	}
}


