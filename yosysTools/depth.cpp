
#include <fstream>
#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <algorithm>
#include <random>
using namespace std;
mt19937 rand_generator;
int Max(int a,int b);
//argv[0] is the input file
int main(int argc, char *argv[]){
    string program[1000];
    ifstream dosyaOku(argv[1]);
    string satir = "";
    string satirlar[1000];
    int i=0;

    if ( dosyaOku.is_open() ){

        while ( getline(dosyaOku, satir) ){
            //cout << satir << endl;
            satirlar[i]=satir;
            i++;
        }

        dosyaOku.close();
    }

    for (int j = 0; j < 16; j++) {
        program[j]="x"+to_string(j);
    }
    int a=0;
    for (int j = 16; j < i+16; j++) {
        program[j]=satirlar[a];
        a++;
    }
    for (int j=0;j<i+16;j++){
        //cout<<program[j]<<endl;
    }
    int programsize=i+16;
    vector<string> tokens;
    int depth[1000];
    string intermediate;
    for (int j = 16; j < programsize; j++) {
        stringstream check2(program[j]);
        while (getline(check2, intermediate, ' ')) {
            tokens.push_back(intermediate);
        }
        string first=tokens[2].substr(0,1);
        string second=tokens[4].substr(0,1);
        if(first=="x"&&second=="x"){
            depth[j]=1;
        }else{
            if(first!="x"&&second!="x"){
                int index1=0;
                int index2=0;
                for (int k = j; k >15 ; k--) {
                    stringstream backCheck(program[k]);
                    string backInter;
                    vector<string> backTokens;
                    while (getline(backCheck, backInter, ' ')) {
                        backTokens.push_back(backInter);
                    }
                    if (backTokens[0]==tokens[2]){
                        index1=k;
                    }
                    if (backTokens[0]==tokens[4]){
                        index2=k;
                    }
                    backTokens.clear();
                }

                depth[j]=Max(depth[index1],depth[index2])+1;

            }else if(first!="x"){
                int index1=0;
                for (int k = j; k >15 ; k--) {
                    stringstream backCheck(program[k]);
                    string backInter;
                    vector<string> backTokens;
                    while (getline(backCheck, backInter, ' ')) {
                        backTokens.push_back(backInter);
                    }
                    if (backTokens[0]==tokens[2]){
                        index1=k;
                    }
                    backTokens.clear();
                }
                depth[j]=depth[index1]+1;
            }else{
                int index2=0;
                for (int k = j; k >15 ; k--) {
                    stringstream backCheck(program[k]);
                    string backInter;
                    vector<string> backTokens;
                    while (getline(backCheck, backInter, ' ')) {
                        backTokens.push_back(backInter);
                    }
                    if (backTokens[0]==tokens[4]){
                        index2=k;
                    }
                    backTokens.clear();
                }

                depth[j]=depth[index2]+1;
            }


        }
        tokens.clear();
    }
    cout<<programsize<<endl;
    //write to file appending
    ofstream dosyaYaz("/Users/mehmetalidemir/Desktop/C++_Araclar/devreler/dosya3.txt", ios::app);
    dosyaYaz<<"\n";
    for (int j = 16; j < programsize; j++) {
        cout<<satirlar[j-16]<<" ( "<<depth[j]<<" )"<<endl;
        dosyaYaz<<satirlar[j-16]<<" ( "<<depth[j]<<" )"<<endl;
    }

    return 0;
}
int Max(int a, int b)
{
    if(a>b)
        return a;
    else
        return b;
}

