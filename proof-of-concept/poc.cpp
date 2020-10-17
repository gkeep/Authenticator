#include <iostream>
#include <string>
#include <chrono> // Used for UNIX epoch
#include <cmath> // Used for `floor` function
#include <iomanip> // Used for conevrsion to HEX
#include <sstream> // Used for conevrsion to HEX

// #include <cryptopp/hmac.h> // HMAC algorithm
// #include <cryptopp/hex.h>
// #include <cryptopp/filters.h>
#include <cryptopp/sha.h>
#include <openssl/evp.h>
#include <openssl/hmac.h>
#include <cryptopp/base32.h>

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
u_int64_t getSteps(unsigned short period);


std::string getOTP(std::string token, u_int64_t timer, unsigned int digits);


// /*
//  * Hash the message through HMAC-SHA1 algorithm
//  *
//  * @param key Token secret.
//  */
// std::string getHash(std::string &key);

// /*
//  * Get binary value from hash
//  *
//  * @param hash Token hash
//  */
// int getVal(std::string hash);

std::string decodeBase32(std::string token);

int main(int argc, char *argv[])
{
    std::string label{}; // Token label, service or company name
    std::string secret{}; // Token secret, 32 HEX characters
    std::string account{}; // Token's account, email or username
    std::string issuer{}; // Token's issuer, company name
    std::string algorithm{}; // Algorithm used in token generation, SHA1 SHA256 SHA512, default is SHA1
    unsigned short digits{}; // Number of digits in token, 3-6
    unsigned short period{30}; // Interval in seconds (3-30), default is 30

    const std::string schema = argv[1]; // TOTP schema

    label = findParameter(schema, "label");
    secret = findParameter(schema, "secret");
    account = findParameter(schema, "account");
    issuer = findParameter(schema, "issuer");
    algorithm = findParameter(schema, "algorithm");
    digits = std::stoi(findParameter(schema, "digits")); // stoi = convert string to int
    period = std::stoi(findParameter(schema, "period"));

    // std::cout << "Full schema: " << schema << std::endl
    //     << "Label: " << label << std::endl
    //     << "Secret: "    << secret << std::endl
    //     << "Account: "   << account << std::endl
    //     << "Issuer: "    << issuer << std::endl
    //     << "Algorithm: " << algorithm << std::endl
    //     << "Digits: "    << digits << std::endl
    //     << "Period: "    << period << std::endl;

    // // Convert string to array of char
    // unsigned char *key = new unsigned char [20];
    // for (int i{}; i < 20; i++)
    //     key[i] = secret.c_str()[i];

    // std::string hash = getHash(secret);
    // std::cout << hash << std::endl;
    // std::cout << getVal(hash);

    std::cout << getOTP(decodeBase32(secret), getSteps(period), digits) << std::endl;
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

u_int64_t getSteps(unsigned short period)
{
    unsigned long int unix_time = std::chrono::duration_cast<std::chrono::seconds>(std::chrono::system_clock::now().time_since_epoch()).count();
    unsigned long int steps = floor(unix_time / period);

    return steps;
}

std::string decodeBase32(std::string token)
{
    std::string secret;

    int lookup[256];
    const byte ALPHABET[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";
    CryptoPP::Base32Decoder::InitializeDecodingLookupArray(lookup, ALPHABET, 32, true);

    CryptoPP::Base32Decoder decoder;
    CryptoPP::AlgorithmParameters params = CryptoPP::MakeParameters(CryptoPP::Name::DecodingLookupArray(),(const int *)lookup);
    decoder.IsolatedInitialize(params);
    decoder.Put((byte*)token.data(), token.length());
    decoder.MessageEnd();

    CryptoPP::word64 size = decoder.MaxRetrievable();
    if (size && size <= SIZE_MAX)
    {
        secret.resize(size);
        decoder.Get((byte*)secret.data(), secret.length());
    }

    return secret;
}

std::string getOTP(std::string token, u_int64_t timer, unsigned int digits)
/*
 * https://github.com/Skarlso/totp-generator/blob/master/totp/generator.cpp
 */
{
    std::string secretBytes = decodeBase32(token);

    secretBytes.erase(std::remove(secretBytes.begin(), secretBytes.end(), '\n'), secretBytes.end());
    unsigned char key[1024];

    for (int i = 0; i < secretBytes.length(); i++)
        key[i] = (unsigned char)secretBytes[i];

    int keylength = 0;
    for (int i = 0; key[i] != '\0'; i++)
        keylength++;

    unsigned char data[8];
    data[0] = (unsigned char)(timer >> 56);
    data[1] = (unsigned char)(timer >> 48);
    data[2] = (unsigned char)(timer >> 40);
    data[3] = (unsigned char)(timer >> 32);
    data[4] = (unsigned char)(timer >> 24);
    data[5] = (unsigned char)(timer >> 16);
    data[6] = (unsigned char)(timer >> 8);
    data[7] = (unsigned char)(timer);

    unsigned char* digest = nullptr;

    digest = HMAC(EVP_sha1(), key, keylength, (unsigned char*)data, sizeof(data), nullptr, nullptr);
    char mdString[41];
    for (int i = 0; i < 20; i++)
        sprintf(&mdString[i*2], "%02x", (unsigned char)digest[i]);

    int offset = digest[strlen((char*)digest)-1] & 0x0F;

	int value = (int)(((int(digest[offset]) & 0x7F) << 24) |
		((int(digest[offset+1] & 0xFF)) << 16) |
		((int(digest[offset+2] & 0xFF)) << 8) |
		(int(digest[offset+3]) & 0xFF));

    int mod = value % int(pow(10, digits));
    return std::to_string(mod);
}

int getVal(std::string hash)
{
    int offset = std::stoi(std::string(1, hash.back()), 0, 16); // Offset, last character of `hash` converted from HEX to INT
    std::cout << offset << std::endl;

    std::string holder{};
    // Starting from the offset, get the first 4 bytes from the `hash`
    for (int i{offset}; i <= offset+8; i++)
        holder.push_back(hash[i]);

    int result{};
    for (int i{}; i < 8; i+=2)
    {
        std::string temp{};
        temp.push_back(holder[i]);
        temp.push_back(holder[i+1]);

        std::cout << "before: " << temp << std::endl;

        int tempp{};
        // Apply binary operations
        if (i == 0)
            tempp += std::stoi(temp, 0, 16) & 0x7F;
        else
            tempp += std::stoi(temp, 0, 16) & 0xFF;

        std::cout << "after: " << tempp << std::endl;
        
        // // Convert INT to HEX
        // std::stringstream stream;
        // stream << std::hex << tempp;
        // result = std::stoi(stream.str(), 0, 16);

        // Append new nums
        result *= 100;
        result += tempp;
    }

    return result;
}