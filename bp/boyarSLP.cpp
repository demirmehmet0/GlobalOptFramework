/* This code is a modified version of Boyar's original implementation of the SLP heuristic*/
//The source code of BP algorithm in our framework is provided by the repository given in https://github.com/siweisun/involutory_mds/tree/master/Code_for_BoyarSLP

#include <math.h>
#include <ctype.h>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <time.h>
#include "random"
#include "array"
#include "algorithm"
#define SIZE 32
using namespace std;

const int MaxBaseSize=1000;
const bool PRINTROWS=true;
struct Element
{
    int parent_i;
    int parent_j;
    int newDist[SIZE];
};
int NumInputs;
int DepthLimit; //The depth bound of the output circuit
int NumMatrices;
int MaxDist; // The number of 1s in the row of the matrix with the maximum number of 1s
int St; //sequence number of the matrices
long long int DepthNewBase; //depth of a new base which is used for calculating the new distances
int NumTargets;
int ProgramSize;
uint64_t Target[MaxBaseSize];
uint64_t Dist[MaxBaseSize]; //distance from current base to Target[i]
int NDist[MaxBaseSize]; //what Dist would be if NewBase is added
long long int Base[MaxBaseSize];
int BaseSize;
int TargetsFound;
char Result[MaxBaseSize][50];
int  Res;
char *flag;
int Depth[MaxBaseSize];
int MaxDepth;

void InitBase();
void ReadTargetMatrix();
bool is_target(long long int x);
bool is_base(long long int x);
int NewDistance(int u); //calculate the distance from the base to Target[u]
int TotalDistance(); //returns the sum of distances to targets
bool reachablE(long long int T, int K, int S, long long int L);
bool EasyMove(); //if any two bases add up to a target, pick them
void PickNewBaseElement();
void binprint(long long int x); //output the last NumInputs bits of x

void PrintExpression(int No);
void PrintBase(void);
void PrintResult();
int Max(int a, int b);

ifstream TheMatrix;
mt19937 rand_generator;
default_random_engine generator;

vector<uint64_t> generate_p(int number)
{
	vector<uint64_t> B;
	vector<uint64_t> P;
	for(int j = 0; j < number; j++)
	{
		B.push_back(j);
	}
	
	while(B.size() > 0)
	{	
		uint64_t a = rand() % B.size();
		vector<uint64_t>::iterator iter = find(B.begin(), B.end(), B[a]);
		if(iter != B.end())
		{	
			P.push_back(B[a]);
			iter = B.erase(iter);
		}
		else
		{
			cout << "generate random permutation wrong!" << endl;
		}
	}
	
	return P;
}

vector<uint64_t> p_m_q(uint64_t *Target, uint64_t no_row, uint64_t no_col, uint64_t *Dist, vector<uint64_t> P, vector<uint64_t> Q)
{		
	vector<uint64_t> target_bar;
	vector<uint64_t> target_reuslt;

	uint64_t tmp_dis[16] = { 0 };
	//update Dist
	for(int i = 0; i < no_row; i++)
	{
		tmp_dis[i] = Dist[P[i]];
	}
	for(int i = 0; i < no_row; i++)
	{
		Dist[i] = tmp_dis[i];
	}

	for(int i = 0; i < no_row; i++)
	{	
		uint64_t sum = 0;
		for(uint64_t j = 0; j < no_col; j++)
		{	
			sum = sum + (((Target[i] >> Q[j]) & 1ull) << j);
		}
		target_bar.push_back(sum);
	}

	for(int j = 0; j < no_row; j++)
	{
		target_reuslt.push_back(target_bar[P[j]]);
	}

	for(int j = 0; j < no_row; j++)
	{
		Target[j] = target_reuslt[j];
	}

	return target_reuslt;
}

