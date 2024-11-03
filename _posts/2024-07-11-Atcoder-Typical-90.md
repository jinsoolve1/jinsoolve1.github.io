---
title: 
excerpt: Atcoder Typical 90 문제 풀이
categories:
  - Problem Solving
tags: 
permalink: 
toc: true
toc_sticky: true
date: 2024-07-11
last_modified_at: 2024-07-17
---

Atcoder Typical 90 문제들을 풀면서 인상깊었던 문제들만을 정리해 놓을 생각이다.

# 005 - Restricted Digits
$c_1 \sim c_k$ 의 한 자리수들로 N자리 문자를 만들었을 때 B의 배수의 갯수를 구하는 문제

## 풀이
n이 무지막지하게 크므로 무조건 $log_2(n)$을 만들어야 한다.  

처음에는 분할정복으로 `sol(길이 n, 값 val) := n자리 수로 mod B 했을 때 val이 되도록 하는 수의 갯수` 를 구해서 l과 r 로 반으로 나눠서 l의 값이 0~B-1 일 때 $l\_val \times 10^r + r\_val = val$ 이 나오도록 하는 r_val을 구해서 재귀적으로 해결한다고 생각했다.   
이때 시간복잡도는 $O(log(n) B^2)$으로 통과할 수 있어 보이지만 n 값이 크기 때문에 map으로 관리해줘야 하고 이로 인해서 인지 시간초과가 났다.  

결국 풀이를 보았는데 비슷하긴 하나 n을 $10^{18}$말고 최대 60자리의 이진수로 표현할 수 있다.   
n은 $10^{18}$이긴 하지만 2진수로 표현하면 60자리이다.   
이를 이용해 `dp[i][j]` := ($10^{2^i} * j$를 현재 c1~ck로 만들 수 있는 갯수) 를 의미한다.
이를 이용해 반복문으로 dp[0][c1~ck] = 1로 초기화해서 모든 반복문을 돌아보면 원하는 값을 구할 수 있다.

## 코드
```cpp
#include <bits/stdc++.h>  
  
#define endl "\n"  
#define all(v) (v).begin(), (v).end()  
#define For(i, n) for(int i=0; i<n; ++i)  
#define For1(i, n) for(int i=1; i<=n; ++i)  
#define For2(i, a, b) for(int i=(a); i<=(b); ++i)  
#define ft first  
#define sd second  
#define Get(i, v) get<i>(v)  
  
using namespace std;  
using ll = long long;  
using ld = long double;  
using pii = pair<int, int>;  
using pll = pair<ll, ll>;  
using ti3 = tuple<int, int, int>;  
using tl3 = tuple<ll, ll, ll>;  
  
const int INF = numeric_limits<int>::max();  
const ll LNF = numeric_limits<ll>::max();  
  
const int logmxn = 62, mxn = 1e3+1;  
const ll MOD = 1e9+7;  
  
ll N;  
int B, K;  
  
ll dp[logmxn][mxn];  
ll ans[logmxn][mxn];  
int pow10[logmxn];  
  
// a^b mod c  
ll pow(ll a, ll b, ll c) {  
    ll res = 1;  
    while(b) {  
        if(b%2) res = (res * a) % c;  
        a = (a * a) % c;  
        b >>= 1;  
    }  
    return res;  
}  
  
void solve() {  
    memset(dp,0,sizeof dp);  
    memset(ans, 0, sizeof ans);  
  
    cin >> N >> B >> K;  
    while(K--) {  
        int x; cin >> x;  
        dp[0][x%B]++;  
    }  
  
    for(int i=0; i<logmxn; i++) {  
        pow10[i] = (int)pow(10LL, 1LL << i, B);  
    }  
  
    for(int i=0; i<logmxn-1; i++) {  
        for(int j=0; j<B; j++) {  
            for(int k=0; k<B; k++) {  
                int nxt = (j*pow10[i] + k) % B;  
                dp[i+1][nxt] += dp[i][j]*dp[i][k];  
                dp[i+1][nxt] %= MOD;  
            }  
        }  
    }  
  
  
    ans[0][0] = 1;  
    for(int i=0; i<logmxn-1; i++) {  
        if((N & (1LL<<i)) == 0) {  
            for(int j=0; j<B; j++) ans[i+1][j] = ans[i][j];  
            continue;  
        }  
        for(int j=0; j<B; j++) {  
            for(int k=0; k<B; k++) {  
                int nxt = (j*pow10[i] + k) % B;  
                ans[i+1][nxt] += ans[i][j] * dp[i][k];  
                ans[i+1][nxt] %= MOD;  
            }  
        }  
    }  
  
    cout << ans[logmxn-1][0] << endl;  
}  
  
int main(void) {  
    ios_base::sync_with_stdio(false);  
    cin.tie(nullptr);  
    cout.tie(nullptr);  
  
    int tc = 1;  
//    cin >> tc;  
    while(tc--) {  
        solve();  
//        cout << solve() << endl;  
    }  
  
  
    return 0;  
}
```

# 006 - Smallest Subsequence
길이가 N인 문자열 S에서 길이가 K인 S의 부분열 중 사전순 가장 작은 것을 출력하는 문제.
여기서 부분열은 원래 문자열에서 0개 이상의 문자를 제거한 뒤 남은 문자의 순서대로 이어붙인 문자열을 뜻한다.

