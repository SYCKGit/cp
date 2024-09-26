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
#ifndef ONLINE_JUDGE
    auto begin = chrono::high_resolution_clock::now();
#endif
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int T = 1; cin >> T;
    for (int i = 1; i <= T; i++){
#ifndef ONLINE_JUDGE
        if (T != 1)
            cout << "Test Case #" << i << endl;
#endif
        solve();
    }
#ifndef ONLINE_JUDGE
    auto elapsed = chrono::duration_cast<chrono::nanoseconds>(chrono::high_resolution_clock::now() - begin);
    cout << "Time Taken : " << (elapsed.count() * 1e-9) << " seconds" << endl;
#endif
    return 0;
}