#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
    long long int a = atol(argv[1]);
    long long int b = 0;
    long long int c = 0;

    do
    {
        // b is a truncated to 3 least significant bits and inverted
        b = a % 8;
        b ^= 7;
        // printf("b = %lld\n", b);

        //
        c = a / (1 << b);
        // c = a >> b;

        // printf("c = %lld\n", c);

        a = a / 8;
        // a = a >> 3;

        b ^= c;
        b ^= 7;

        // printf("b = %lld\n", b);

        printf("%lld,", b % 8);
    } while (a != 0);
}