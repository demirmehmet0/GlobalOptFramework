//The source code of Paar's algorithm(Paar1-Paar2) in our framework is provided by the repository given in https://github.com/rub-hgi/shorter_linear_slps_for_mds_matrices
#include <iostream>
#include <stdlib.h>
#include <time.h>
#include <vector>
#include <fstream>
#include <cmath>
#include <math.h>
#include <ctype.h>
#include <stdio.h>
#include <string>
#include "random"

#define SIZE 16
#define TIME_LIMIT 90000
using namespace std;

struct Element
{
    int parent_i;
    int parent_j;
    int newDist[SIZE];
};
mt19937 rand_generator;
default_random_engine generator;
string file;
ifstream TheMatrix;
int global_best_xor_count, DIM;
const int MaxBaseSize = 1000;
const bool PRINTROWS = true;

int NumInputs;
int DepthLimit; // The depth bound of the output circuit
int NumMatrices;
int MaxDist;                // The number of 1s in the row of the matrix with the maximum number of 1s
int St;                     // sequence number of the matrices
long long int DepthNewBase; // depth of a new base which is used for calculating the new distances
int NumTargets;
int ProgramSize;
long long int Target[MaxBaseSize];
int Dist[MaxBaseSize];  // distance from current base to Target[i]
int NDist[MaxBaseSize]; // what Dist would be if NewBase is added
long long int Base[MaxBaseSize];
int BaseSize;
int TargetsFound;
char Result[MaxBaseSize][50];
int Res;
char *flag;
int Depth[MaxBaseSize];
int MaxDepth;

void InitBase();
void ReadTargetMatrix();
bool is_target(long long int x);
bool is_base(long long int x);
int NewDistance(int u); // calculate the distance from the base to Target[u]
int TotalDistance();    // returns the sum of distances to targets
bool reachablE(long long int T, int K, int S, long long int L);
bool EasyMove(); // if any two bases add up to a target, pick them
void PickNewBaseElementBP();
void binprint(long long int x); // output the last NumInputs bits of x

void PrintExpression(int No);
void PrintBase(void);
void PrintResult(bool, bool, char *, char *);
int Max(int a, int b);

int hamming_weight(uint64_t input)
{
    return __builtin_popcount(input & 0xffffffff) + __builtin_popcount((input >> 32) & 0xffffffff);
}

int paar_algorithm1(std::fstream *f, uint64_t *input_matrix)
{

    int xor_count = 0;
    uint64_t number_of_columns = DIM;
    int hw_max;
    int i_max = 0, j_max = 0;
    uint64_t tmp;
    int hw;
    uint64_t new_column;
    vector<pair<int, int> > program;

    // compute naive xor count
    for (uint64_t i = 0; i < DIM; i++)
    {
        xor_count += hamming_weight(input_matrix[i]);
    }
    xor_count -= DIM;
    *f << "Naive XOR count: " << xor_count << endl;
    cout << "Naive XOR count: " << xor_count << endl;
    *f << "SLP:" << endl<< endl;
    cout << "SLP:" << endl<< endl;

    do
    {
        hw_max = 0;
        for (uint64_t i = 0; i < number_of_columns; i++)
        {
            for (uint64_t j = i + 1; j < number_of_columns; j++)
            {
                tmp = input_matrix[i] & input_matrix[j];
                hw = hamming_weight(tmp);
                if (hw > hw_max)
                {
                    hw_max = hw;
                    i_max = i;
                    j_max = j;
                }
            }
        }
        if (hw_max > 1)
        {
            new_column = input_matrix[i_max] & input_matrix[j_max];
            input_matrix[number_of_columns] = new_column;
            input_matrix[i_max] = (new_column ^ ((1llu << DIM) - 1)) & input_matrix[i_max];
            input_matrix[j_max] = (new_column ^ ((1llu << DIM) - 1)) & input_matrix[j_max];
            xor_count -= (hw_max - 1);
            number_of_columns++;
            program.push_back(make_pair(i_max, j_max));
        }
    } while (hw_max > 1);

    int ctr = DIM;
    for (auto const &prog : program)
    {
        *f << "x" << ctr << " = x" << prog.first << " + x" << prog.second << endl;
        cout << "x" << ctr << " = x" << prog.first << " + x" << prog.second << endl;
        ctr++;
    }

    for (uint64_t i = 0; i < DIM; i++)
    {
        bool plus_flag = 0;
        *f << endl
           << "y" << i;
        cout << endl
             << "y" << i;
        for (uint64_t j = 0; j < number_of_columns; j++)
        {
            if ((input_matrix[j] & (1ll << (DIM - 1 - i))) != 0)
            {
                if (plus_flag == 0)
                {
                    *f << " = x" << j;
                    cout << " = x" << j;
                    plus_flag = 1;
                }
                else
                {
                    *f << " + x" << j;
                    cout << " + x" << j;
                }
            }
        }
    }

    *f << endl
       << endl;
    cout << endl
         << endl;
    return xor_count;
}

