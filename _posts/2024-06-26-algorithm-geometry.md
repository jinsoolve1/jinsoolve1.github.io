---
title: 기하학
excerpt: 기하학
categories:
  - Algorithm Theory
tags: []
permalink: /algorithm/geometry/
toc: true
toc_sticky: true
date: 2024-06-24
last_modified_at: 2024-08-01
---

# Convex Hull
볼록 껍질
## 회전하는 캘리퍼스(Rotating Calipers)
참고: https://stonejjun.tistory.com/42
i -> ni 와 j->nj 가 있다고 하자. 둘의 ccw가 음수가 되기 시작하는 점 j가 점 i로부터 가장 먼 점이다.

```cpp
#include <iostream>
#include <algorithm>
#include <cmath>
#include <utility>
#include <string>
#include <cstring>
#include <vector>
#include <tuple>
#include <stack>
#include <queue>
#include <deque>
#include <list>
#include <map>
#include <unordered_map>
#include <climits>

#define INF 987654321
#define INF2 2147483647
#define all(v) (v).begin(), (v).end()

using namespace std;
using ll = long long;
using pii = pair<int, int>;
using ti3 = tuple<int, int, int>;

struct Point {
    ll x, y;

    Point() {}
    Point(ll _x, ll _y) : x(_x), y(_y) {}
    ll cross(Point other) {
        return x*other.y - y*other.x;
    }
    ll crossSign(Point other) {
        ll res = this->cross(other);
        if(res > 0) return 1;
        else if(res < 0) return -1;
        return 0;
    }
    ll dist(Point other) {
        return pow(x-other.x,2) + pow(y-other.y,2);
    }
    Point operator-(Point other) const {
        return Point(x-other.x, y-other.y);
    }
    bool operator<(Point other) const {
        if(x == other.x) return y < other.y;
        return x < other.x;
    }
    void print() {
        cout << x << ' ' << y << ' ';
    }
};

ll n, m;
vector<Point> white, black;
vector<Point> convex_white, convex_black;
Point reference;

bool cmp(Point a, Point b) {
    ll res = (a - reference).cross(b - reference);
    if(res != 0) return res > 0;
    return reference.dist(a) < reference.dist(b);
}
void Graham_Scan(vector<Point> &points, vector<Point> &convex) {
    sort(all(points));
    reference = points[0];
    sort(points.begin()+1, points.end(), cmp);
    for(Point p3 : points) {
        while(convex.size() >= 2) {
            Point p2 = convex.back();
            Point p1 = convex[convex.size() - 2];
            ll ccw = (p2-p1).cross(p3-p2);
            if(ccw > 0) break;
            convex.pop_back();
        }
        convex.emplace_back(p3);
    }
}
void Rotating_Calipers() {
    int sz = convex.size();
    ll ans = 0; int l=0, r=0;
    for(int k=0; k<sz; k++) {
        if(convex[l].x > convex[k].x) l = k;
        if(convex[r].x < convex[k].x) r = k;
    }

    int L = l, R = r;
    ll maxDist = convex[l].dist(convex[r]);
    for(int _=0; _<sz; _++) {
        int nl = (l+1)%sz, nr = (r+1)%sz;
        ll ccw = (convex[nl] - convex[l]).cross(convex[nr] - convex[r]);
        if(ccw < 0) l = (l+1)%sz;
        else r = (r+1)%sz;
        ll minDist = convex[l].dist(convex[r]);
        if(maxDist < minDist) {
            maxDist = minDist;
            L = l, R = r;
        }
    }
    convex[L].print(); convex[R].print();
    cout << '\n';
}
bool isIntersect(Point p1, Point p2, Point p3, Point p4) {
    ll p1p2 = (p2-p1).crossSign(p3-p2) * (p2-p1).crossSign(p4-p2); // 선분 p1p2 기준
    ll p3p4 = (p4-p3).crossSign(p1-p4) * (p4-p3).crossSign(p2-p4); // 선분 p3p4 기준

    // 두 직선이 일직선 상에 존재
    if(p1p2 == 0 && p3p4 == 0) {
        if(p2 < p1) swap(p1,p2);
        if(p4 < p3) swap(p3,p4);
        return p3 < p2 && p1 < p4;
    }
    return p1p2 <= 0 && p3p4 <= 0;
}
// 모든 B가 A의 영역 안에 있는지를 반환
// 점을 오른쪽으로 선을 끝까지 그었을 때 만나는 선분의 개수가 홀수면 내부, 짝수면 외부에 있는 것이다.
bool isIncluded(vector<Point> &A, vector<Point> &B) {
    int sza = A.size(), szb = B.size();
    for(int b=0; b<szb; b++) {
        Point pointNB(B[b].x + INF, B[b].y);
        int cnt = 0;
        for (int a = 0; a < sza; a++) {
            int na = (a + 1) % sza;
            if((B[b].y < A[na].y) != (B[b].y < A[a].y)) cnt += isIntersect(A[a], A[na], B[b], pointNB);
        }
        if(cnt%2 == 0) return false;
    }
    return true;
}
string solve() {
    int szb = convex_black.size(), szw = convex_white.size();

    for(int b=0; b<szb; b++) {
        int nb = (b+1) % szb;
        for(int w=0; w<szw; w++) {
            int nw = (w+1) % szw;
            if(isIntersect(convex_black[b], convex_black[nb], convex_white[w], convex_white[nw])) return "NO";
        }
    }
    if(szb < 3 || szw < 3) return "YES";
    // 영역을 구축할 수 있으려면 각 점들이 3개 이상이어야 한다.

    // 검은색 점 영역 안에 모든 흰색 점이 들어가 있는지 확인
    if(isIncluded(convex_black, convex_white)) return "NO";
    // 흰색 점 영역 안에 모든 검은색 점이 들어가 있는지 확인
    if(isIncluded(convex_white, convex_black)) return "NO";

    return "YES";
}

int main(void) {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int T; cin >> T;
    while(T--) {
        black.resize(0); white.resize(0);
        convex_black.resize(0); convex_white.resize(0);

        cin >> n >> m;
        for(int i=0; i<n; i++) {
            ll x, y; cin >> x >> y;
            black.emplace_back(x,y);
        }
        for(int i=0; i<m; i++) {
            ll x, y; cin >> x >> y;
            white.emplace_back(x,y);
        }
        Graham_Scan(black, convex_black);
        Graham_Scan(white, convex_white);
        cout << solve() << '\n';
    }


    return 0;
}
```

