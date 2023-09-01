import fastapi.testclient
from celery import Celery
import worker
from main import app


class TestClient:
    def __init__(self, app, inline=False):
        self.app = app
        self.app.conf.broker_url = "memory://"
        self.inline = inline
        if self.inline:
            # self.always_eager = True
            self._monkey_patch()

    @property
    def tasks(self):
        tasks = {}
        with self.app.connection() as connection:
            channel = connection.channel()
            for key, queue in channel.queues.items():
                if key not in tasks:
                    tasks[key] = []
                while not queue.empty():
                    tasks[key].append(queue.get())
        return tasks

    def _monkey_patch(self):
        self.app.send_task = self._send_task.__get__(self.app, Celery)

    def _send_task(
        self,
        name,
        args=None,
        kwargs=None,
        countdown=None,
        eta=None,
        task_id=None,
        producer=None,
        connection=None,
        router=None,
        result_cls=None,
        expires=None,
        publisher=None,
        link=None,
        link_error=None,
        add_to_parent=True,
        group_id=None,
        group_index=None,
        retries=0,
        chord=None,
        reply_to=None,
        time_limit=None,
        soft_time_limit=None,
        root_id=None,
        parent_id=None,
        route_name=None,
        shadow=None,
        chain=None,
        task_type=None,
        **options
    ):
        x = self.tasks[name].apply(args, kwargs, **options)
        print(x.get())
        print("monkey patch")
        return x


# app = Celery("test", broker="redis://localhost:6379/0")
# app = Celery("test", broker="memory://")

client = fastapi.testclient.TestClient(app)
celery_client = TestClient(worker.app, inline=True)

# @fixture
# def client(user):
#     yield TestClient(app, cookies={"authToken": user.api_token})

# transport = app.broker_connection().connect()
# connection = transport.client.connection
# # print(transport.client.connection)
# consumer = transport.client.Consumer()
# # print(dir(consumer))

# print(app.tasks())


def test_1():
    # r = app.send_task("test")
    # print(client.tasks)
    response = client.post("/users", json={"name": "Harry"})
    print(celery_client.tasks)
    assert response.status_code == 201