## 풀이1
처음에는 lis 알고리즘처럼 증가하는 부분수열을 찾을까 생각하다가 lis가 k보다 작다면 문제가 생겨서 포기했다.  
그 다음에는 segment tree를 이용해서 풀어보았다.  
1. start ~ n-k 중에서 가장 작은 문자와 그 문자의 index를 구한다. 그리고 해당 문자를 ans의 끝에 추가해준다.
2. 그 다음 start = index+1, k-- 시키고 다시 1번을 반복한다.
3. 이를 k가 0이 될 때까지 반복한다. 

위와 같이 풀면, k개의 부분문자열 중 가장 사전 순으로 낮은 부분열을 구할 수 있다.  
O(nlogn) 정도에 구할 수 있다.
### 코드1
```cpp
#include <bits/stdc++.h>

#define endl "\n"
#define all(v) (v).begin(), (v).end()
#define For(i, n) for(int i=0; i<n; ++i)
#define For1(i, n) for(int i=1; i<=n; ++i)
#define For2(i, a, b) for(int i=(a); i<=(b); ++i)
#define ft first
#define sd second
#define Get(i, v) get<i>(v)

using namespace std;
using ll = long long;
using ld = long double;
using pii = pair<int, int>;
using pll = pair<ll, ll>;
using ti3 = tuple<int, int, int>;
using tl3 = tuple<ll, ll, ll>;

const int INF = numeric_limits<int>::max();
const ll LNF = numeric_limits<ll>::max();

class Segment {
public:
    vector<pair<char,int>> tree; //tree[node] := a[start ~ end] 의 합

    Segment() {}
    Segment(int size) {
        this->resize(size);
    }
    void resize(int size) {
        size = (int) floor(log2(size)) + 2;
        size = pow(2, size);
        tree.resize(size, {numeric_limits<char>::max(), 0});
    }
    pair<char,int> sol(int node, int start, int end, int left, int right) {
        if(right < start || end < left) return {numeric_limits<char>::max(), 0};
        if(left <= start && end <= right) return tree[node];
        return min(sol(node * 2, start, (start + end) / 2, left, right),
                   sol(node * 2 + 1, (start + end) / 2 + 1, end, left, right));
    }
    void update(int node, int start, int end, int index, char value) {
        if(index < start || end < index) return;
        if(start == end) tree[node] = {value,index};
        else {
            update(node * 2, start, (start + end) / 2, index, value);
            update(node * 2 + 1, (start + end) / 2 + 1, end, index, value);
            tree[node] = min(tree[2*node], tree[2*node+1]);
        }
    }
};

void solve() {
    int n, k; cin >> n >> k;
    string s; cin >> s;
    Segment root(n);
    for(int i=0; i<n; i++) {
        root.update(1,0,n-1,i,s[i]);
    }

    string ans;
    int start=0;
    while(k) {
        auto [c,i] = root.sol(1,0,n-1,start,n-k);
        ans += c;
        start = i+1;
        k--;
    }
    cout << ans << endl;
}

int main(void) {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int tc = 1;
//    cin >> tc;
    while(tc--) {
        solve();
//        cout << solve() << endl;
    }


    return 0;
}
```
## 풀이2
그 다음에 해설을 찾아보니 O(n)만에 해결할 수 있었다.  
stack을 이용해서 풀이를 구하는 것이다. erase라는 변수를 0으로 초기화한다.  
stack의 top보다 들어오는 문자가 더 사전순으로 작다면 지울 수 있을 때까지 삭제해준다. 하지만 여기서 지울 때마다 erase++를 해준다. 하지만 우리는 k개의 부분열을 만들어야 하므로 erase는 최대 n-k 까지 할 수 있다.  
이를 이용해서 erase < n-k 일 동안만 stack을 오름차순으로 만들어주면 된다.  

### 코드2
```cpp
#include <bits/stdc++.h>

#define endl "\n"
#define all(v) (v).begin(), (v).end()
#define For(i, n) for(int i=0; i<n; ++i)
#define For1(i, n) for(int i=1; i<=n; ++i)
#define For2(i, a, b) for(int i=(a); i<=(b); ++i)
#define ft first
#define sd second
#define Get(i, v) get<i>(v)

using namespace std;
using ll = long long;
using ld = long double;
using pii = pair<int, int>;
using pll = pair<ll, ll>;
using ti3 = tuple<int, int, int>;
using tl3 = tuple<ll, ll, ll>;

const int INF = numeric_limits<int>::max();
const ll LNF = numeric_limits<ll>::max();

void solve() {
    int n,k; cin >> n >> k;
    string s; cin >> s;
    int erase=0;
    stack<char> st;
    for(char c : s) {
        while(!st.empty() && erase < n-k && st.top() > c) { st.pop(); erase++; }
        st.push(c);
    }
    string ans;
    while(!st.empty()) {
        ans += st.top();
        st.pop();
    }
    reverse(all(ans));
    cout << ans.substr(0,k) << endl;
}

int main(void) {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int tc = 1;
//    cin >> tc;
    while(tc--) {
        solve();
//        cout << solve() << endl;
    }


    return 0;
}
```
## 후기
stack 이 더 좋은 풀이인데 익숙한 segment부터 떠올렸다.  
stack이나 two-pointer 같은 기법도 한 번 정리해서 쭉 밀어봐야 할 것 같다.  

비슷한 문제로는 [백준 2812 - 크게 만들기](https://www.acmicpc.net/problem/2812)가 있다. 해당 문제는 3년 전에 stack으로 풀었는데 기억하지 못 한 걸 보니 재활이 필요한 듯 하다.