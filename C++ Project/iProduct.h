/*
*****************************************************************************
File : iProduct.h
Full Name  : Harnoor Kaur Dran
Email : hkdran@outlook.com
*****************************************************************************
*/
#ifndef SDDS_I_PRODUCTS_H
#define SDDS_I_PRODUCTS_H
#include <iostream>
#include <fstream>
namespace sdds {
	class iProduct {
	public:
		virtual int readSku(std::istream& istr) = 0;
		virtual int operator-=(int qty) = 0;
		virtual int operator+=(int qty) = 0;
		virtual ~iProduct() {};
		
		virtual operator double()const = 0;
		
		virtual operator bool()const = 0;
		virtual int qtyNeeded()const = 0;
		
		virtual int qty()const = 0;
		virtual void linear(bool isLinear) = 0;
		virtual std::ofstream& save(std::ofstream& ofstr)const = 0;
		virtual std::ifstream& load(std::ifstream& ifstr) = 0;
		// displays the iProduct 
		virtual std::ostream& display(std::ostream& ostr)const = 0;
		// reads the iProduct 
		virtual std::istream& read(std::istream& istr) = 0;
		// return true if the SKU is a match to the iProduct's SKU unit
		virtual bool operator==(int sku)const = 0;
		// returns true if the description is found in the iPorduct's description
		virtual bool operator==(const char* description)const = 0;

	};
	std::istream& operator>>(std::istream& istr, iProduct& p);
	std::ostream& operator<<(std::ostream& ostr, iProduct& p);


}
#endif // !I_PRODUCTS_H