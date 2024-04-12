// Name: Harnoor Kaur Dran
// Seneca Student ID: 145433223
// Seneca email: hkdran@myseneca.ca
// Date of completion: 02-04-2024
//
// I confirm that I am the only author of this file
//   and the content was created entirely by me.
#ifndef SENECA_STATION_H
#define SENECA_STATION_H
#include <string>
#include <iomanip>
#include "Utilities.h"
namespace seneca {
	class Station {
		int station_id;
		std::string m_itemName;
		std::string m_description;
		size_t m_serialNumber;
		size_t m_quantity;
		static size_t m_widthField;
		static int id_generator;
	public:
		Station() {};
		Station(const std::string& obj);
		const std::string& getItemName() const;
		size_t getNextSerialNumber();
		size_t getQuantity() const;
		void updateQuantity();
		void display(std::ostream& os, bool full) const;




	};
}
#endif