int
main(int argc, char *argv[])
{
    int Threshold;
    int BFI = 0;
    int  i;

    clock_t t1=clock();
    TheMatrix.open("");

    NumMatrices = 1;
    Threshold = 0;
    DepthLimit = 0;
    for (i = 0; i < NumMatrices; i++)
    {
        ReadTargetMatrix();
        if(BFI == 1){
            vector<uint64_t> P;
            vector<uint64_t> Q;
            P = generate_p(NumTargets);
            Q = generate_p(NumInputs);
            p_m_q(Target, NumTargets, NumInputs, Dist, P, Q);
        }

        if (MaxDist + 1 > pow(2, DepthLimit)) continue;
        InitBase();
        ProgramSize = 0;
        int counter = 0;
        St = i+1;
        while (TargetsFound < NumTargets)
        {
            counter++;
            if(ProgramSize > Threshold)
            {
                break;
            }
            if (!EasyMove()) PickNewBaseElement();
        }

        if(ProgramSize <= Threshold)
            PrintResult();
        else
            printf("Out of threshold\n\n");

    }

    clock_t t2=clock();
    std::cout << (t2-t1)/(double)CLOCKS_PER_SEC<<endl;
}

void InitBase()
{
    TargetsFound = 0;
    Res = 0;
    Base[0] = 1;
    Depth[0] = 0;
    MaxDepth = 0;
    for (int i = 1; i < NumInputs; i++)
    {
        Base[i] = 2*Base[i-1];
        Depth[i] = 0;
    }
    BaseSize = NumInputs; //initial base is just the xi's, depths are 0
    for (int i = 0; i < NumTargets; i++)
        if (Dist[i] == 0)
        {
            TargetsFound++;
            //print the expression of the output and input
            for(int j = 0; j < NumInputs; ++j)
                if(Base[j] == Target[i])
                {
                    sprintf(Result[Res], "y%d = x%d  *  (0)\n", i, j);
                    ++Res;
                    break;
                }
        }
}

int TotalDistance() //returns the sum of distances to targets
{
    int D = 0;
    int t;
    for (int i = 0; i < NumTargets; i++)
    {
        t = NewDistance(i);
        NDist[i] = t;
        D = D + t;
    }
    return D;
}

long long int NewBase; //global variable containing a candidate new base

bool EasyMove()
{
    int t;
    bool foundone = false;

    //see if anything in the distance vector is 1
    for(int i = 0; i < NumTargets; i++)
        if (Dist[i] == 1)
        {
            foundone = true;
            t = i;
            break;
        }
    if (!foundone) return false;
    //update Dist array
    NewBase = Target[t];
    Base[BaseSize] = NewBase;
    BaseSize++;
    DepthNewBase = pow(2, DepthLimit);
    for(int i = 0; i < BaseSize; ++i)
        for(int j = i + 1; j < BaseSize; ++j)
            if(((Base[i] ^ Base[j]) == Base[BaseSize - 1]) && (DepthNewBase > pow(2, Max(i,j)+1)))
            {
                DepthNewBase = pow(2, Max(i,j)+1); //find the lowest depth of output signal i
            }


    for (int u = 0; u < NumTargets; u++) Dist[u] = NewDistance(u);
    ProgramSize++;
    //print the expression
    PrintExpression(t);
    TargetsFound++;
    return true;
} //EasyMove()

void PrintResult()
{
    std::fstream f("", std::fstream::out | std::fstream::app);
    f << St << endl << endl;
    cout << St << endl << endl;
    f << ProgramSize << endl << endl;
    cout<<"ProgramSize: "<<ProgramSize<< " and Depth is " << MaxDepth << endl;
    for(int i = 0; i < Res; ++i){
        f << Result[i] ;
        cout << Result[i] ;
    }
    f << "Depth is " << MaxDepth << endl << endl;
    cout << "Depth is " << MaxDepth << endl << endl;
}

int Max(int a, int b)
{
    if(Depth[a] > Depth[b])
        return Depth[a];
    else
        return Depth[b];
}

