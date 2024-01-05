/*
*****************************************************************************
File : Menu.cpp
Full Name  : Harnoor Kaur Dran
Email : hkdran@outlook.com
*****************************************************************************
*/
#define _CRT_SECURE_NO_WARNINGS
#include "Menu.h"
#include"AidMan.h"
#include<limits>
#include <cstring>
using namespace std;
namespace sdds {

	Menu::Menu(const char* options)
	{
		if (options == nullptr)
		{
			m_options = nullptr;
		}
		if (strlen(options) > 15)
		{
			m_options = nullptr;
		}
		if (options != nullptr)
		{
			if (strlen(options) == 20) { m_options = nullptr; }
			else {

				delete[] m_options;

				m_options = new char[strlen(options) + 1];
				strcpy(m_options, options);
			}
		}

	}

	unsigned int  Menu::run() const
	{

		const char* prompt = "> ";
		int i = 0;
		int m = 7;
		int m_value = 0;


		if (m_options)
		{

			size_t sequenceNumber = 1;

			for (size_t i = 0; i < strlen(m_options); i++) {
				if (m_options[i] != '\t') {
					cout << sequenceNumber << "- ";
					while (m_options[i] != '\t' && m_options[i] != '\0') {
						cout << m_options[i++];
					}
					cout << endl;
					sequenceNumber++;
				}
			}
			cout << "---------------------------------\n"
				<< "0- Exit\n";


			m_value = ut.getint(i, m, prompt);
		}
		else cout << "Invalid Menu!\n";
		return m_value;
	}



	Menu::~Menu()
	{
		delete[] m_options;
	}

}