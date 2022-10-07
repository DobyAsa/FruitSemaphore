# 实验二  进程同步程序设计
# 一、实验目的
# 1、	加深对进程概念的理解，明确进程和程序的区别。
# 2、	认识进程并发执行的实质
# 3、	掌握信号通信机制，实现进程之间通过信号实现互斥与同步的方法。
#
# 二、实验内容
# 桌子上有一只水果篮，最多可容纳两个水果，每次只能放入或者取出一个水果。爸爸专门向水果篮中放香蕉，妈妈专门向水果篮中放草莓，儿子专门等待吃水果篮中
# 的香蕉，女儿专门等吃水果篮中的草莓。每个小孩最多连吃2个水果后，等另一个小孩吃至少一个水果才会再次开始吃水果，为此，水果篮中若连续放4个相同水果，
# 则必须由放置该水果的人将水果拿回1个。试编程实现爸爸、妈妈、儿子、女儿四个人之间的同步。
# （1）水果、水果篮均通过导入图片来实现可视化；
# （2）放水果、拿水果均有动画显示，包括把水果拿到手上去放、放完空手回来等均通过的动画予以展示；
# （3）执行顺序由并发控制机制决定，而非通过延时实现；
# （4）要求界面美观、动作流畅。
#
# 三、实验要求
# 1、	写出程序，并调试程序，要给出测试数据和实验结果。
# 2、	整理上机步骤，总结经验和体会。
# 3、	完成实验报告和上交程序。
import threading
import time

verbose = True
wait = False

bucket = {
    "香蕉": 0,
    "草莓": 0
}
count = {
    "父亲": 0,
    "母亲": 0,
    "儿子": 0,
    "女儿": 0
}
bucket_lock = threading.Lock()
count_lock = threading.Lock()

# 控制篮子中的水果不能超过两个
bucket_sema = threading.BoundedSemaphore(2)

# 控制小男孩可以吃香蕉
boy_get_sema = threading.Semaphore(0)

# 控制小女孩可以吃草莓
girl_get_sema = threading.Semaphore(0)


def father():
    while True:
        bucket_sema.acquire()

        bucket_lock.acquire()
        count_lock.acquire()

        if count["父亲"] < 3:
            if wait:
                time.sleep(1)

            bucket["香蕉"] += 1
            count["父亲"] += 1
            count["母亲"] = 0
            if verbose:
                print("父亲放了一个香蕉")
                print(bucket)
                print(count)
                print()
            boy_get_sema.release()

        count_lock.release()
        bucket_lock.release()


def mother():
    while True:
        bucket_sema.acquire()

        bucket_lock.acquire()
        count_lock.acquire()

        if count["母亲"] < 3:
            if wait:
                time.sleep(1)

            bucket["草莓"] += 1
            count["母亲"] += 1
            count["父亲"] = 0
            if verbose:
                print("母亲放了一个草莓")
                print(bucket)
                print(count)
                print()
            girl_get_sema.release()
        count_lock.release()
        bucket_lock.release()


def boy():
    while True:
        boy_get_sema.acquire()

        bucket_lock.acquire()
        count_lock.acquire()
        if count["儿子"] <= 1:
            if wait:
                time.sleep(1)

            bucket["香蕉"] -= 1
            count["儿子"] += 1
            count["女儿"] = 0
            if verbose:
                print("儿子拿了一个香蕉")
                print(bucket)
                print(count)
                print()
            bucket_sema.release()

        count_lock.release()
        bucket_lock.release()


def girl():
    while True:
        girl_get_sema.acquire()

        bucket_lock.acquire()
        count_lock.acquire()

        if count["女儿"] <= 1:
            if wait:
                time.sleep(1)

            bucket["草莓"] -= 1
            count["女儿"] += 1
            count["儿子"] = 0
            if verbose:
                print("女儿拿了一个草莓")
                print(bucket)
                print(count)
                print()
            bucket_sema.release()

        count_lock.release()
        bucket_lock.release()


f = threading.Thread(target=father, args=())
m = threading.Thread(target=mother, args=())
b = threading.Thread(target=boy, args=())
g = threading.Thread(target=girl, args=())

f.start()
m.start()
g.start()
b.start()
