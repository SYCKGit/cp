#include <bits/stdc++.h>
using namespace std;
#define CURSOR
#define DEFAULT 0
typedef int SEGTYPE;

struct SegTree {
    int n;
    vector<SEGTYPE> a, seg;

    SegTree(int n)
        : n{n}, a(n), seg(4*n, DEFAULT) {}

    SegTree(vector<SEGTYPE> a)
        : n{(int)a.size()}, a{a}, seg(4*n) { build(0, n-1, 1); }

    SEGTYPE combine(SEGTYPE l, SEGTYPE r){
        CURSOR
    }

    void build(int l, int r, int pos){
        if (l == r){
            seg[pos] = a[l];
            return;
        }
        int mid = l + ((r-l) >> 1);
        build(l, mid, pos << 1);
        build(mid+1, r, (pos << 1) + 1);
        seg[pos] = combine(seg[pos << 1], seg[(pos << 1)+1]);
    }

    void update(int idx, SEGTYPE val){ return update(idx, val, 0, n-1, 1); }
    void update(int idx, SEGTYPE val, int l, int r, int pos){
        if (l == r){
            seg[pos] = a[idx] = val;
            return;
        }
        int mid = l + ((r-l) >> 1);
        if (idx <= mid)
            update(idx, val, l, mid, pos << 1);
        else
            update(idx, val, mid+1, r, (pos << 1) + 1);
        seg[pos] = combine(seg[pos << 1], seg[(pos << 1)+1]);
    }

    SEGTYPE query(int l, int r){ return query(l, r, 0, n-1, 1); }
    SEGTYPE query(int ql, int qr, int l, int r, int pos){
        if (qr < l || r < ql)
            return DEFAULT;
        if (ql <= l && r <= qr)
            return seg[pos];
        int mid = l + ((r-l) >> 1);
        return combine(query(ql, qr, l, mid, pos << 1), query(ql, qr, mid+1, r, (pos << 1)+1));
    }
};