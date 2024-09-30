// #define ONLINE_JUDGE
#include <bits/stdc++.h>
using namespace std;
#define int long long

// MACROS
// ALIASES
// DATA STRUCTURES
// ALGORITHMS
// MAIN

void solve(){
    
}

int32_t main(){
#ifdef ONLINE_JUDGE
    freopen("{problem name}.in", "r", stdin);
    freopen("{problem name}.out", "w", stdout);
#else
    auto begin = chrono::high_resolution_clock::now();
#endif
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    solve();
#ifndef ONLINE_JUDGE
    auto elapsed = chrono::duration_cast<chrono::nanoseconds>(chrono::high_resolution_clock::now() - begin);
    cout << "Time Taken : " << (elapsed.count() * 1e-9) << " seconds" << endl;
#endif
    return 0;
}