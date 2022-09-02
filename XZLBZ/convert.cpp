#include <bitset>
#include <iostream>
#include <vector>
using namespace std;
string hexToString(unsigned int a) {

    unsigned int b ;
    string binary ="";
    for (int i = 0; i < 32; i++)
    {
        b = a & (1 << i);
        if (b)
            binary += "1";
        else
            binary += "0";
    }
    cout << binary << endl;
    return binary;
}
//32 bit binary to hex
string binaryToHex(long long int binaryNum) {
    int hex=0, mul=1, chk=1, rem, i=0;
    char hexDecNum[20];
    while(binaryNum!=0)
    {
        rem = binaryNum%10;
        hex = hex + (rem*mul);
        if(chk%4==0)
        {
            if(hex<10)
                hexDecNum[i] = hex+48;
            else
                hexDecNum[i] = hex+55;
            mul = 1;
            hex = 0;
            chk = 1;
            i++;
        }
        else
        {
            mul = mul*2;
            chk++;
        }
        binaryNum = binaryNum/10;
    }
    if(chk!=1)
        hexDecNum[i] = hex+48;
    if(chk==1)
        i--;
    cout<<"\nEquivalent Value in Hexadecimal: ";
    for(i=i; i>=0; i--)
        cout<<hexDecNum[i];
    cout<<endl;
}
int main(int argc, char const *argv[])
{
    // unsigned int 32 to bit
    // unsigned int 32 to binary
    string binary[32];

    vector<unsigned int> m{
            0x01818080,
            0x81c14040,
            0x40602020,
            0x21311010,
            0x11190808,
            0x080c0404,
            0x04060202,
            0x02030101,
            0x80018180,
            0x4081c140,
            0x20406020,
            0x10213110,
            0x08111908,
            0x04080c04,
            0x02040602,
            0x01020301,
            0x80800181,
            0x404081c1,
            0x20204060,
            0x10102131,
            0x08081119,
            0x0404080c,
            0x02020406,
            0x01010203,
            0x81808001,
            0xc1404081,
            0x60202040,
            0x31101021,
            0x19080811,
            0x0c040408,
            0x06020204,
            0x03010102
    };
    for (int i = 0; i < 32; i++)
    {
        binary[i] = hexToString(m[i]);
    }



    binaryToHex(11111111111111111111);
    return 0;
}

