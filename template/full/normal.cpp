#include <bits/stdc++.h>
using namespace std;
#ifdef ONLINE_JUDGE
    #define endl '\n'
#endif
#define int long long
#define all(x) x.begin(), x.end()
typedef long double ld; typedef vector<int> vi; typedef vector<vector<int>> vvi; typedef vector<bool> vb; typedef vector<vector<bool>> vvb; typedef pair<int, int> pii; typedef map<int, int> mii; typedef map<int, vector<int>> mivi;
const int mod = 1000000007; // 10^9 + 7
const int INF = 1e17;

// MAIN CODE
void solve(){
    
}

int32_t main(){
#ifndef ONLINE_JUDGE
    auto begin = chrono::high_resolution_clock::now();
#endif
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int T = 1;// cin >> T;
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