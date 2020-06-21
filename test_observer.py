class Subject:
    def __init__(self):
        self.__observers = []

    def register_observer(self, observer):
        if observer not in self.__observers:
            self.__observers.append(observer)

    def remove_observer(self, observer):
        if observer in self.__observers:
            self.__observers.remove(observer)

    def notify_observers(self):
        for observer in self.__observers:
            observer.update(self)


class SimpleSubject(Subject):
    def __init__(self):
        Subject.__init__(self)
        self.__value = 0

    def set_value(self, value):
        self.__value = value
        self.notify_observers()

    def get_value(self):
        return self.__value


class SecondSubject(Subject):
    def __init__(self):
        Subject.__init__(self)
        self.__second = 5

    def set_second(self, second):
        self.__second = second
        self.notify_observers()

    def get_second(self):
        return self.__second


class SimpleObserver:
    def __init__(self, subject, second):
        self.__subject = subject
        self.__subject.register_observer(self)
        self.__second = second
        self.__second.register_observer(self)
        print("initial", self.__subject.get_value())
        print("initial", self.__second.get_second())

    def update(self, subject):
        if isinstance(subject, SimpleSubject):
            self.__subject = subject
            print("updated", self.__subject.get_value())
            print("not updated", self.__second.get_second())
        elif isinstance(subject, SecondSubject):
            self.__second = subject
            print("not updated", self.__subject.get_value())
            print("updated", self.__second.get_second())

def main():
    simple_subject = SimpleSubject()
    second_subject = SecondSubject()
    simple_observer = SimpleObserver(simple_subject, second_subject)
    simple_subject.set_value(100)
    second_subject.set_second(200)

if __name__ == '__main__':
    main()