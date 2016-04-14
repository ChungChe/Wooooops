#ifndef _HTML_PARSER_H_
#define _HTML_PARSER_H_

#include <string>
#include <vector>

namespace html_parser {

void get(const std::string& data, const std::string& key, 
		std::vector<std::string>& sub_content, bool include_tag);
}

#endif
