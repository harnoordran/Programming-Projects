// Name: Harnoor Kaur Dran
// Seneca Student ID: 145433223
// Seneca email: hkdran@myseneca.ca
// Date of completion: 02-04-2024
//
// I confirm that I am the only author of this file
//   and the content was created entirely by me.
#include "LineManager.h"
#include "Utilities.h"
#include <iostream>
#include <fstream>
namespace seneca {
	LineManager::LineManager(const std::string& file, const std::vector<Workstation*>& stations)
	{
		Utilities tempObj;
		std::string line;
		size_t nextIndex;
		bool quit = false;
		std::string item;
		std::string nextItem;

		std::ifstream fs(file);
		if (!fs) {
			throw std::string("Unable to open the file!");
		}
		
		while (std::getline(fs, line)) {
			nextIndex = 0;
			quit = true;
			Workstation* station{};
			Workstation* nextStation{};
			std::string item;
			std::string nextItem;

			item = tempObj.extractToken(line, nextIndex, quit);
			station = *std::find_if(stations.begin(), stations.end(), [&](Workstation* ws) {
				return ws->getItemName() == item;
				});
			m_activeLine.push_back(station);

			if (quit != false) {
				nextItem = tempObj.extractToken(line, nextIndex, quit);
				nextStation = *std::find_if(stations.begin(), stations.end(), [&](Workstation* ws1) {
					return ws1->getItemName() == nextItem;
					});
				station->setNextStation(nextStation);
			}
		}

		std::for_each(m_activeLine.begin(), m_activeLine.end(), [&](Workstation* ws2) {
			auto firstStation = std::find_if(m_activeLine.begin(), m_activeLine.end(), [&](Workstation* ws3) {
				return ws2 == ws3->getNextStation();
				});
			if (firstStation == m_activeLine.end()) {
				m_firstStation = ws2;
			}
			});
		fs.close();
		m_cntCustomerOrder = g_pending.size();
	}
	void LineManager::reorderStations()
	{
		m_activeLine.clear();
		Workstation* ws;
		m_activeLine.push_back(m_firstStation);
		while ((ws = m_activeLine.back()->getNextStation())) {
			m_activeLine.push_back(ws);
		}
	}
	bool LineManager::run(std::ostream& os)
	{
		static int count = 0;
		os << "Line Manager Iteration: " << ++count << std::endl;
		if (!g_pending.empty()) {
			*m_firstStation += std::move(g_pending.front());
			g_pending.pop_front();

		}

		std::for_each(m_activeLine.begin(), m_activeLine.end(), [&](Workstation* ws) {
			ws->fill(os);
			});

		std::for_each(m_activeLine.begin(), m_activeLine.end(), [](Workstation* ws) {
			ws->attemptToMoveOrder();
			});
		return g_completed.size() + g_incomplete.size() == m_cntCustomerOrder;


	}
	void LineManager::display(std::ostream& os) const {
		std::for_each(m_activeLine.begin(), m_activeLine.end(), [&](const Workstation* ws) {
			ws->display(os); 
			});
		
	}
}