#pragma once

#define CURL_STATICLIB 1
#include <curl/curl.h>

#include <memory>
#include <mutex>

#include "IRestClient.h"
#include "log/ILogger.h"

namespace api {
class CurlRestClient : public interfaces::IRestClient {
   private:
    std::shared_ptr<logging::ILogger> m_logger;

   public:
    CurlRestClient(std::shared_ptr<logging::ILogger> logger);
    ~CurlRestClient();

    interfaces::HttpResponse get(const std::string& url,
                                 const std::map<std::string, std::string>& headers = {}) override;
    interfaces::HttpResponse post(const std::string& url, const std::string& body,
                                  const std::map<std::string, std::string>& headers = {}) override;
    interfaces::HttpResponse put(const std::string& url, const std::string& body,
                                 const std::map<std::string, std::string>& headers = {}) override;
    interfaces::HttpResponse patch(const std::string& url, const std::string& body,
                                   const std::map<std::string, std::string>& headers = {}) override;
    interfaces::HttpResponse del(const std::string& url,
                                 const std::map<std::string, std::string>& headers = {}) override;

   private:
    struct Communication {
        std::mutex lock;
        CURL* socket;

        Communication() : lock(), socket(curl_easy_init()) {}
    };
    Communication m_getRequest;
    Communication m_postRequest;
    Communication m_putRequest;
    Communication m_patchRequest;
    Communication m_deleteRequest;
};

}  // namespace api