int paar_algorithm_2_recursive(std::fstream *f, uint64_t *input_matrix, int current_xor_count, int number_of_columns, vector<pair<int, int> > program)
{
    int xor_count_new;
    int xor_count_best = current_xor_count;
    int xor_count_tmp;
    uint64_t tmp;
    int hw_max;
    int hw;
    int i, j;
    uint64_t new_column;

    int i_max_list[1000];
    int j_max_list[1000];
    int list_end = 0;

    uint64_t *input_matrix_new;
    input_matrix_new = (uint64_t *)malloc((DIM + 200) * sizeof(uint64_t));

    hw_max = 0;
    for (i = 0; i < number_of_columns; i++)
    {
        for (j = i + 1; j < number_of_columns; j++)
        {
            tmp = input_matrix[i] & input_matrix[j];
            hw = hamming_weight(tmp);
            if (hw > hw_max)
            {
                hw_max = hw;
                i_max_list[0] = i;
                j_max_list[0] = j;
                list_end = 1;
            }
            else if ((hw == hw_max) && (hw != 1))
            {
                i_max_list[list_end] = i;
                j_max_list[list_end] = j;
                list_end++;
            }
        }
    }
    if (hw_max > 1)
    {
        for (i = 0; i < list_end; i++)
        {
            for (j = 0; j < number_of_columns; j++)
            {
                input_matrix_new[j] = input_matrix[j];
            }

            vector<pair<int, int> > program_new;
            for (auto const &prog : program)
            {
                program_new.push_back(prog);
            }

            new_column = input_matrix_new[i_max_list[i]] & input_matrix_new[j_max_list[i]];
            input_matrix_new[number_of_columns] = new_column;
            input_matrix_new[i_max_list[i]] = (new_column ^ ((1llu << DIM) - 1)) & input_matrix_new[i_max_list[i]];
            input_matrix_new[j_max_list[i]] = (new_column ^ ((1llu << DIM) - 1)) & input_matrix_new[j_max_list[i]];
            xor_count_new = current_xor_count - (hw_max - 1);
            program_new.push_back(make_pair(i_max_list[i], j_max_list[i]));
            xor_count_tmp = paar_algorithm_2_recursive(f, input_matrix_new, xor_count_new, number_of_columns + 1, program_new);
            if (xor_count_tmp < xor_count_best)
            {
                xor_count_best = xor_count_tmp;
            }
        }
    }

    free(input_matrix_new);

    if (xor_count_best < global_best_xor_count)
    {
        global_best_xor_count = xor_count_best;

        int ctr = DIM;
        for (auto const &prog : program)
        {
            *f << "x" << ctr << " = x" << prog.first << " + x" << prog.second << endl;
            cout << "x" << ctr << " = x" << prog.first << " + x" << prog.second << endl;
            ctr++;
        }

        for (int i = 0; i < DIM; i++)
        {
            int plus_flag = 0;
            *f << endl
               << "y" << i;
            cout << endl
                 << "y" << i;
            for (int j = 0; j < number_of_columns; j++)
            {
                if ((input_matrix[j] & (1ll << (DIM - 1 - i))) != 0)
                {
                    if (plus_flag == 0)
                    {
                        *f << " = x" << j;
                        cout << " = x" << j;
                        plus_flag = 1;
                    }
                    else
                    {
                        *f << " + x" << j;
                        cout << " + x" << j;
                    }
                }
            }
        }

        *f << endl
           << endl
           << "xor count (tmp) = " << global_best_xor_count << endl
           << endl
           << endl;
        cout << endl
             << endl
             << "xor count (tmp) = " << global_best_xor_count << endl
             << endl
             << endl;
    }

    return xor_count_best;
}

