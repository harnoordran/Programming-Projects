// Name: Harnoor Kaur Dran
// Seneca Student ID: 145433223
// Seneca email: hkdran@myseneca.ca
// Date of completion: 22-03-2024
//
// I confirm that I am the only author of this file
//   and the content was created entirely by me.
#include <iostream>
#include <iomanip>
#include <string>
#include "Station.h"
#include "Utilities.h"
namespace seneca {
	int Station::id_generator = 0;
	size_t Station::m_widthField = 0;


	Station::Station(const std::string& obj)
	{
		std::string string = "";
		Utilities utilitiesObj = Utilities();
		bool validity = false;
		size_t pos = 0;
		try {
			m_itemName = utilitiesObj.extractToken(obj, pos, validity);
			if (m_itemName.size() > m_widthField) {
				m_widthField = m_itemName.size();
			}
			utilitiesObj.setFieldWidth(m_widthField);
			if (validity == true) {
				string = utilitiesObj.extractToken(obj, pos, validity);
				m_serialNumber = std::stoi(string);
				string = utilitiesObj.extractToken(obj, pos, validity);
				m_quantity = std::stoi(string);
				m_description = utilitiesObj.extractToken(obj, pos, validity);
				station_id = ++id_generator;


			}


		}
		catch (const char* msg) {
			std::cout << "Error: " << msg << std::endl;
		}

	}
	const std::string& Station::getItemName() const
	{
		return m_itemName;
	}

	size_t Station::getNextSerialNumber()
	{
		size_t value = m_serialNumber;
		m_serialNumber++;
		return value;
	}

	size_t Station::getQuantity() const
	{
		return m_quantity;
	}

	void Station::updateQuantity()
	{
		if (m_quantity > 0) {
			m_quantity--;


		}
	}

	void Station::display(std::ostream& os, bool full) const
	{
		os << std::right << std::setw(3) << std::setfill('0') << station_id << " | "
			<< std::left << std::setw(m_widthField) << std::setfill(' ') << m_itemName << " | "
			<< std::right << std::setfill('0') << std::setw(6) << m_serialNumber << std::setfill(' ') << " | ";

		if (!full) {
			os << std::endl;
		}
		else {
			os << std::right << std::setw(4) << m_quantity << " | "
				<< std::left << m_description << std::endl;
		}
	}


}