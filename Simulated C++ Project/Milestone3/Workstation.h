// Name: Harnoor Kaur Dran
// Seneca Student ID: 145433223
// Seneca email: hkdran@myseneca.ca
// Date of completion: 02-04-2024
//
// I confirm that I am the only author of this file
//   and the content was created entirely by me.
#ifndef SENECA_WORKSTATION_H
#define SENECA_WORKSTATION_H
#include <iostream>
#include <deque>
#include "Station.h"
#include "CustomerOrder.h"
namespace seneca { 
	extern std::deque<CustomerOrder> g_pending;
	extern std::deque<CustomerOrder> g_completed;
	extern std::deque<CustomerOrder> g_incomplete;

	class Workstation : public Station{
		std::deque<CustomerOrder> m_orders;
		Workstation* m_pNextStation{ nullptr };
	public:
		Workstation(const std::string& str) : Station(str) {};
		void fill(std::ostream& os);
		bool attemptToMoveOrder();
		void setNextStation(Workstation* station = nullptr);
		Workstation* getNextStation() const;
		void display(std::ostream& os) const;
		Workstation& operator+=(CustomerOrder&& newOrder);
		~Workstation();

		Workstation(const Workstation& src) = delete;
		Workstation& operator=(const Workstation& src) = delete;
		Workstation(Workstation&& src) = delete;
		Workstation& operator=(Workstation&& src) = delete;
	};
}
#endif