int paar_algorithm2(std::fstream *f, uint64_t *input_matrix)
{
    cout<<"paar_algorithm2"<<endl;
    int xor_count = 0;

    // compute naive xor count
    for (int i = 0; i < DIM; i++)
    {
        xor_count += hamming_weight(input_matrix[i]);
    }
    xor_count -= DIM;

    global_best_xor_count = xor_count;
    *f << "xor count (start) = " << global_best_xor_count << endl
       << endl;
    cout << "xor count (start) = " << global_best_xor_count << endl
         << endl;

    vector<pair<int, int> > program;

    xor_count = paar_algorithm_2_recursive(f, input_matrix, xor_count, DIM, program);
    
    return xor_count;
}

void ReadMatrix(uint64_t *input_matrix)
{
    int NumTargets, NumInputs;
    TheMatrix >> NumTargets;
    TheMatrix >> NumInputs;
    DIM = NumTargets;
    // check that NumInputs is < wordsize
    if (NumInputs >= 8 * sizeof(long long int))
    {
        cout << "too many inputs" << endl;
        exit(0);
    }
    int bit;
    long long int PowerOfTwo = pow(2.0, NumTargets - 1);
    for (int i = 0; i < NumTargets; i++)
    {
        TheMatrix.ignore(1, '[');
        for (int j = 0; j < NumInputs; j++)
        {
            TheMatrix >> bit;
            if (i == 0)
            {
                input_matrix[j] = 0;
            }
            if (bit)
            {
                input_matrix[j] += PowerOfTwo;
            }
        }
        PowerOfTwo = PowerOfTwo / 2;
        TheMatrix.get();
    }
}

