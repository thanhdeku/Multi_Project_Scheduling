1. Du lieu:
n (Jobs)
k (Operation)
m (machine)
process_time(ma tran (nxk) x m)

VD:
1
2
3
1 2 5
4 3 1

2. Ma hoa:
Ma hoa bao gom 2 phan: left - right
[1,2,3,0,4,1,2,1,2,0]
 --------- ---------
    left     right
left: permutation voi do dai = n x k : Thu tu sap xep cua cac operation
right: day so tu nhien random trong khoang (0,m): Sap xep cac may cho cac operation tuong ung
==> gen = concat(left,right) la day co do dai: 2 x (nxk)

3. Khoi tao:
left: Khoi tao ngau nhien
right: Khoi tao voi xac suat ti le nghich voi thoi gian xu ly cua may
( May xu li cang nhanh thi xac suat duoc dung cang cao )

4. Crossover:
- Left: Pmx
- Right: TwoPoint Crossover
(Hai diem cat cua Left va Right giong nhau)

5. Mutation:
Cho 2 phan tu bat ki va swap
