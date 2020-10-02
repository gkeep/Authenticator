#include <iostream>

std::string findParameter(std::string schema, std::string parameter);

int main()
{
    /*
     * SCHEMA: otpauth://totp/ACME%20Co:john@example.com?secret=NYO2G5NPHL556J2HSF4AWOGFOZA3SRDR&issuer=ACME%20Co&algorithm=SHA1&digits=6&period=30
     */

    std::string label{}; // ex. "ACME%20Co"
    std::string secret{}; // ex. "NYO2G5NPHL556J2HSF4AWOGFOZA3SRDR"
    std::string account{}; // ex. "john@example.com"
    std::string issuer{}; // ex. "ACME%20Co"
    std::string algorithm{}; // ex. SHA1
    unsigned short digits{};
    unsigned period{30}; // interval in seconds, 3-30, 30 by default

    std::string schema{"otpauth://totp/ACME%20Co:john@example.com?secret=NYO2G5NPHL556J2HSF4AWOGFOZA3SRDR&issuer=ACME%20Co&algorithm=SHA1&digits=6&period=30"};

    std::cout << "Full schema: " << schema << std::endl;
    std::cout << std::endl << "Label: " << findParameter(schema, "label") << std::endl
        << "Secret: " << findParameter(schema, "secret") << std::endl
        << "Account: " << findParameter(schema, "account") << std::endl
        << "Issuer: " << findParameter(schema, "issuer") << std::endl
        << "Algorithm: " << findParameter(schema, "algorithm") << std::endl
        << "Digits: " << findParameter(schema, "digits") << std::endl;
}

std::string findParameter(std::string schema, std::string parameter)
{
    unsigned short start{}, end{};

    if (parameter == "label")
    {
        schema = schema.erase(0, schema.find("//"));

        start = schema.find("//") + 7;
        end = schema.find(":") - start;
    }
    else if (parameter == "account")
    {
        // truncate everything before label, since it has a ':'
        schema = schema.erase(0, 15);

        start = schema.find(":") + 1;
        end = schema.find("?") - start;
    }
    else
    {
        // truncate everything before parameter
        schema = schema.erase(0, schema.find(parameter));

        start = schema.find(parameter) + parameter.length() + 1; // +1 to compensate for '='
        end = schema.find("&") - start;
    }

    std::string param = schema.substr(start, end);

    return param;
}
