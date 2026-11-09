# -*- coding: utf-8 -*-
"""Практична робота №2: ітератори та генератори."""
import itertools,sys,timeit
STUDENTS = [('Олена', 95), ('Іван', 78), ('Марія', 92), ('Петро', 85), ('Анна', 88)]
RECORDS = [('Олена', 'Програмування', 95), ('Іван', 'Математика', 78), ('Марія', 'Програмування', 92), ('Петро', 'Математика', 85), ('Анна', 'Програмування', 88)]
from collections import namedtuple,defaultdict
class CyclicRange:
    def __init__(self,start,stop,step=1,repeats=1):
        if step==0 or repeats<0:raise ValueError('Некоректні параметри')
        self.values=range(start,stop,step);self._iterator=iter(self.values);self._cycle=0;self.repeats=repeats
    def __iter__(self):return self
    def __next__(self):
        while self._cycle<self.repeats:
            try:return next(self._iterator)
            except StopIteration:
                self._cycle+=1;self._iterator=iter(self.values)
        raise StopIteration
Student=namedtuple('Student','name grade')
class StudentGroupIterator:
    def __init__(self,students):self.students=students;self.index=0
    def __iter__(self):return self
    def __next__(self):
        if self.index>=len(self.students):raise StopIteration
        s=self.students[self.index];self.index+=1;return s
class StudentGroup:
    def __init__(self,name):self.name=name;self.students=[]
    def add_student(self,name,grade):self.students.append(Student(name,grade))
    def __iter__(self):return StudentGroupIterator(self.students)
    def __len__(self):return len(self.students)
    def top_students(self,n=3):return iter(sorted(self.students,key=lambda s:s.grade,reverse=True)[:n])
def arithmetic_progression(start,step):
    while True:
        yield start;start+=step
def geometric_progression(start,ratio,limit=float('inf')):
    if start<=0 or ratio<=1:raise ValueError('Потрібно start>0 і ratio>1')
    while start<=limit:
        yield start;start*=ratio
def fibonacci(n=None):
    a,b=0,1;k=0
    while n is None or k<n:
        yield a;a,b=b,a+b;k+=1
def collatz_sequence(n):
    if n<=0:raise ValueError('n>0')
    while True:
        yield n
        if n==1:break
        n=n//2 if n%2==0 else 3*n+1
def flatten(nested):
    for item in nested:
        if isinstance(item,list):yield from flatten(item)
        else:yield item
def data_source(records):
    for r in records:yield r
def filter_empty(records):
    for r in records:
        if r.strip():yield r
def parse_records(records):
    for line in records:
        parts=line.split(',')
        if len(parts)!=3:continue
        try:grade=int(parts[2]);assert 0<=grade<=100
        except (ValueError,AssertionError):continue
        yield {'student':parts[0],'subject':parts[1],'grade':grade}
def filter_passed(records,min_grade=60):
    for r in records:
        if r['grade']>=min_grade:yield r
def format_output(records):
    for r in records:yield f"[{r['subject']}] {r['student']}: {r['grade']} балів"
def main():
    print('1.1 CyclicRange:',list(CyclicRange(1,4,repeats=3)),sum(CyclicRange(1,5,repeats=2)))
    group=StudentGroup('КІ-21')
    for name,grade in STUDENTS:group.add_student(name,grade)
    print('1.2 Перша ітерація:',list(group),'друга:',list(group),'топ:',list(group.top_students()))
    it1,it2=iter(group),iter(group);print('Незалежні ітератори:',next(it1),next(it1),next(it2))
    print('2.1 Прогресії:',list(itertools.islice(arithmetic_progression(2,3),10)),list(geometric_progression(1,2,1000)))
    print('Фібоначчі:',list(fibonacci(15)),'Коллатц:',list(collatz_sequence(9)))
    print('flatten:',list(flatten([1,[2,[3,4]],5])))
    print('Перше Фібоначчі >10000:',next(x for x in fibonacci() if x>10000))
    rows=[f'{name},{subject},{grade}' for name,subject,grade in RECORDS]+['','Помилка,Математика,INVALID']
    pipeline=format_output(filter_passed(parse_records(filter_empty(data_source(rows))),75))
    print('2.2 Відфільтровано:',list(pipeline))
    stats=defaultdict(list)
    for r in parse_records(filter_empty(data_source(rows))):stats[r['subject']].append(r['grade'])
    print('Середні:',{k:round(sum(v)/len(v),1) for k,v in stats.items()})
    print('3.1 Пам’ять: N | list байт | generator байт')
    for n in [1000,10000,100000,1000000]:
        li=[x*x for x in range(n)];ge=(x*x for x in range(n))
        print(n,sys.getsizeof(li),sys.getsizeof(ge))
    n=100000
    print('Час list:',round(timeit.timeit(lambda:sum([x*x for x in range(n)]),number=5)/5,5))
    print('Час generator:',round(timeit.timeit(lambda:sum(x*x for x in range(n)),number=5)/5,5))
    words=['Python','ітератор','генератор','обчислення']
    print('max:',max((w for w in words),key=len),'all:',all(w for w in words),'any:',any(len(w)>15 for w in words))
    print('CSV:',','.join(w for w in words),'довжини:',sum(len(w) for w in words),'словник:',{w:len(w) for w in words})
    print('Квадрати парних:',sum(x*x for x in range(1,101) if x%2==0))
if __name__=='__main__':main()
