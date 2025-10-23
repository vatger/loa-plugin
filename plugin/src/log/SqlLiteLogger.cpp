#include "SqlLiteLogger.h"

using namespace logging;

static const char __loggingTable[] =
    "CREATE TABLE messages( \
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, \
    location TEXT, \
    level INT, \
    message TEXT \
);";
static const std::string __insertMessage = "INSERT INTO messages VALUES (CURRENT_TIMESTAMP, @1, @2, @3)";

SqlLiteLogger::SqlLiteLogger() { this->createLogFile(generateLogFileName()); }

SqlLiteLogger::SqlLiteLogger(const std::filesystem::path& dirPath) {
    std::filesystem::path fullPath = dirPath / generateLogFileName();
    this->createLogFile(fullPath);
}

SqlLiteLogger::~SqlLiteLogger() {
    if (nullptr != this->m_database) sqlite3_close_v2(this->m_database);
}

void SqlLiteLogger::emitLog(const LoggerAsyncBase::LogMessage& logMsg) {
    sqlite3_stmt* stmt = nullptr;

    if (sqlite3_prepare_v2(this->m_database, __insertMessage.c_str(), -1, &stmt, nullptr) != SQLITE_OK) {
        return;
    }

    std::string sender = std::filesystem::path(logMsg.location.file_name()).filename().string();

    constexpr std::string_view prefix = "src\\";
    auto pos = sender.find(prefix);
    if (pos != std::string::npos) {
        sender = sender.substr(pos + prefix.size());
    }

    sender += ":" + std::to_string(logMsg.location.line());

    sqlite3_bind_text(stmt, 1, sender.c_str(), -1, SQLITE_TRANSIENT);
    sqlite3_bind_int(stmt, 2, static_cast<int>(logMsg.level));
    sqlite3_bind_text(stmt, 3, logMsg.message.c_str(), -1, SQLITE_TRANSIENT);

    if (sqlite3_step(stmt) != SQLITE_DONE) {
        return;
    }

    sqlite3_clear_bindings(stmt);
    sqlite3_reset(stmt);
    sqlite3_finalize(stmt);
}

void SqlLiteLogger::createLogFile(const std::filesystem::path& file) {
    sqlite3_open(file.string().c_str(), &this->m_database);
    sqlite3_exec(this->m_database, __loggingTable, nullptr, nullptr, nullptr);
    sqlite3_exec(this->m_database, "PRAGMA journal_mode = MEMORY", nullptr, nullptr, nullptr);
}