// Name: Harnoor Kaur Dran
// Seneca Student ID: 145433223
// Seneca email: hkdran@myseneca.ca
// Date of completion: 14-03-2024
//
// I confirm that I am the only author of this file
//   and the content was created entirely by me.
#include <iostream>
#include <string>
#include "Utilities.h"
namespace seneca {
	char Utilities::m_delimiter =','; //The default delimiter

	void Utilities::setFieldWidth(size_t newWidth)
	{
		m_widthField = newWidth;

	}
	size_t Utilities::getFieldWidth() const
	{
		return m_widthField;
	}

	std::string Utilities::extractToken(const std::string& str, size_t& next_pos, bool& more)
	{
		std::string token = ""; 
		static size_t newWidth = 0;
		size_t index = 0;
		more = false;

		if (str.find(m_delimiter, next_pos) == next_pos) {
			more = false;
			newWidth = 0;
			throw "   ERROR: No token.";
		}
		else {

			if (str.find(m_delimiter, next_pos) >= str.length()) {
				index = str.length();
			}
		

			else 
			{
				index = str.find(m_delimiter, next_pos);
			}

			token = str.substr(next_pos, index - next_pos + 1);
			next_pos += token.length(); 


			if (next_pos >= str.length()) {
				more = false;
			}
			else {
				token.erase(token.find(m_delimiter));
				more = true;
			}
			token = trimString(token);


			if (newWidth < token.size()) {
				newWidth = token.size();
				m_widthField = newWidth;
			}
			if (more == false) {
				newWidth = 0;
			}
		}

		return token;

		
	}

	void Utilities::setDelimiter(char newDelimiter)
	{
		m_delimiter = newDelimiter;
	}

	char Utilities::getDelimiter()
	{
		return m_delimiter;
	}

	std::string trimString(std::string& obj)
	{
		bool quitLoop = false;
		while (!quitLoop) {
			if(obj[0] == ' ')
			{
				obj.erase(0, obj.find_first_not_of(' '));

			} 
			else if (obj[obj.length() - 1] == ' ')
			{
				obj.erase(obj.find_last_not_of(' ') + 1);
			}
			else {
				quitLoop = true;

			}
		}
		return obj;
		
	}


}