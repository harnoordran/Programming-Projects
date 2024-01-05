/*
*****************************************************************************
File : Persihable.cpp
Full Name  : Harnoor Kaur Dran
Email : hkdran@outlook.com
*****************************************************************************
*/
#define _CRT_SECURE_NO_WARNINGS
#include "Perishable.h"
#include"Date.h"
#include<iostream>
#include <limits>
#include<iomanip>
#include<cstring>
#include<fstream>
using namespace std;
namespace sdds {
	Perishable::Perishable() {}
	Perishable::Perishable(const Perishable& other) :Item(other)
	{
		*this = other;
	}
	Perishable& Perishable::operator=(const Perishable& perishable)
	{
		if (this != &perishable) {
			Item::operator=(perishable);

			delete[] m_instructions;
			m_instructions = nullptr;

			if (perishable.m_instructions
				&& perishable.m_instructions[0] != '\0') {
				m_instructions = new char[strlen(perishable.m_instructions) + 1];
				strcpy(m_instructions, perishable.m_instructions);
			}

			m_exp_date = perishable.m_exp_date;
		}

		return *this;
	}
	const Date& Perishable::expiry() const
	{
		return m_exp_date;
	}
	void Perishable::setUnformatted()
	{
		m_exp_date.formatted(false);
	}

	char* Perishable::readInstructions(istream& istr)
	{
		delete[] m_instructions;
		m_instructions = nullptr;
		const int size = 1000;
		char tempInstructions[size];
		tempInstructions[0] = '\0';
		//istr.clear();
		//istr.ignore();
		istr.get(tempInstructions, size, '\n');
		ut.alocpy(m_instructions, tempInstructions);


		return m_instructions;
	}

	ostream& Perishable::displayExpiryDate(ostream& ostr) const
	{
		m_exp_date.write(ostr);
		return ostr;
	}
	istream& Perishable::readExpiryDate(istream& istr)
	{
		if (istr)
		{
			cout << "Expiry date (YYMMDD): ";
			istr.clear();
			istr.ignore();
			m_exp_date.read(istr);
		


		}
		return istr;
	}
	int Perishable::readSku(istream& istr)
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
			else if (sku < 10000 || sku>39999) {
				cout << "Value out of range [10000<=val<=39999]: ";
			}
			else { isValid = true; }

		} while (!isValid);
		m_sku = sku;
		return sku;


		return 0;
	}
	ofstream& Perishable::save(ofstream& ofstr) const
	{
		if (ofstr) {
			Item::save(ofstr);
			ofstr << '\t' << (m_instructions ? m_instructions : "") << '\t';

		
			Date temp(m_exp_date.getYear(), m_exp_date.getMonth(), m_exp_date.getDay());
			temp.formatted(false);

			ofstr << temp;
		}
		return ofstr;

		
	}
	ifstream& Perishable::load(ifstream& ifstr)
	{

		Item::load(ifstr);
		ifstr.ignore();

		const int size = 1000;
		char tempInstructions[size];
		tempInstructions[0] = '\0';

		ifstr.getline(tempInstructions, size, '\t');
		if (tempInstructions[0] != '\0') {
			ut.alocpy(m_instructions, tempInstructions);
		}
		else
		{
			delete[] m_instructions;
			m_instructions = nullptr;
		}


		ifstr >> m_exp_date;
		ifstr.ignore();
		if (ifstr.fail())
		{
			status.clear();
			status.setStatus("Input file stream read (perishable) failed!");
		}
		return ifstr;
	}
	ostream& Perishable::display(ostream& ostr) const
	{
		if (m_exp_date)
		{
			double purchaseFund = 0.0;
			if (Item::linear())
			{
				Item::display(ostr);

				ostr << (m_instructions && m_instructions[0] != '\0' ? '*' : ' ');

				displayExpiryDate(ostr);
			}
			else {
				char* itemDesc = getItemDesc();
				int needQty = qtyNeeded();
				int qtyOnHand = qty();
				double price = getPrice();
				ostr << "Perishable AMA Item:" << endl;
				ostr << m_sku << ": " << itemDesc << endl;
				ostr << "Quantity Needed: " << needQty << endl;
				ostr << "Quantity Available: " << qtyOnHand << endl;
				ostr << "Unit Price: $" << setw(4) << fixed << setprecision(2) << price << endl;
				if (qtyOnHand == 0)
				{
					purchaseFund = price * needQty;
				}
				if (qtyOnHand > 1)
				{
					purchaseFund = ((price * needQty) - qtyOnHand * price);
				}
				ostr << "Needed Purchase Fund: $" << fixed << setprecision(2) << purchaseFund << endl;
				ostr << "Expiry date: "; displayExpiryDate(cout); ostr << endl;
				if (m_instructions != nullptr && m_instructions[0] != '\0') {
					ostr << "Handling Instructions: " << m_instructions << endl;
				}
			}
		}
		else { ostr << "Bad state"; }

		return ostr;
	}
	istream& Perishable::read(std::istream& istr)
	{
		if (istr)
		{
			Item::read(istr);
			readExpiryDate(istr);
			istr.ignore();
			cout << "Handling Instructions, ENTER to skip: " << endl;

			delete[] m_instructions;
			m_instructions = nullptr;

			const int bufferSZ = 99;
			char buffer[bufferSZ]{};
			size_t i{};

			for (; i < bufferSZ && istr.peek() != '\n'; i++)
				buffer[i] = istr.get();

			if (i) {
				m_instructions = new char[i + 1];
				strcpy(m_instructions, buffer);
			}
		}
		else {
			status.clear();
			status.setStatus("Perishable console date entry failed!");
		}
		return istr;
	}
}