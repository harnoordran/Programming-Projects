// Name: Harnoor Kaur Dran
// Seneca Student ID: 145433223
// Seneca email: hkdran@myseneca.ca
// Date of completion: 02-04-2024
//
// I confirm that I am the only author of this file
//   and the content was created entirely by me.
#include "CustomerOrder.h"
#include "Utilities.h"

namespace seneca {
	size_t CustomerOrder::m_widthField = 0;

	CustomerOrder::CustomerOrder(const std::string& str) {
		Utilities utilitiesObj;
		size_t index = 0u;
		bool quitLoop = false;
		m_cntItem = std::count(str.begin(), str.end(), Utilities::getDelimiter());
		m_cntItem--;
		m_lstItem = new Item * [m_cntItem];
		m_name = utilitiesObj.extractToken(str, index, quitLoop);
		m_product = utilitiesObj.extractToken(str, index, quitLoop);

		for (size_t i = 0; i < m_cntItem && quitLoop; i++){
			m_lstItem[i] = new Item(utilitiesObj.extractToken(str, index,quitLoop));
			CustomerOrder::m_widthField = CustomerOrder::m_widthField < utilitiesObj.getFieldWidth() ? utilitiesObj.getFieldWidth() : CustomerOrder::m_widthField;
		}
	}
	CustomerOrder::CustomerOrder(const CustomerOrder& src) {
		throw "Error!";

	}
	CustomerOrder::CustomerOrder(CustomerOrder&& src)noexcept {
		*this = std::move(src);
	}

	CustomerOrder& CustomerOrder::operator=(CustomerOrder&& src) noexcept
	{
		if (this != &src) {

			m_name = src.m_name;
			m_product = src.m_product;
			m_widthField = src.m_widthField;
			deallocateMemory();
			this->m_lstItem = src.m_lstItem;
			src.m_lstItem = nullptr;
			this->m_cntItem = src.m_cntItem;
			src.m_cntItem = 0;
			
		}

		return *this;
	}

	void CustomerOrder::deallocateMemory(){
		for (size_t i = 0; i < m_cntItem; i++) {
			delete m_lstItem[i];
			m_lstItem[i] = nullptr;
		}
		delete[] m_lstItem;
		m_lstItem = nullptr;
	}
	CustomerOrder::~CustomerOrder()
	{
		deallocateMemory();
 	}

	bool CustomerOrder::isOrderFilled() const
	{
		bool quitLoop = true;
		for (unsigned int i = 0; i < m_cntItem; i++) {

			if (!m_lstItem[i]->m_isFilled) {
				quitLoop = false;
			}
		}
		return quitLoop;
	}

	bool CustomerOrder::isItemFilled(const std::string& itemName) const
	{
		bool isFill = true;
		for (unsigned int i = 0; i < m_cntItem; i++) {
			if (m_lstItem[i]->m_itemName == itemName && m_lstItem[i]->m_isFilled == false) {
				isFill = false;
			}
		}
		return isFill;
	}

	void CustomerOrder::fillItem(Station& station, std::ostream& os)
	{
		bool quitLoop = false;
		for (size_t i = 0; i < m_cntItem && !quitLoop; i++) {
			if (m_lstItem[i]->m_itemName == station.getItemName() && !m_lstItem[i]->m_isFilled && station.getQuantity() >= 1)
			{
				station.updateQuantity();
				m_lstItem[i]->m_serialNumber = station.getNextSerialNumber();
				m_lstItem[i]->m_isFilled = true;
				os << "    Filled " << m_name << ", " << m_product << " [" << m_lstItem[i]->m_itemName << "]" << std::endl;
				quitLoop = true;
			}
			else if (m_lstItem[i]->m_itemName == station.getItemName() && !m_lstItem[i]->m_isFilled && station.getQuantity() < 1)
			{
				os << "    Unable to fill " << m_name << ", " << m_product << " [" << m_lstItem[i]->m_itemName << "]" << std::endl;
			}
			
		}
	}

	void CustomerOrder::display(std::ostream& os) const
	{
		os << m_name << " - " << m_product << std::endl;
		for (size_t i = 0; i < m_cntItem; i++)
		{
			os << "[" << std::setw(6) << std::setfill('0') << std::right << m_lstItem[i]->m_serialNumber << "] " << std::setfill(' ') << std::setw(CustomerOrder::m_widthField) << std::left << m_lstItem[i]->m_itemName << " - " << (m_lstItem[i]->m_isFilled ? "FILLED" : "TO BE FILLED") << std::endl;
		}
	}



}