/* print the expression*/
void PrintExpression(int No)
{
    int i, j;

    for(i = 0; i < BaseSize; ++i)
        for(j = i + 1; j < BaseSize; ++j)
            if(((Base[i] ^ Base[j]) == Base[BaseSize-1]) && (pow(2, Max(i,j)+1) == DepthNewBase))
            {
                Depth[BaseSize-1] = Max(i,j)+1;
                if(Depth[BaseSize-1] > MaxDepth)
                    MaxDepth = Depth[BaseSize-1];
                flag = Result[Res];
                flag += sprintf(flag, "t%d = ", ProgramSize);
                if(i < NumInputs)
                    flag += sprintf(flag, "x%d + ", i);
                else
                    flag += sprintf(flag, "t%d + ", i - NumInputs + 1);
                if(j < NumInputs)
                    flag += sprintf(flag, "x%d *  y%d  (%d)\n", j, No, Depth[BaseSize-1]);
                else
                    flag += sprintf(flag, "t%d *  y%d  (%d)\n", j - NumInputs + 1, No, Depth[BaseSize-1]);
                ++Res;
                return;
            }
}

/* PickNewBaseElement is only called when there are no 1's in Dist[]*/
void PickNewBaseElement()
{
    int MinDistance;
    long long int TheBest;
    long long int TheBestArray[MaxBaseSize*NumTargets];
    int ThisDist;
    int ThisNorm, OldNorm;
    int besti,bestj, d;
    bool easytarget;
    int BestDist[MaxBaseSize];
    Element* AllElements = new Element[BaseSize*(BaseSize-1)];
    int counter = 0;
    int count2=0;
    MinDistance = BaseSize*NumTargets; //i.e. something big
    OldNorm = 0; //i.e. something small
    //try all pairs of bases
    for (int i = 0; i < BaseSize - 1; i++)
    {
        if (Depth[i] + 1 >= DepthLimit) continue;
        for (int j = i+1; j < BaseSize; j++)
        {
            if (Depth[j] + 1 >= DepthLimit) continue;
            NewBase = Base[i] ^ Base[j];

            if (NewBase == 0) { cout << "a base is 0, should't happen " << endl; exit(0); }
            //if NewBase is not new continue
            if (is_base(NewBase)) continue;
            //if NewBase is target then choose it
            easytarget = false;
            if (is_target(NewBase))
            {
                cout << "shouldn't find an easy target here " << endl;
                exit(0);
            }
            DepthNewBase = pow(2, Max(j,i)+1);
            ThisDist = TotalDistance(); //this also calculates NDist[]
            if (ThisDist <= MinDistance)
            {
                //calculate Norm
                ThisNorm = 0;
                for (int k = 0; k < NumTargets; k++)
                {
                    d = NDist[k];
                    ThisNorm = ThisNorm + d*d;
                }
                //resolve tie in favor of largest norm
                if ((ThisDist < MinDistance) || (ThisNorm > OldNorm) )
                {
                    if (counter>3)
                        counter=0;
                    AllElements[counter].parent_i=i;
                    AllElements[counter].parent_j=j;
                    for (int uu = 0; uu < NumTargets; uu++) AllElements[counter].newDist[uu] = NDist[uu];
                    TheBestArray[counter]=NewBase;
                    MinDistance = ThisDist;
                    OldNorm = ThisNorm;
                    counter++;
                    count2++;
                }
            }
        }
        if (easytarget) break;
    }


/*
    array<double,3> intervals ={0.0,(float)(counter-1),(float)(counter-1)};
    array<double,3> weights = {0.0, 10.0, 10.0};
    piecewise_linear_distribution<double>
            distribution (intervals.begin(),intervals.end(),weights.begin());
    int number = distribution(generator);
    */
    rand_generator.seed(time(0));
    uniform_int_distribution<int> rand_distribution(0,counter-1);
    int number = rand_distribution(rand_generator);
    if(counter==0||counter==1)
        number=0;
    if(counter==2&&count2==2)
        number=1;
    if(counter==3&&count2==3)
        number=2;
    besti = AllElements[number].parent_i;
    bestj = AllElements[number].parent_j;
    TheBest = TheBestArray[number];
    for (int uu = 0; uu < NumTargets; uu++) BestDist[uu] = AllElements[number].newDist[uu];


    //update Dist array
    NewBase = TheBest;
    for (int i = 0; i < NumTargets; i++) Dist[i] = BestDist[i];
    //for (int i = 0; i < NumTargets; i++)
    //printf ("%d %d %d \n", besti, bestj, MinDistance);
    //std::cout<<"Press [ENTER] to continue\n";
    //std::cin.get();
    Base[BaseSize] = TheBest;
    Depth[BaseSize] = Max(besti, bestj) + 1;
    if(Depth[BaseSize] > MaxDepth)
        MaxDepth = Depth[BaseSize];
    BaseSize++;
    //output linear program
    ProgramSize++;
    //print the expression
    flag = Result[Res];
    flag += sprintf(flag, "t%d = ", ProgramSize);
    if(besti < NumInputs)
        flag += sprintf(flag, "x%d + ", besti);
    else
        flag += sprintf(flag, "t%d + ", besti - NumInputs + 1);
    if(bestj < NumInputs)
        flag += sprintf(flag, "x%d  (%d)\n", bestj, Depth[BaseSize-1]);
    else
        flag += sprintf(flag, "t%d  (%d)\n", bestj - NumInputs + 1, Depth[BaseSize-1]);
    ++Res;
    if (is_target(TheBest)) TargetsFound++; //this shouldn't happen
} //PickNewBaseElement()

