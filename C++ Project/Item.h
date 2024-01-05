/*
*****************************************************************************
File : Item.h
Full Name  : Harnoor Kaur Dran
Email : hkdran@outlook.com
*****************************************************************************
*/
#ifndef SDDS_ITEM_H
#define SDDS_ITEM_H
#include <iostream>
#include "iProduct.h"
#include"Status.h"
#include"Utils.h"
using namespace std;
namespace sdds {

	class Item :public iProduct {
		double m_price;
		int m_qtyOnHand;
		int m_neededQty;
		char* m_item_desc;
		bool m_isLinear;

	protected:
		Status status;
		int m_sku;
		bool linear() const;

	public:
		void setSku(int sku);
		Item();
		Item(const Item& other);
		Item& operator=(const Item& other);
		void clear();
		~Item();

		char* getItemDesc()const;
		double getPrice()const;

		int qtyNeeded()const override;
		int qty()const override;
		operator double()const override;
		operator bool()const override;

		int readSku(std::istream& istr)override;
		char* readDesc(istream& istr);
		int readQtyNeeded(istream& istr);
		int readQtyInHand(istream& istr);
		double readPrice(istream& istr);

		char* FileReadDesc(ifstream& ifstr);
		int operator-=(int qty) override;
		int operator+=(int qty) override;
		void linear(bool isLinear) override;
		bool operator==(int sku)const override;
		bool operator==(const char* description)const override;
		ofstream& save(std::ofstream& ofstr)const override;
		ifstream& load(std::ifstream& ifstr)override;
		ostream& display(std::ostream& ostr)const override;
		istream& read(std::istream& istr) override;


	};

}
#endif // !ITEM_H