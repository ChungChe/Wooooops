#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <curl/curl.h>
#include <string>
#include <sstream>

#include <libxml/HTMLparser.h>
#include <libxml/HTMLtree.h>
#include <libxml/tree.h>
#include <libxml/parser.h>

struct MemoryStruct {
    char *memory;
    size_t size;
};

    static size_t
WriteMemoryCallback(void *contents, size_t size, size_t nmemb, void *userp)
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
void traverseTree(xmlNode* node)
{
    xmlNode *cur_node(NULL);
    xmlAttr* cur_attr(NULL);
    for (cur_node = node; cur_node; cur_node = cur_node->next) {
        /*
        std::string n(std::string(reinterpret_cast<const char*>(cur_node->name)));
        if (n != std::string("h2")) {
            continue;
        }
        */
        printf("Tag: %s\n", cur_node->name);
        for (cur_attr = cur_node->properties; cur_attr; cur_attr = cur_attr->next) {
            printf(" -> attribute: %s\n", cur_attr->name);
        }
        traverseTree(cur_node->children);
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

        htmlParserCtxtPtr parser = htmlCreatePushParserCtxt(NULL, NULL, NULL, 0, NULL, XML_CHAR_ENCODING_UTF8);
        htmlParseChunk(parser, data.c_str(), (int)data.size(), 0);
        traverseTree(xmlDocGetRootElement(parser->myDoc));
        //printf("data.size = %d\n", (int)data.size());
    } 
    return 0;
}
