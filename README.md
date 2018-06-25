# Simply-2048
80行代码简单实现2048小游戏
根据游戏规则可以把2048小游戏简单拆分为： 
初始化游戏，更新矩阵，随机生成数字，游戏显示，游戏开始这五个模块。下面我来分别解析这些模块。

### 1）初始化游戏
通过对2048游戏进行抽象创建Game类，对后续游戏的初始化分别放在构造函数以及init_matrix方法中执行。
```python
START = 1
OVER = 2
WIN = 3
def __init__(self):
    self.matrix = []
    self.changes = False
    self.state = Game.START
    self.score = 0
    self.oder = {'w': "self.matrix[j][i]", 's': "self.matrix[3 - j][i]",
                 'd': "self.matrix[i][3 - j]", 'a': "self.matrix[i][j]"}
def init_matrix(self):
    for i in range(4):
        self.matrix.append([])
        for j in range(4):
            self.matrix[i].append(Check())
```
对于构造函数__init__()

matrix变量作为矩阵用于存放数值。Changes变量当矩阵内数值发生变化时将被赋予True。State变量用于表示当前状态。初始化状态为START，而这个Game类中还有类变量OVER与WIN，分别代表游戏输赢。Score变量用于存储游戏过程中玩家获得的分数。Oder变量为字典类型，用来存储对应操作的命令。

对于方法init_matrix(self):

该方法主要对matrix进行赋值操作，生成一个4*4的矩阵。可以看到该方法中赋值的是为Check()的类，这个类对init类型进行封装。
```python
class Check:
    def __init__(self):
        self.value = 0
```
由于在一般编程语言中存在着，引用变量以及值变量这样的概念，该程序也是充分运用到了这个概念，对矩阵的后续更新操作也需要用到此概念，所以对int类型进行封装使其能够满足引用变量的概念。
### 2）更新矩阵
更新矩阵操作在do()与overlay()方法中执行。两方法的执行逻辑是:
通过命令行，接收用户输入值，通过Oder变量根据输入值选择相应的命令调用do()方法传入命令，之后将矩阵分割为单行或单列交由overlay执行
```python
def do(self, code):
    self.changes = False
    for i in range(4):
        row = []
        for j in range(4):
            row.append(eval(code))
        self.overlay(row)
def overlay(self, row):
    for index in range(4):
        next_index = index + 1
        while next_index < 4:
            if row[next_index].value is 0:
                next_index += 1
            elif row[index].value is 0:
                row[index].value = row[next_index].value
                row[next_index].value = 0
                self.changes = True
            elif row[index].value is row[next_index].value:
                self.score += row[index].value
                row[index].value *= 2
                row[next_index].value = 0
                self.changes = True
            else:
                next_index += 1
```
对于如何更新矩阵，根据2048中的规则：“每滑动一次，所有的数字方块都会往滑动的方向靠拢外”，即可知每次操作后每个方块只会对单行或单列的其他方块产生影响，即每次更新操作，只需把单行或单列从矩阵中拆分开交由一个方法来进行判断，对方块执行重叠或移动操作就可以了。
通过上面的解释，就可以说明do()方法中的code变量就是指定其对矩阵的拆分逻辑。overlay()方法对这个通过拆分而获得的数组进行判断。
Overlay()的判断逻辑：row为拆分后的单行或单列数组。指定row中下标为index的值，再取其后一个下标为next_index的值，对于下标为index_next值为0时，index_next自增1，对于下标为index值为0且下标为index_next值不为0时，row[index_next]值赋值给row[index]，row[index_next]赋值为0,即让有数值的方格移动到空方格。若row[index]与row[index_next]则让row[index]乘2，row{index_next]赋值为0,其他情况让index_next自增1.
除此外当该数组发生变化时changes变量将被赋值为True，以及当方块发生重合时score变量也将记录下该值，视为玩家分数。
### 3）从空方格中随机生成数值
```python
随机生成数值的操作由random()方法来执行
def random(self):
    zero = []
    for i in range(4):
        for j in range(4):
            if self.matrix[i][j].value is 0:
                zero.append(self.matrix[i][j])
    if len(zero):
        slot = random.randint(0, len(zero) - 1)
        zero[slot].value = 2
    else:
        self.state = Game.OVER
```
该方法的执行逻辑为：通过遍历4x4矩阵找出数值为0的项，存储进zero数组
之后通过判断该数组长度来执行相应操作，如果数组长度不为0,则随机该数组中的一个随机项给其赋值为2（此处运用到值引用）,对于在zero上的赋值操作也将运用在matrix上。若数组长度为0,说明矩阵已被占满。将state变量赋值为OVER说明游戏结束。
### 4）游戏显示
对游戏的显示由show()方法完成
```python
def show(self):
    print('-----------------')
    for row in self.matrix:
        line = []
        for item in row:
            if item.value is 0:
                line.append('')
            else:
                line.append(str(item.value))
        print('| {}\t| {}\t| {}\t| {}\t|\n-----------------'.format(line[0], line[1], line[2], line[3]))
```

### 5）游戏开始
游戏通过start方法开始运行。
```python
def start(self):
    self.init_matrix()
    self.random()
    while self.state is Game.START:
        print("操作: (W)上 (S)下 (A)左 (D)右")
        print('***** 2048 *****')
        self.show()
        print('***** Game *****')
        print('分数: ', self.score)
        key = input('输入: ')
        self.do(self.oder[key.lower()])
        if self.changes:
            self.random()
```
其中init_matrix()初始化矩阵，random()开始时随机生成数值。
进入while循环判断state是否为Game.START若为否则跳出循环。
通过show()方法显示游戏矩阵，用input()接收用户输入,
之后通过用户输入选择命令交由do()方法，矩阵在这其中执行更新操作。
后判断changes若为真则再次随机生成数值。
