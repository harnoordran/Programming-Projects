/*
*****************************************************************************
File : Date.h
Full Name  : Harnoor Kaur Dran
Email : hkdran@outlook.com
*****************************************************************************
*/
#ifndef SDDS_DATE_H
#define SDDS_DATE_H
#include"Status.h"
#include "Utils.h"
namespace sdds {


	class Date {
		
		const int MAX_YEAR = 2030;
		const int CURRENT_YEAR = 2023;
		const int INVALID_DATE = 0;
		const int MONTH_THIRTEEN = 13;
		int FIRST_VALID_DAY = 1;
		int LAST_VALID_DAY = 31;

		sdds::Status m_state{};
		sdds::Utils ut;

		int year = 2023;
		int month = 12;
		int day = 9;

		bool m_formatted{ true };


		bool validDate();
		bool validDateWithParameters(int year, int month, int day);
		int uniqueValue() const;
	public:
		Date() {}
		Date(int year, int month, int day);
		bool operator =(const Date& other);
		bool operator ==(const Date& other) const;
		bool operator !=(const Date& other) const;
		bool operator <(const Date& other) const;
		bool operator >(const Date& other) const;
		bool operator <=(const Date& other) const;
		bool operator >=(const Date& other) const;
		const sdds::Status& state() const;
		Date& formatted(bool isFormatted);
		operator bool() const;
		std::ostream& write(std::ostream& COUT) const;
		std::istream& read(std::istream& CIN);

		//Queries
		int getYear() const { return year; }
		int getMonth() const { return month; }
		int getDay() const { return day; }
	};
	std::ostream& operator<<(std::ostream& os, const Date& date);
	std::istream& operator>>(std::istream& is, Date& date);
}
#endif // !DATE_H