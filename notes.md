[bash-totp](https://github.com/jakwings/bash-totp)

[google authenticator docs](https://github.com/google/google-authenticator/wiki/Key-Uri-Format)

[demo with test schema](https://rootprojects.org/authenticator/)

[IOTA tutorial 34: Time-Based One-Time Password (TOTP)](https://www.youtube.com/watch?v=VOYxF12K1vE)


### Algorithm:

1. Get `N`, number of time steps elapsed since UNIX time
    `N = floor(Tu / period)`, `Tu` is UNIX Time, `period` is interval in seconds (3-30)

2. Convert `N` into HEX, the hex value *must* have 16 characters (prepend with 0, if needed)

3. Convert the HEX value into a 8 bytes array and assign the value to var `message`.

4. Convert the `secret` into a 20 bytes array and assign the value to var `key`.

5. Put `message` and `key` through the `algorithm` (SHA-1) to get `hash`

6. Get last 4 bits of `hash` and get its integer value - `offset`

7. Starting from the offset, get the first 4 bytes from the `hash`

8. Apply a binary operation for each byte: `0x7F` for first and `0xFF` for others

9. Convert binary value to an integer - `val`

10. Calculate the `token`: `val % 10^n`
    `n` - amount of `digits`

    If token size (`digits`) < `n`, prefix the `token` with 0's.