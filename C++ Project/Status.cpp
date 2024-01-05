/*
*****************************************************************************
File: Status.cpp
Full Name  : Harnoor Kaur Dran
Email : hkdran@outlook.com
*****************************************************************************
*/
#define _CRT_SECURE_NO_WARNINGS
#include "Status.h"
#include<cstring>
namespace sdds {
	const char* Status::getDescription() const
	{
		return description;
	}

	Status::operator int() const
	{
		return statusCode;
	}

	Status::operator const char* () const
	{
		return description;
	}

	Status::operator bool() const
	{
		return !description;
	}


	Status::Status(char* desc, int status)
	{
		if (desc != nullptr)
		{
			description = new char[strlen(desc) + 1];
			strcpy(description, desc);
		}
		else
		{
			description = nullptr;
		}
		statusCode = status;
	}

	Status::~Status()
	{
		delete[] description;
	}

	Status::Status(const Status& other)
	{
		if (other.description != nullptr)
		{
			description = new char[strlen(other.description) + 1];
			strcpy(description, other.description);
		}
		else {
			description = nullptr;
		}
		statusCode = other.statusCode;
	}

	void Status::setStatus(int status)
	{
		statusCode = status;

	}
	void Status::setStatus(const char* status)
	{
		if (status != nullptr)
		{
			delete[] description;
			description = nullptr;
			description = new char[strlen(status) + 1];
			strcpy(description, status);
		}
	}
	int Status::getStatus() const 
	{
		return statusCode;
	}


	Status& Status::operator=(const char* newDesc)
	{
		delete[] description;
		description = new char[strlen(newDesc) + 1];
		strcpy(description, newDesc);
		statusCode = 0; 
		return *this;
	}

	Status& Status::operator=(const int newStatus)
	{
		statusCode = newStatus;
		return *this;
	}

	Status& Status::clear()
	{
		delete[] description;
		description = nullptr;
		statusCode = 0;
		return *this;
	}





	std::ostream& operator<<(std::ostream& ostr, const Status& status)
	{
		if (!status) {

			if (status.getStatus() == 1)
			{
				ostr << "ERR#" << status.getStatus() << ": " << status.getDescription();
			}
			else if (status.getStatus() == 2)
			{
				ostr << "ERR#" << status.getStatus() << ": " << status.getDescription();
			}
			else if (status.getStatus() == 3)
			{
				ostr << "ERR#" << status.getStatus() << ": " << status.getDescription();
			}
			else if (status.getStatus() == 0) {
				ostr << status.getDescription();
			}
			else if (status.getStatus() > 0)
			{
				ostr << "ERR#" << status.getStatus() << " " << status.getDescription();
			}
			else if (status.getStatus() < 0)
			{
				ostr << "ERR#" << status.getStatus() << ": " << status.getDescription();
			}
		}
		return ostr;
	}


}