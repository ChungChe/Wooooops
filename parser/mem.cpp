#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <curl/curl.h>
#include <string>
#include <vector>
#include <sstream>

#include <Document.h>
#include <Selection.h>
#include <Node.h>

struct MemoryStruct {
    char *memory;
    size_t size;
};

static size_t WriteMemoryCallback(void *contents, size_t size, size_t nmemb, void *userp)
{
    size_t realsize = size * nmemb;
    struct MemoryStruct *mem = (struct MemoryStruct *)userp;

    mem->memory = (char*)realloc(mem->memory, mem->size + realsize + 1);
    if(mem->memory == NULL) {
        /* out of memory! */ 
        printf("not enough memory (realloc returned NULL)\n");
        return 0;
    }

    memcpy(&(mem->memory[mem->size]), contents, realsize);
    mem->size += realsize;
    mem->memory[mem->size] = 0;

    return realsize;
}

bool get_url(const std::string& url, std::string& data)
{
    CURL *curl_handle;
    CURLcode res;

    struct MemoryStruct chunk;

    chunk.memory = (char*)malloc(1);  /* will be grown as needed by the realloc above */ 
    chunk.size = 0;    /* no data at this point */ 

    curl_global_init(CURL_GLOBAL_ALL);
    curl_handle = curl_easy_init();
    curl_easy_setopt(curl_handle, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl_handle, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);
    curl_easy_setopt(curl_handle, CURLOPT_WRITEDATA, (void *)&chunk);
    curl_easy_setopt(curl_handle, CURLOPT_USERAGENT, "libcurl-agent/1.0");

    res = curl_easy_perform(curl_handle);
    bool ret = false;
    if(res != CURLE_OK) {
        fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
    }
    else {
        data = std::string(chunk.memory);
        ret = true;
    }

    curl_easy_cleanup(curl_handle);
    free(chunk.memory);
    curl_global_cleanup();

    return ret;
}

void get_sub(const std::string& data, const std::string& key, 
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

void get_all_titles(const std::string& data)
{
	std::vector<std::string> out;
	get_sub(data, std::string("h2[class=\"posttitle\"]"), out, false); 
	for (unsigned int i = 0; i < out.size(); ++i) {
		printf("%s\n", out[i].c_str());
	}
}

void get_info(const std::string& data)
{
	std::vector<std::string> out;
	get_sub(data, std::string("article.full-content"), out, true); 
	for (unsigned int i = 0; i < out.size(); ++i) {
		//printf("%s\n", out[i].c_str());
		get_all_titles(out[i]);
	}
}

int main(void)
{
    for (unsigned int i = 2; i < 3; ++i) {
        std::stringstream ss;
        ss << "http://latestjavstar.com/page/" << i;
        std::string data;
        if (!get_url(ss.str(), data)) {
            continue;
        }
		get_info(data);
    } 
    return 0;
}
