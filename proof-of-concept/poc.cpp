#include <iostream>
#include <string>

std::string findParameter(std::string schema, std::string parameter);

int main()
{
    /*
     * SCHEMA: otpauth://totp/ACME%20Co:john@example.com?secret=NYO2G5NPHL556J2HSF4AWOGFOZA3SRDR&issuer=ACME%20Co&algorithm=SHA1&digits=6&period=30
     */

    std::string label{}; // ex. "ACME%20Co"
    std::string secret{}; // ex. "NYO2G5NPHL556J2HSF4AWOGFOZA3SRDR"
    std::string account{}; // ex. "john[at]example.com"
    std::string issuer{}; // ex. "ACME%20Co"
    std::string algorithm{}; // ex. SHA1
    unsigned short digits{};
    unsigned short period{30}; // interval in seconds (3-30), 30 by default

    std::string schema{"otpauth://totp/ACME%20Co:john@example.com?secret=NYO2G5NPHL556J2HSF4AWOGFOZA3SRDR&issuer=ACME%20Co&algorithm=SHA1&digits=6&period=30"};

    std::cout << "Full schema: " << schema << std::endl;

    label = findParameter(schema, "label");
    secret = findParameter(schema, "secret");
    account = findParameter(schema, "account");
    issuer = findParameter(schema, "issuer");
    algorithm = findParameter(schema, "algorithm");
    digits = std::stoi(findParameter(schema, "digits")); // stoi = convert string to int
    period = std::stoi(findParameter(schema, "period"));

    std::cout << std::endl << "Label: " << label << std::endl
        << "Secret: "    << secret << std::endl
        << "Account: "   << account << std::endl
        << "Issuer: "    << issuer << std::endl
        << "Algorithm: " << algorithm << std::endl
        << "Digits: "    << digits << std::endl
        << "Period: "    << period << std::endl;
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

        start = schema.find(":") + 1; // +1 to compensate for '='
        end = schema.find("?") - start;
    }
    else
    {
        // truncate everything before parameter
        schema = schema.erase(0, schema.find(parameter));

        start = schema.find(parameter) + parameter.length() + 1;
        end = schema.find("&") - start;
    }

    std::string param = schema.substr(start, end);

    return param;
}