int Threshold;
int main(int argc, char *argv[])
{

    int i;
    string mode;
    clock_t t1 = clock();
    if (argc < 3)
    {
        cout << "Yanlis kullanim!" << endl;
        return 0;
    }
    mode = argv[1];
    file = argv[2];
    cout << "File: " << file << endl;
    cout << "Mode: " << mode << endl;
    TheMatrix.open(file);
    NumMatrices = 1;
    if (mode.compare("boyar") == 0)
    {
        if (argc < 5)
        {
            TheMatrix >> Threshold;
            TheMatrix >> DepthLimit;
        }
        else
        {
            Threshold = strtol(argv[3], NULL, 10);
            DepthLimit = strtol(argv[4], NULL, 10);
        }
        bool print = true;
        if (argc >= 6)
        {
            print = strtol(argv[5], NULL, 10) == 1;
        }
        cout << "Threshold: " << Threshold << endl;
        cout << "DepthLimit: " << DepthLimit << endl;
        cout << "numMatrices: " << NumMatrices << endl;
        int numIter = 0;
        int limit = 0;

        for (i = 0; i < NumMatrices; i++)
        {

            ReadTargetMatrix();

            if (MaxDist + 1 > pow(2, DepthLimit))
                continue;
            InitBase();
            ProgramSize = 0;
            int counter = 0;
            St = i + 1;

            while (TargetsFound < NumTargets)
            {
                counter++;
                if (ProgramSize > Threshold)
                {
                    break;
                }
                if (mode.compare("boyar") == 0)
                {
                    if (!EasyMove())
                        PickNewBaseElementBP();
                }
            }

            if (ProgramSize <= Threshold && ProgramSize != 0)
                PrintResult(true, print, argv[4], "matrices/result/");
            else
                PrintResult(false, false, argv[4], "matrices/result/");
        }
        TheMatrix.close();
        cout << "program size: " << ProgramSize << endl;

        clock_t t2 = clock();
        cout << (t2 - t1) / (double)CLOCKS_PER_SEC;
    }
    else if ((mode.compare("paar1") == 0) || (mode.compare("paar2") == 0))
    {
        uint64_t *input_matrix;
        input_matrix = (uint64_t *)malloc((64 + 200) * sizeof(uint64_t));
        string filePath = file;

        string s;
        s.append("matrices/result/");
        s.append("result.");
        s.append(mode);
        s.append(".");
        // split filepath to get filename
        string filename = filePath.substr(filePath.find_last_of("/") + 1);
        s.append(filename);

        cout << "File: " << s << endl;
        std::fstream f(s, std::fstream::out);

        for (int i = 0; i < NumMatrices; i++)
        {
            ReadMatrix(input_matrix);
            int result;
            if (mode.compare("paar1") == 0)
            {
                result = paar_algorithm1(&f, input_matrix);
                f << "Paar1 XOR count:" << result << endl;
                cout << "Paar1 XOR count:" << result << endl;
            }
            else if (mode.compare("paar2") == 0)
            {
                result = paar_algorithm2(&f, input_matrix);
                f << "Paar2 XOR count:" << result << endl;
                cout << "Paar2 XOR count:" << result << endl;
            }
            f << endl
              << endl
              << endl;
            cout << endl
                 << endl
                 << endl;
        }
        f.close();
        free(input_matrix);
    }
    else if (mode.compare("sxor") == 0)
    {
        cout << "Yanlis kullanim!" << endl;
        return 0;
    }

    return 0;
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
        Base[i] = 2 * Base[i - 1];
        Depth[i] = 0;
    }
    BaseSize = NumInputs; // initial base is just the xi's, depths are 0
    for (int i = 0; i < NumTargets; i++)
        if (Dist[i] == 0)
        {
            TargetsFound++;
            // print the expression of the output and input
            for (int j = 0; j < NumInputs; ++j)
                if (Base[j] == Target[i])
                {
                    sprintf(Result[Res], "y%d = x%d  *  (0)\n", i, j);
                    ++Res;
                    break;
                }
        }
}

int TotalDistance()
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

long long int NewBase; // global variable containing a candidate new base

bool EasyMove()
{
    int t;
    bool foundone = false;

    // see if anything in the distance vector is 1
    for (int i = 0; i < NumTargets; i++)
        if (Dist[i] == 1)
        {
            foundone = true;
            t = i;
            break;
        }
    if (!foundone)
        return false;
    // update Dist array
    NewBase = Target[t];
    Base[BaseSize] = NewBase;
    BaseSize++;
    DepthNewBase = pow(2, DepthLimit);
    for (int i = 0; i < BaseSize; ++i)
        for (int j = i + 1; j < BaseSize; ++j)
            if (((Base[i] ^ Base[j]) == Base[BaseSize - 1]) && (DepthNewBase > pow(2, Max(i, j) + 1)))
            {
                DepthNewBase = pow(2, Max(i, j) + 1); // find the lowest depth of output signal i
            }

    for (int u = 0; u < NumTargets; u++)
        Dist[u] = NewDistance(u);
    ProgramSize++;
    // print the expression
    PrintExpression(t);
    TargetsFound++;
    return true;
} // EasyMove()

