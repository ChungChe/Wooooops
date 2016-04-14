#include <stdio.h>
#include <stdlib.h>

#include <string>
#include <vector>
#include <sstream>
#include <map>
#include <algorithm>
#include "url_utility.h"
#include "html_parser.h"

void get_all_titles(const std::string& data, std::vector<std::string>& titles)
{
	std::vector<std::string> out;
    html_parser::get(data, std::string("h2[class=\"posttitle\"]"), out, false); 
	for (unsigned int i = 0; i < out.size(); ++i) {
		//printf("%s\n", out[i].c_str());
        titles.push_back(out[i]);
	}
}

void get_tags(const std::string& data, std::vector<std::string>& stars)
{
	std::vector<std::string> out;
    html_parser::get(data, std::string("span.tags"), out, true); 
	for (unsigned int i = 0; i < out.size(); ++i) {
        std::vector<std::string> star;
        html_parser::get(data, std::string("a[rel=\"tag\"]"), star, false); 
	    for (unsigned int j = 0; j < star.size(); ++j) {
            stars.push_back(star[j]);
        }
    }
}

enum e_special_pid {
    PID_1000GIRI,
    PID_HEYZO,
    PID_MURAMURA,
    PID_PACOPACOMAMA,
    PID_TOKYOHOT,
    PID_CARIB,
    PID_CARIBPR,
    PID_MESUBUTA,
    PID_1PON,
    PID_KIN8,
    PID_C0930
};

bool is_special_pid(const std::string& title)
{
    if (title.find('[') == 0) {
        return false;
    }
    if (title.find("1000giri") != std::string::npos) // DDDDDDNNN...
        return true;
    if (title.find("Heyzo") != std::string::npos) // DDDD
        return true;
    if (title.find("muramura") != std::string::npos) // DDDDDD_DDD
        return true;
    if (title.find("pacopacomama ") != std::string::npos) // DDDDDD_DDD
        return true;
    if (title.find("Tokyo Hot") != std::string::npos) // nDDDD or kDDDD
        return true;
    if (title.find("Caribbeancom ") != std::string::npos) // DDDDDD_DDD
        return true;
    if (title.find("caribbeancompr") != std::string::npos) // DDDDDD_DDD
        return true;
    if (title.find("Mesubuta") != std::string::npos)
        return true;
    if (title.find("1pondo") != std::string::npos)
        return true;
    if (title.find("10musume") != std::string::npos)
        return true;
    if (title.find("Kin8tengoku") != std::string::npos)
        return true;
    if (title.find("c0930") != std::string::npos)
        return true;
    //if (title.find("") != std::string::npos)
    //    return true;
    return false;
}

void find_special_pid(const std::string& title, const std::string& prefix, 
        std::string& pid)
{
    std::size_t pos = title.find(prefix);
    if (pos == std::string::npos) {
        return;
    }

}
void get_pid(const std::string& title, std::string& pid)
{
    std::size_t pos = title.find(']');
    if (pos == std::string::npos) {
        // special case !
        return;
    }
    pid = title.substr(1, pos - 1);
}

void get_info(const std::string& data)
{
    std::map<std::string, std::vector<std::string> > name2pid_map;
    std::map<std::string, std::vector<std::string> > pid2name_map;

	std::vector<std::string> out;
	html_parser::get(data, std::string("article.full-content"), out, true); 
	for (unsigned int i = 0; i < out.size(); ++i) {
		//printf("%s\n", out[i].c_str());
        std::vector<std::string> titles;
		get_all_titles(out[i], titles);

        for (unsigned j = 0; j < titles.size(); ++j) {
            std::string pid;
            get_pid(titles[j], pid);
            std::string upper = titles[j];
            std::transform(upper.begin(), upper.end(), upper.begin(), ::toupper);
            printf("upper: %s\n", upper.c_str());
            if (pid.empty()) {
                continue;
            }
            printf("%s\n", pid.c_str());
            int pid_length = pid.size() + 1;
            //printf("pid_length: %d\n", pid_length);
            //printf("title: %s\n", titles[j].c_str());
            std::string new_title = titles[j].substr(pid_length + 2, titles[j].size() - pid_length);

            printf("%s\n", new_title.c_str());
        }
        std::vector<std::string> stars;
        get_tags(out[i], stars);

        // store name to pid map
        // store pid to name map
    }
}

int main(void)
{
    for (unsigned int i = 1; i < 10; ++i) {
        std::stringstream ss;
        ss << "http://latestjavstar.com/page/" << i;
        std::string data;
        if (!url::get_data(ss.str(), data)) {
            continue;
        }
		get_info(data);
    } 
    return 0;
}
