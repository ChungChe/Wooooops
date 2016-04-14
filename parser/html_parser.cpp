#include <Document.h>
#include <Selection.h>
#include <Node.h>
#include "html_parser.h"

namespace html_parser {

void get(const std::string& data, const std::string& key, 
		std::vector<std::string>& sub_content, bool include_tag)
{
	CDocument doc;
	doc.parse(data.c_str());
	CSelection s = doc.find(key);
	
	for (unsigned int i = 0; i < s.nodeNum(); ++i) {
		CNode node = s.nodeAt(i);
		if (include_tag) {
			sub_content.push_back(data.substr(node.startPos(), node.endPos() - node.startPos()));
		} else {
			sub_content.push_back(node.text());
		}
	}
}


}