void PrintResult(bool fin, bool results, char *dpth, char *path)
{
    string filePath = file;
    string s;
    s.append(path);
    s.append("result.");
    s.append(dpth);
    s.append(".");
    filePath.replace(filePath.find("paar/"), 5, "");
    s.append(filePath);
    cout << "File: " << s << endl;
    std::fstream f(s, std::fstream::out | std::fstream::app);
    f << St << endl
      << endl;
      cout << St << endl
        << endl;
    if (!fin)
    {
        f << Threshold << "+" << endl
          << endl;
        cout << Threshold << "+" << endl
             << endl;
    }
    else
    {
        f << ProgramSize << endl
          << endl;
        cout << ProgramSize << endl
             << endl;

        if (results)
        {
            for (int i = 0; i < Res; ++i)
                f << Result[i];

            f << "Depth is " << MaxDepth << endl
              << endl;
            cout << "Depth is " << MaxDepth << endl
                 << endl;
        }
    }
}

int Max(int a, int b)
{
    if (Depth[a] > Depth[b])
        return Depth[a];
    else
        return Depth[b];
}

/* print the expression*/
void PrintExpression(int No)
{
    int i, j;

    for (i = 0; i < BaseSize; ++i)
        for (j = i + 1; j < BaseSize; ++j)
            if (((Base[i] ^ Base[j]) == Base[BaseSize - 1]) && (pow(2, Max(i, j) + 1) == DepthNewBase))
            {
                Depth[BaseSize - 1] = Max(i, j) + 1;
                if (Depth[BaseSize - 1] > MaxDepth)
                    MaxDepth = Depth[BaseSize - 1];
                flag = Result[Res];
                flag += sprintf(flag, "t%d = ", ProgramSize);
                if (i < NumInputs)
                    flag += sprintf(flag, "x%d + ", i);
                else
                    flag += sprintf(flag, "t%d + ", i - NumInputs + 1);
                if (j < NumInputs)
                    flag += sprintf(flag, "x%d *  y%d  (%d)\n", j, No, Depth[BaseSize - 1]);
                else
                    flag += sprintf(flag, "t%d *  y%d  (%d)\n", j - NumInputs + 1, No, Depth[BaseSize - 1]);
                ++Res;
                return;
            }
}

/* PickNewBaseElement is only called when there are no 1's in Dist[]*/
void PickNewBaseElementBP()
{
    int MinDistance;
    long long int TheBest;
    int ThisDist;
    int ThisNorm, OldNorm;
    int besti, bestj, d;
    bool easytarget;
    int BestDist[MaxBaseSize];

    MinDistance = BaseSize * NumTargets; // i.e. something big
    OldNorm = 0;                         // i.e. something small
    // try all pairs of bases
    for (int i = 0; i < BaseSize - 1; i++)
    {
        if (Depth[i] + 1 >= DepthLimit)
            continue;
        for (int j = i + 1; j < BaseSize; j++)
        {
            if (Depth[j] + 1 >= DepthLimit)
                continue;
            NewBase = Base[i] ^ Base[j];

            if (NewBase == 0)
            {
                cout << "a base is 0, should't happen " << endl;
                exit(0);
            }
            // if NewBase is not new continue
            if (is_base(NewBase))
                continue;
            // if NewBase is target then choose it
            easytarget = false;
            if (is_target(NewBase))
            {
                cout << "shouldn't find an easy target here " << endl;
                exit(0);
                easytarget = true;
                besti = i;
                bestj = j;
                TheBest = NewBase;
                break;
            }
            DepthNewBase = pow(2, Max(j, i) + 1);
            ThisDist = TotalDistance(); // this also calculates NDist[]
            if (ThisDist <= MinDistance)
            {
                // calculate Norm
                ThisNorm = 0;
                for (int k = 0; k < NumTargets; k++)
                {
                    d = NDist[k];
                    ThisNorm = ThisNorm + d * d;
                }
                // resolve tie in favor of largest norm
                if ((ThisDist < MinDistance) || (ThisNorm > OldNorm))
                {
                    besti = i;
                    bestj = j;
                    TheBest = NewBase;
                    for (int uu = 0; uu < NumTargets; uu++)
                        BestDist[uu] = NDist[uu];
                    MinDistance = ThisDist;
                    OldNorm = ThisNorm;
                }
            }
        }
        if (easytarget)
            break;
    }
    // update Dist array
    NewBase = TheBest;
    for (int i = 0; i < NumTargets; i++)
        Dist[i] = BestDist[i];
    // for (int i = 0; i < NumTargets; i++)
    // printf ("%d %d %d \n", besti, bestj, MinDistance);
    // std::cout<<"Press [ENTER] to continue\n";
    // std::cin.get();
    Base[BaseSize] = TheBest;
    Depth[BaseSize] = Max(besti, bestj) + 1;
    if (Depth[BaseSize] > MaxDepth)
        MaxDepth = Depth[BaseSize];
    BaseSize++;
    // output linear program
    ProgramSize++;
    // print the expression
    flag = Result[Res];
    flag += sprintf(flag, "t%d = ", ProgramSize);
    if (besti < NumInputs)
        flag += sprintf(flag, "x%d + ", besti);
    else
        flag += sprintf(flag, "t%d + ", besti - NumInputs + 1);
    if (bestj < NumInputs)
        flag += sprintf(flag, "x%d  (%d)\n", bestj, Depth[BaseSize - 1]);
    else
        flag += sprintf(flag, "t%d  (%d)\n", bestj - NumInputs + 1, Depth[BaseSize - 1]);
    ++Res;
    if (is_target(TheBest))
        TargetsFound++; // this shouldn't happen
} // PickNewBaseElement()

