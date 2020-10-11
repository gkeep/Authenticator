#include <iostream>
#include <string>
#include <chrono> // Used for UNIX epoch
#include <cmath> // Used for `floor` function
#include <iomanip> // Used for conevrsion to HEX
#include <sstream> // Used for conevrsion to HEX

#include <cryptopp/hmac.h> // HMAC algorithm
#include <cryptopp/sha.h>
#include <cryptopp/hex.h>
#include <cryptopp/filters.h>

/*
 * Returns value of a specified parameter from initial schema
 *
 * @param schema Full TOTP schema
 * @param parameter Needed parameter
 */
std::string findParameter(std::string schema, std::string parameter);

/*
 * Returns HEX value of steps elapsed since UNIX epoch
 *
 * @param period Interval in seconds
 */
std::string getSteps(unsigned short &period);

int main()
/*
 * Hash the message through HMAC-SHA1 algorithm
 *
 * @param key Token secret.
 */
std::string getHash(std::string &key);
{
    /*
     * SCHEMA: otpauth://totp/ACME%20Co:john@example.com?secret=NYO2G5NPHL556J2HSF4AWOGFOZA3SRDR&issuer=ACME%20Co&algorithm=SHA1&digits=6&period=30
     */

    std::string label{}; // Token label, service or company name
    std::string secret{}; // Token secret, 32 HEX characters
    std::string account{}; // Token's account, email or username
    std::string issuer{}; // Token's issuer, company name
    std::string algorithm{}; // Algorithm used in token generation, SHA1 SHA256 SHA512, default is SHA1
    unsigned short digits{}; // Number of digits in token, 3-6
    unsigned short period{30}; // Interval in seconds (3-30), default is 30

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
    std::string message{getSteps(period)};
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

std::string getSteps(unsigned short &period)
{
    unsigned long int unix_time = std::chrono::duration_cast<std::chrono::seconds>(std::chrono::system_clock::now().time_since_epoch()).count();
    unsigned long int steps = floor(unix_time / period);

    std::stringstream stream;
    stream << std::hex << steps;
    std::string result(stream.str());
    return result;
}

std::string getHash(std::string &key)
/*
 * DOCS:
 * https://www.cryptopp.com/docs/ref/class_h_m_a_c.html
 * 
 * Implementation example:
 * https://github.com/transeos/trading_bot/blob/f109b2b7f9fb41ba432a8de082b2408c2eb6b693/lib/include/utils/EncodeDecode.h
 */
{
    std::string mac, hmac_hash;
    CryptoPP::SecByteBlock byteKey((const uint8_t*)key.data(), key.size());

    CryptoPP::HMAC<CryptoPP::SHA1> hash(byteKey, byteKey.size());

    CryptoPP::StringSource ss1(key, true, new CryptoPP::HashFilter(hash, new CryptoPP::StringSink(mac)));
    CryptoPP::StringSource ss2(mac, true, new CryptoPP::HexEncoder(new CryptoPP::StringSink(hmac_hash)));

    return hmac_hash;
}
