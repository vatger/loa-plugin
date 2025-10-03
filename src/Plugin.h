#pragma once

#pragma warning(push, 0)
#include "EuroScopePlugIn.h"
#pragma warning(pop)

#include <string>

namespace loa {
class LoaPlugin : public EuroScopePlugIn::CPlugIn {
   public:
    LoaPlugin();
    ~LoaPlugin();

    void DisplayMessage(const std::string &message, const std::string &sender = "LoaPlugin");
};
}  // namespace loa
