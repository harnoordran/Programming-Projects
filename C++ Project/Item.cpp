/*
*****************************************************************************
File : Item.cpp
Full Name  : Harnoor Kaur Dran
Email : hkdran@outlook.com
*****************************************************************************
*/
#define _CRT_SECURE_NO_WARNINGS
#include "Item.h"
#include <iostream>
#include<fstream>
#include<iomanip>
#include <cstring>
#include <limits>
using namespace std;
namespace sdds {
	bool Item::linear() const
	{
		return m_isLinear;
	}
	Item::Item() :m_price(0.0), m_qtyOnHand(0), m_neededQty(0), m_item_desc(nullptr), m_isLinear(false)
	{
		status.clear();
		m_sku = 0;
	}
	Item::Item(const Item& other) :m_price(other.m_price), m_qtyOnHand(other.m_qtyOnHand), m_neededQty(other.m_neededQty), m_item_desc(nullptr),
		m_isLinear(other.m_isLinear), status(other.status), m_sku(other.m_sku)
	{
		if (other.m_item_desc)
		{
			m_item_desc = new char[strlen(other.m_item_desc) + 1];
			strcpy(m_item_desc, other.m_item_desc);
		}
		else {
			m_item_desc = nullptr;
		}
	}
	Item& Item::operator=(const Item& other)
	{
		if (this != &other)
		{
			m_price = other.m_price;
			m_qtyOnHand = other.m_qtyOnHand;
			m_neededQty = other.m_neededQty;
			m_isLinear = other.m_isLinear;
			status = other.status;
			m_sku = other.m_sku;

			delete[] m_item_desc;
			if (other.m_item_desc)
			{
				m_item_desc = new char[strlen(other.m_item_desc) + 1];
				strcpy(m_item_desc, other.m_item_desc);
			}
			else {
				m_item_desc = nullptr;
			}
		}
		return *this;
	}
	int Item::qtyNeeded() const
	{
		return m_neededQty;
	}
	int Item::qty() const
	{
		return m_qtyOnHand;
	}
	Item::operator double() const
	{
		return m_price;
	}
	Item::operator bool() const {

		return status;
	}
	int Item::readSku(std::istream& istr)
	{
		int sku;
		bool isValid = false;
		cout << "SKU: ";
		do {

			istr >> sku;
			if (istr.fail())
			{
				istr.clear();
				istr.ignore(numeric_limits<streamsize>::max(), '\n');
				cout << "Invalid Integer, retry: ";
			}
			else if (sku < 4000 || sku>99999) {
				cout << "Value out of range [40000<=val<=99999]: ";
			}
			else { isValid = true; }

			
		} while (!isValid);
		m_sku = sku;
		return sku;
	}
	char* Item::readDesc(istream& istr)
	{

		const int size = 1000;
		char tempDescription[size];
		tempDescription[0] = '\0';
		cout << "Description: ";
		istr.get(tempDescription, size, '\n');
		ut.alocpy(m_item_desc, tempDescription);
		return m_item_desc;
	}
	int Item::readQtyNeeded(istream& istr)
	{
		int qty_needed;
		bool isValid = false;
		cout << "Quantity Needed: ";
		do {

			istr >> qty_needed;
			if (istr.fail())
			{
				istr.clear();
				istr.ignore(numeric_limits<streamsize>::max(), '\n');
				cout << "Invalid Integer, retry: ";
			}
			else if (qty_needed < 1 || qty_needed>9999) {
				cout << "Value out of range [1<=val<=9999]: ";
			}
			else { isValid = true; }

			/*cout << endl;*/
		} while (!isValid);
		m_neededQty = qty_needed;
		return m_neededQty;
	}
	int Item::readQtyInHand(istream& istr)
	{
		int qty_inHand;
		bool isValid = false;
		cout << "Quantity On Hand: ";
		do {

			istr >> qty_inHand;
			if (istr.fail())
			{
				istr.clear();
				istr.ignore(numeric_limits<streamsize>::max(), '\n');
				cout << "Invalid Integer, retry: ";
			}
			else if (qty_inHand<0 || qty_inHand>m_neededQty) {
				cout << "Value out of range [0<=val<=" << m_neededQty << "]: ";
			}
			else { isValid = true; }

			/*cout << endl;*/
		} while (!isValid);
		m_qtyOnHand = qty_inHand;
		return m_qtyOnHand;
	}
	double Item::readPrice(istream& istr)
	{
		double price = 0.0;
		bool isValid = false;
		cout << "Unit Price: $";
		do {

			istr >> price;
			if (istr.fail())
			{
				istr.clear();
				istr.ignore(numeric_limits<streamsize>::max(), '\n');
				cout << "Invalid number, retry: ";
			}
			else if (price < 0.0 || price >9999.0) {
				cout << "Value out of range [0.00<=val<=9999.00]: ";
			}
			else { isValid = true; }

		} while (!isValid);
		m_price = price;
		return m_price;
	}
	char* Item::FileReadDesc(ifstream& ifstr)
	{

		const int size = 1000;
		char tempDescription[size];
		tempDescription[0] = '\0';
		ifstr.get(tempDescription, size, '\t');
		ut.alocpy(m_item_desc, tempDescription);
		return m_item_desc;
	}
	int Item::operator-=(int qty)
	{
		if (*this)
		{
			m_qtyOnHand -= qty;
		}
		return *this;
	}
	int Item::operator+=(int qty)
	{
		if (*this)
		{
			m_qtyOnHand += qty;
		}
		return *this;
	}
	void Item::linear(bool isLinear)
	{
		m_isLinear = isLinear;
	}
	bool Item::operator==(int sku) const
	{
		return sku == m_sku;
	}
	bool Item::operator==(const char* description) const
	{
		if (description == nullptr || m_item_desc == nullptr)
		{
			return false;
		}
		return(strstr(m_item_desc, description) != nullptr);
	}
	ofstream& Item::save(std::ofstream& ofstr) const
	{
		if (*this)
		{
			ofstr << m_sku << "\t"
				<< m_item_desc << "\t"
				<< m_qtyOnHand << "\t"
				<< m_neededQty << "\t"
				<< m_price;
		}
		return ofstr;
	}
	ifstream& Item::load(std::ifstream& ifstr)
	{
		
		ifstr >> m_sku >> std::ws;
		FileReadDesc(ifstr);
		ifstr >> m_qtyOnHand >> m_neededQty >> m_price;
		if (ifstr.fail())
		{
			status.clear();
			status.setStatus("Input file stream read failed!");
		}

		return ifstr;
	}
	ostream& Item::display(std::ostream& ostr) const
	{

		double purchaseFund = 0.0;
		if (*this)
		{
			if (linear() && m_sku) {

				ostr << setw(5) << left << m_sku << " " << setfill(' ') << "| ";
				for (size_t i = 0; i < 35 && m_item_desc[i] != '\0'; i++)
				{
					ostr << m_item_desc[i];
				}
				std::streamsize padding = 35 - strlen(m_item_desc) + 1;
				ostr << setw(padding) << " " << "| "

					//ostr << setw(35- strlen(m_item_desc)+1) <<" " << "| "
					<< setw(4) << right << m_qtyOnHand << " | "
					<< setw(4) << right << m_neededQty << " |  ";
				if (m_qtyOnHand == 0)
				{
					purchaseFund = m_price * m_neededQty;
				}
				if (m_qtyOnHand > 1)
				{
					purchaseFund = ((m_price * m_neededQty) - m_qtyOnHand * m_price);
				}
				ostr << setw(6) << fixed << setprecision(2) << m_price << " |";
			}
				
			else {

				ostr << "AMA Item:" << endl;
				ostr << m_sku << ": " << m_item_desc << endl;
				ostr << "Quantity Needed: " << m_neededQty << endl;
				ostr << "Quantity Available: " << m_qtyOnHand << endl;
				ostr << "Unit Price: $" << setw(4) << fixed << setprecision(2) << m_price << endl;
				if (m_qtyOnHand == 0)
				{
					purchaseFund = m_price * m_neededQty;
				}
				if (m_qtyOnHand > 1)
				{
					purchaseFund = ((m_price * m_neededQty) - m_qtyOnHand * m_price);
				}
				ostr << "Needed Purchase Fund: $" << fixed << setprecision(2) << purchaseFund << endl;
			}

		}
		else { ostr << "Bad state"; }

		return ostr;
	}
	istream& Item::read(std::istream& istr)
	{
	
		if (istr)
		{
			status.clear();
			cout << "AMA Item:" << endl;
			cout << "SKU: " << m_sku << endl;
			readDesc(istr);
			readQtyNeeded(istr);
			readQtyInHand(istr);
			readPrice(istr);

		}
		else { status.setStatus("Console entry failed!"); }

		return istr;
	}

	void Item::clear()
	{
		status.clear();
	}
	Item::~Item()
	{
		delete[] m_item_desc;
		m_item_desc = nullptr;
	}
	char* Item::getItemDesc() const
	{
		return m_item_desc;
	}
	double Item::getPrice() const
	{
		return m_price;
	}
	
	void Item::setSku(int sku) {
		m_sku = sku;
	}


}