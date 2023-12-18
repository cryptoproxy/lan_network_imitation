class Data:
    def __init__(self, data, ip):
        self.data = data
        self.ip = ip


class Server:
    count = 0

    def __new__(cls, *args, **kwargs):
        cls.count += 1
        return super().__new__(cls)

    def __init__(self):
        self.buffer = []
        self.ip = self.count
        self.router = None

    def send_data(self, data: Data):
        if self.router:
            self.router.buffer.append(data)
        else:
            print('Вы не подключены к интернету')

    def get_data(self):
        buffer = self.buffer[:]
        self.buffer = []
        return buffer

    def get_ip(self):
        return self.ip


class Router:
    def __init__(self):
        self.buffer = []
        self.servers = {}

    def link(self, *server: Server):
        for i in server:
            self.servers[i.get_ip()] = i
            i.router = self

    def unlink(self, server: Server):
        del self.servers[server.get_ip()]
        server.router = None

    def send_data(self):
        for data in self.buffer:
            if self.servers.get(data.ip):
                self.servers[data.ip].buffer.append(data.data)
            else:
                print(f'Нет такого сервера {data.ip}')
        self.buffer = []


def main():
    sv1 = Server()
    sv2 = Server()
    sv3 = Server()
    sv4 = Server()

    router = Router()
    router.link(sv1, sv2, sv3, sv4)

    data1 = Data('Строка с данными', 1)
    data2 = Data('Опа', 2)
    data3 = Data('Привет тут вирус', 3)
    data4 = Data('HentAI', 6)

    sv1.send_data(data1)
    sv2.send_data(data2)
    sv2.send_data(data3)
    sv2.send_data(data4)
    router.send_data()


if __name__ == '__main__':
    main()
