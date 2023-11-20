// #define ONLINE_JUDGE
#define MEM_LIMIT 256
#include <bits/stdc++.h>
using namespace std;
#ifndef ONLINE_JUDGE
    #include <sys/resource.h>
#else
    #define endl '\n'
#endif
#define int long long
typedef vector<int> vi; typedef vector<vector<int>> vvi; typedef vector<bool> vb; typedef vector<vector<bool>> vvb; typedef pair<int, int> pii; typedef pair<int, pair<int, int>> pipii; typedef deque<int> di; typedef deque<deque<int>> ddi; typedef map<int, int> mii; typedef map<int, pair<int, int>> mipii; typedef map<pair<int, int>, int> mpiii;
const int mod = 1000000007; // 10^9 + 7

// MAIN CODE
void solve(){
    
}

int32_t main(){
#ifdef ONLINE_JUDGE
    freopen("{problem name}.in", "r", stdin);
    freopen("{problem name}.out", "w", stdout);
#endif
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
#ifndef ONLINE_JUDGE
    struct rlimit lim;
    lim.rlim_cur = lim.rlim_max = MEM_LIMIT*1'000'000;
    setrlimit(RLIMIT_AS, &lim);
    auto begin = std::chrono::high_resolution_clock::now();
#endif
    solve();
#ifndef ONLINE_JUDGE
    auto elapsed = std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::high_resolution_clock::now() - begin);
    cout << "Time Taken : " << (elapsed.count() * 1e-9) << " seconds" << endl;
#endif
    return 0;
}