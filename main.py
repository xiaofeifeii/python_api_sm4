import threading
import time
import queue
import mqtt_msg
import handle_data


class Receive(threading.Thread):
    def __init__(self, t_name, queue1, clint):
        threading.Thread.__init__(self, name=t_name)
        self.data = queue1
        self.cli = clint

    def run(self):
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            self.data.put(msg.payload.decode())

        self.cli.subscribe(mqtt_msg.topic)
        self.cli.on_message = on_message
        self.cli.loop_forever()


class DataHandel(threading.Thread):
    def __init__(self, t_name, queue):
        threading.Thread.__init__(self, name=t_name)
        self.data = queue

    def run(self):
        while True:
            if not self.data.empty():
                msg = self.data.get()
                print('%s %s 出队 %s' % (time.ctime(), self.name, msg))
                self.data.task_done()
            time.sleep(2)


if __name__ == '__main__':
    queue = queue.Queue()
    m_clint = mqtt_msg.connect_mqtt()
    receive = Receive('Receive', queue, m_clint)
    data_Handel = DataHandel('DataHandel', queue)
    receive.start()
    data_Handel.start()
    queue.join()
