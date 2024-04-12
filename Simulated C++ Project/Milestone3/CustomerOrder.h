// Name: Harnoor Kaur Dran
// Seneca Student ID: 145433223
// Seneca email: hkdran@myseneca.ca
// Date of completion: 02-04-2024
//
// I confirm that I am the only author of this file
//   and the content was created entirely by me.
#ifndef SENECA_CUSTOMERORDER_H
#define SENECA_CUSTOMERORDER_H
#include "Station.h"
#include <iostream>
#include <cstring>
#include <iomanip>
#include <algorithm>
#include <sstream>
namespace seneca {
	struct Item
	{
		std::string m_itemName;
		size_t m_serialNumber{ 0 };
		bool m_isFilled{ false };

		Item(const std::string& src) : m_itemName(src) {};
	};
	class CustomerOrder {
		std::string m_name{};
		std::string m_product{};
		Item** m_lstItem{nullptr};
		size_t m_cntItem{ 0 };

		void deallocateMemory();
		static size_t m_widthField;
	public:
		CustomerOrder() {};
		CustomerOrder(const std::string&);
		CustomerOrder(const CustomerOrder& src);
		CustomerOrder& operator=(CustomerOrder& src) = delete;
		CustomerOrder(CustomerOrder&& src) noexcept;
		CustomerOrder& operator=(CustomerOrder&& src)noexcept;
		~CustomerOrder();
		bool isOrderFilled() const;
		bool isItemFilled(const std::string& itemName) const;
		void fillItem(Station& station, std::ostream& os);
		void display(std::ostream& os) const;




	};


}
#endif