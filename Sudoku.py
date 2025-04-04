import sys
sys.setrecursionlimit(10000000)

#初期状態の読み込み
f = open("problem.txt","r",encoding = "UTF-8")
lines = f.readlines()
plate = [[] for _ in range(9)]#図面を入れる
for i in range(9):
    line = lines[i]
    for j in range(9):
        plate[i].append(int(line[j]))
f.close()

#初期状態で空白のマスの要素番号を格納するリスト
lst = []
for i in range(9):
    for j in range(9):
        if plate[i][j] == 0:
            lst.append([i,j])

#一番近い3*3の中心点を見つける
def nearCenter(i,j):
    d = 100000
    a,b = 0,0
    for x in [1,4,7]:
        for y in [1,4,7]:
            if (x-i)**2 + (y-j)**2 < d:
                d = (x-i)**2 + (y-j)**2
                a,b = x,y
    return a,b

#選択肢の探索
def findChoice(i,j):
    s = set([1,2,3,4,5,6,7,8,9])
    
    #行を見る
    for k in range(9):
        if plate[i][k] in s:
            s.discard(plate[i][k])
            
    #列を見る
    for k in range(9):
        if plate[k][j] in s:
            s.discard(plate[k][j])
    
    #3*3を見る
    x,y = nearCenter(i,j)
    for k in [-1,0,1]:
        for l in [-1,0,1]:
            if plate[x+k][y+l] in s:
                s.discard(plate[x+k][y+l])
    
    return s

#大丈夫かどうかをチェックする
#だめならFalse,大丈夫ならTrueを返す
def check(i,j):
    
    #行を見る
    for k in range(9):
        if plate[i][j] == plate[i][k] and j!=k:
            return False
            
    #列を見る
    for k in range(9):
        if plate[i][j] == plate[k][j] and i!=k:
            return False
    
    #3*3を見る
    x,y = nearCenter(i,j)
    for k in [-1,0,1]:
        for l in [-1,0,1]:
            if plate[i][j] == plate[x+k][y+l] and [i,j] != [x+k,y+l]:
                return False
    
    return True


#plate[i][j]に置ける数字がなかったらFalse,置けるものがあればTrueを返す
def dfs(i,j,k):
    choice = findChoice(i,j) #plate[i][j]に入れる候補
    
    if [i,j] != lst[-1]:#lstの一番最後以外
        x,y = lst[k+1]
        for a in choice:
            plate[i][j] = a
            if check(i,j):
                if dfs(x,y,k+1):
                    return True
        plate[i][j] = 0
        return False 
    else:#lstの一番最後
        for a in choice:
            plate[i][j] = a
            if check(i,j):
                return True
        plate[i][j] = 0
        return False

#全探索して解く
dfs(lst[0][0],lst[0][1],0)

#答えを書き込む
f = open("answer.txt","w")
for i in range(9):
    result = ""
    for j in range(9):
        result = result + str(plate[i][j])
    result = result + "\n"
    if 0 in plate[i]:
        print("Couldn't solve this sudoku.")
    
    f.writelines(result)

f.close()