void binprint(long long int x)
{
    long long int t = x;
    for (int i = 0; i < NumInputs; i++)
    {
        if (t % 2)
            cout << "1 ";
        else
            cout << "0 ";
        t = t / 2;
    }
} // binprint

void PrintBase()
{
    int i;

    for (i = 0; i < BaseSize; ++i)
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
    // check that NumInputs is < wordsize
    if (NumInputs >= 8 * sizeof(long long int))
    {
        cout << "too many inputs" << endl;
        exit(0);
    }

    int bit;
    for (int i = 0; i < NumTargets; i++)
    // read row i
    {
        long long int PowerOfTwo = 1;
        Target[i] = 0;
        Dist[i] = -1; // initial distance from Target[i] is Hamming weight - 1
        TheMatrix.ignore(1, '[');
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
        if (Dist[i] > MaxDist)
            MaxDist = Dist[i];
        TheMatrix.get();
    }
}

bool is_target(long long int x)
{
    for (int i = 0; i < NumTargets; i++)
        if (x == Target[i])
            return true;
    return false;
}

bool is_base(long long int x)
{
    // sanity check, shouldn't ask if 0 is base
    if (x == 0)
    {
        cout << "asking if 0 is in Base " << endl;
        exit(0);
    }

    for (int i = 0; i < BaseSize; i++)
        if (x == Base[i])
            return true;
    return false;
}

int NewDistance(int u)
{

    if (Target[u] == 0)
        return 0;
    else
    {
        if (is_base(Target[u]) || (NewBase == Target[u]))
            return 0;

        if (reachablE(Target[u] ^ NewBase, Dist[u] - 1, 0, pow(2, DepthLimit) - DepthNewBase))
            return (Dist[u] - 1);
        else
            return Dist[u];
    }
}
// return true if T is the sum of K elements among Base[S..BaseSize-1]
bool reachablE(long long int T, int K, int S, long long int L)
{
    if ((BaseSize - S) < K)
        return false; // not enough base elements
    if (L < 1)
        return false;
    if (K == 0)
        return false; // this is probably not reached
    if (K == 1)
    {
        for (int i = S; i < BaseSize; i++)
            if ((T == Base[i]) && (pow(2, Depth[i]) <= L))
                return true;
        return false;
    }

    // consider those sums containing Base[S]
    if (reachablE(T ^ Base[S], K - 1, S + 1, L - pow(2, Depth[S])))
        return true;
    // consider those sums not containing Base[S]
    if (reachablE(T, K, S + 1, L))
        return true;
    // not found
    return false;
}