void binprint(long long int x) //outputs last NumInputs bits of x
{
    long long int t = x;
    for (int i = 0; i < NumInputs; i++)
    {
        if (t%2) cout << "1 "; else cout << "0 ";
        t = t/2;
    }
} //binprint

void PrintBase()
{
    int i;

    for(i = 0; i < BaseSize; ++i)
    {
        binprint(Base[i]);
        printf("\n");
    }
}

void ReadTargetMatrix()
{
    TheMatrix >> NumTargets;
    TheMatrix >> NumInputs;
    MaxDist = 0;
    //check that NumInputs is < wordsize
    if (NumInputs >= 8*sizeof(long long int))
    {
        cout << "too many inputs" << endl;
        exit(0);
    }

    int bit;
    for (int i = 0; i < NumTargets; i++)
        //read row i
    {
        long long int PowerOfTwo  = 1;
        Target[i] = 0;
        Dist[i] = -1; //initial distance from Target[i] is Hamming weight - 1

        for (int j = 0; j < NumInputs; j++)
        {
            TheMatrix >> bit;
            if (bit)
            {
                Dist[i]++;
                Target[i] = Target[i] + PowerOfTwo;
            }
            PowerOfTwo = PowerOfTwo * 2;
        }
        if (Dist[i] > MaxDist) MaxDist = Dist[i];
        TheMatrix.get();
    }
}


bool is_target(long long int x)
{
    for (int i = 0; i < NumTargets; i++)
        if (x == Target[i]) return true;
    return false;
}

bool is_base(long long int x)
{
    //sanity check, shouldn't ask if 0 is base
    if (x==0) { cout << "asking if 0 is in Base " <<endl ; exit(0); }

    for (int i = 0; i < BaseSize; i++) if (x == Base[i]) return true;
    return false;
}



int NewDistance(int u)
{

    if (Target[u] == 0) return 0;
    else
    {
        if (is_base(Target[u]) || (NewBase == Target[u])) return 0;



        if (reachablE(Target[u] ^ NewBase, Dist[u]-1, 0, pow(2, DepthLimit) - DepthNewBase)) return (Dist[u]-1);
        else return Dist[u];
    }
}


//return true if T is the sum of K elements among Base[S..BaseSize-1]
bool reachablE(long long int T, int K, int S, long long int L)
{
    if ((BaseSize-S) < K) return false; //not enough base elements
    if (L < 1) return false;
    if (K==0) return false; //this is probably not reached
    if (K==1)
    {
        for (int i=S; i < BaseSize; i++) if ((T == Base[i]) && (pow(2, Depth[i]) <= L)) return true;
        return false;
    }

    //consider those sums containing Base[S]
    if (reachablE(T^Base[S], K-1, S+1, L - pow(2, Depth[S]))) return true;
    //consider those sums not containing Base[S]
    if (reachablE(T, K, S+1, L)) return true;
    //not found
    return false;
}
