/*
*****************************************************************************
File : Perishable.h
Full Name  : Harnoor Kaur Dran
Email : hkdran@outlook.com
*****************************************************************************
*/
#ifndef SDDS_PERISHABLE_H
#define SDDS_PERISHABLE_H
#include"Item.h"
#include"Date.h"
#include<iostream>
#include<fstream>
namespace sdds {
	class Perishable :public Item {
		char* m_instructions{};
		Date m_exp_date{ Date() };

	public:
		Perishable();
		Perishable(const Perishable& other);
		Perishable& operator=(const Perishable& perishable);
		virtual ~Perishable() { delete[] m_instructions; }

		const Date& expiry()const;
		void setUnformatted();
		ostream& displayExpiryDate(ostream& ostr)const;
		istream& readExpiryDate(istream& istr);
		char* readInstructions(istream& istr);
		int readSku(std::istream& istr)override;
		ofstream& save(std::ofstream& ofstr)const override;
		ifstream& load(std::ifstream& ifstr)override;
		ostream& display(std::ostream& ostr)const override;
		istream& read(std::istream& istr) override;

		operator bool()const {
			return m_exp_date.getYear();
		}
	};
}
#endif // !PERISHABLE_H