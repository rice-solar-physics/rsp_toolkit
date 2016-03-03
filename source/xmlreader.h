// ****
// *
// * Header file for XML parser functions
// * 
// * Author: Will Barnes
// *
// * Date last modified: 16/12/2015
// *
// ****

#include <string>
#include <stdlib.h>
#include "../tinyxml2/tinyxml2.h"

tinyxml2::XMLElement * recursive_read(tinyxml2::XMLElement *, std::string);
tinyxml2::XMLElement * check_element(tinyxml2::XMLElement *, std::string);