# 선분 교차 판정

참고: [https://killerwhale0917.tistory.com/6](https://killerwhale0917.tistory.com/6)

```cpp
struct Point {
    ll x, y;

    Point() {}
    Point(ll _x, ll _y) : x(_x), y(_y) {}
    ll cross(Point other) {
        return x*other.y - y*other.x;
    }
    ll crossSign(Point other) {
        ll res = this->cross(other);
        if(res > 0) return 1;
        else if(res < 0) return -1;
        return 0;
    }
    ll dist(Point other) {
        return pow(x-other.x,2) + pow(y-other.y,2);
    }
    Point operator-(Point other) const {
        return Point(x-other.x, y-other.y);
    }
    bool operator==(Point other) const {
        return x == other.x && y == other.y;
    }
    bool operator<(Point other) const {
        if(x == other.x) return y < other.y;
        return x < other.x;
    }
    void print() {
        cout << x << ' ' << y << ' ';
    }
};
int isIntersect(Point p1, Point p2, Point p3, Point p4) {
    ll p1p2p3 = (p2-p1).crossSign(p3-p2), p1p2p4 = (p2-p1).crossSign(p4-p2);
    ll p3p4p1 = (p4-p3).crossSign(p1-p4), p3p4p2 = (p4-p3).crossSign(p2-p4);
    ll p1p2 = p1p2p3 * p1p2p4; // 선분 p1p2 기준
    ll p3p4 = p3p4p1 * p3p4p2; // 선분 p3p4 기준

    // 두 직선이 일직선 상에 존재
    if(p1p2p3 == 0 && p1p2p4 == 0) {
        if(p2 < p1) swap(p1,p2);
        if(p4 < p3) swap(p3,p4);
        if(p3p4p1 == 0 && p3p4p2 == 0) { // 평행할 때
            if(p2 < p3 || p4 < p1) return 0; // 평행 하지만 겹치지 않음
            if(p2 == p3 || p4 == p1) return 1; // 한 점만 겹침
            return INF; // 해가 무수히 많음
        }
        return 1;
    }
    return p1p2 <= 0 && p3p4 <= 0;
}
```

선분 p1p2, 선분 p3p4의 교차판정을 한다고 했을 때

1. p1p2 = ccw(p1,p2,p3) * ccw(p1,p2,p4)  
   p3p4 = ccw(p3,p4,p1) * ccw(p3,p4,p2)  
   을 계산한다.

2. p1p2 == 0 && p3p4 == 0 이면,  
   두 선분이 한 직선 상에 있다는 의미이므로 두 선분이 겹치는 지 확인한다.

3. p1p2 ≤ 0 && p3p4 ≤ 0 이면,  
   두 선분이 교차한다는 의미다.


# 선분의 교차점 구하기

설명: [https://velog.io/@jinsoolve/2023.11.12.-PS-log](https://velog.io/@jinsoolve/2023.11.12.-PS-log)

교차점을 구하는 방식은 findIntersectionPoint()함수와 같다. 증명은 velog에 있다.

교차점이라는 것은 한 점만 있어야 하므로 선분이 겹칠 때는 제외해준다.

```cpp
void findIntersectionPoint(Vector p1, Vector p2, Vector p3, Vector p4) {
    Vector p1p2 = p2-p1, p3p4 = p4-p3;
    double px = p2.cross(p1)*p3p4.x - p1p2.x*p4.cross(p3);
    double py = p2.cross(p1)*p3p4.y - p1p2.y*p4.cross(p3);
    double p = p1p2.cross(p3p4);

    if(fabs(p) < EPSILON) { // parallel
        if(p2 < p1) swap(p1,p2);
        if(p4 < p3) swap(p3,p4);
        if(p2 == p3) p2.print();
        else if(p4 == p1) p4.print();
    }
    else Vector(px/p, py/p).print(); // intersect
}
void solve(Vector p1, Vector p2, Vector p3, Vector p4) {
    double p1p2_ccw = ccw(p1,p2,p3) * ccw(p1,p2,p4);
    double p3p4_ccw = ccw(p3,p4,p1) * ccw(p3,p4,p2);

    // intersect at end point
    if(fabs(p1p2_ccw) < EPSILON && fabs(p3p4_ccw) < EPSILON) {
        if(p2 < p1) swap(p1, p2);
        if(p4 < p3) swap(p3,p4);

        if(p3 <= p2 && p1 <= p4) {
            cout << "1\n";
            findIntersectionPoint(p1,p2,p3,p4);
        }
        else cout << "0\n";
    }
    // just intersect normally
    else {
        if(p1p2_ccw < EPSILON && p3p4_ccw < EPSILON) {
            cout << "1\n";
            findIntersectionPoint(p1,p2,p3,p4);
        }
        else cout << "0\n";
    }
}

```

# 볼록 다각형 내부의 점 판정

참고: [https://bowbowbow.tistory.com/24](https://bowbowbow.tistory.com/24)

한 점을 기준으로 오른쪽으로 반직선을 그었을 때 만나는 볼록 다각형의 선분의 개수가 짝수면 외부, 홀수면 내부다.

```cpp
// 모든 B가 A의 영역 안에 있는지를 반환
// 점을 오른쪽으로 선을 끝까지 그었을 때 만나는 선분의 개수가 홀수면 내부, 짝수면 외부에 있는 것이다.
bool isIncluded(vector<Point> &A, vector<Point> &B) {
    int sza = A.size(), szb = B.size();
    for(int b=0; b<szb; b++) {
        Point pointNB(B[b].x + INF, B[b].y);
        int cnt = 0;
        for (int a = 0; a < sza; a++) {
            int na = (a + 1) % sza;
            if((B[b].y < A[na].y) != (B[b].y < A[a].y)) cnt += isIntersect(A[a], A[na], B[b], pointNB);
        }
        if(cnt%2 == 0) return false;
    }
    return true;
}
```