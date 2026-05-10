# 認識裝飾詞 (decorator)的用法


def say_hello():
    print("Hello")


def run_with_announce(func):  # func 就是傳進來的函式
    print("準備執行")
    func()  # 呼叫傳入的函式
    print("執行完畢")


print("直接呼叫:")
say_hello()

print()
print("透過run_with_announce呼叫:")
run_with_announce(say_hello)  # 把 say_hello 當參數傳進去(不要括號)


def gift_wrap(func):
    def wrapper():
        print("----前置動作----")
        func()  # 呼叫傳入的函式
        print("----後置動作----")

    return wrapper


say_hello = gift_wrap(say_hello)  # 把 say_hello 包裝起來

say_hello()

print("------------------")


@gift_wrap
def say_hello():
    print("Hello")


say_hello()

print("------------------")


def register_command(name, description):
    print(f"[登記]指令 /{name}: {description}")

    def decorator(func):  # 中層:接收函式
        def wrapper():  # 內層:包裝後的函式
            print(f"[執行]指令 /{name}")
            func()  # 執行原本的函式

        return wrapper

    return decorator  # 回傳中曾(真正得裝飾器)


@register_command(name="hello", description="打招呼")
def hello_command():
    print("你好!我是hello指令")


hello_command()  # 執行 hello_command 就會觸發裝飾器的功能
print("------------------")
