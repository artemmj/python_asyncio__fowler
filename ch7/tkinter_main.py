import asyncio
from asyncio import AbstractEventLoop
from aiohttp import ClientSession
from concurrent.futures import Future
from queue import Queue
from typing import Callable, Optional
from threading import Thread
from tkinter import Tk, Label, Entry, ttk


class StressTest:
    def __init__(
        self,
        loop: AbstractEventLoop,
        url: str,
        total_requests: int,
        callback: Callable[[int, int], int],
    ):
        self._completed_reqs: int = 0
        self._load_test_future: Optional[Future] = None
        self._loop = loop
        self._url = url
        self._total_reqs = total_requests
        self._callback = callback
        self._refresh_rate = total_requests // 100

    def start(self):
        """
        Начать отправку запросов и сохранить будущий объект,
        чтобы впоследствии можно было отменить тест.
        """
        future = asyncio.run_coroutine_threadsafe(self._make_requests(), self._loop)
        self._load_test_future = future

    def cancel(self):
        """Чтобы отменить тест, нужно вызвать метод cancel объекта _load_test_future."""
        if self._load_test_future:
            self._loop.call_soon_threadsafe(self._load_test_future.cancel())

    async def _get_url(self, session: ClientSession, url: str):
        try:
            await session.get(url)
        except Exception as exc:
            print(f'Ошибка: {exc}')
        self._completed_reqs += 1
        # После того как отправка 1% запросов завершена, вызвать функцию обратного вызова,
        # передав ей число завершенных запросов и общее число запросов
        if self._completed_reqs % self._refresh_rate == 0 or self._completed_reqs == self._total_reqs:
            self._callback(self._completed_reqs, self._total_reqs)

    async def _make_requests(self):
        async with ClientSession() as sess:
            reqs = [self._get_url(sess, self._url) for _ in range(self._total_reqs)]
            await asyncio.gather(*reqs)


class LoadTester(Tk):
    # В конструкторе инициализируем поля ввода, метки,
    # кнопку отправки и индикатор хода выполнения
    def __init__(self, loop, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self._queue = Queue()
        self._refresh_ms = 25

        self._loop = loop
        self._load_test: Optional[StressTest] = None
        self.title('URL Requester')

        self._url_label = Label(self, text="URL:")
        self._url_label.grid(column=0, row=0)
        self._url_field = Entry(self, width=40)
        self._url_field.grid(column=1, row=0)

        self._request_label = Label(self, text="Number of requests:")
        self._request_label.grid(column=0, row=1)
        self._request_field = Entry(self, width=40)
        self._request_field.grid(column=1, row=1)

        # При нажатии на кнопку Submit вызывается метод _start
        self._submit = ttk.Button(self, text="Submit", command=self._start)
        self._submit.grid(column=2, row=1)

        self._pb_label = Label(self, text="Progress:")
        self._pb_label.grid(column=0, row=3)
        self._pb = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        self._pb.grid(column=1, row=3, columnspan=2)

    def _update_bar(self, pct: int):
        """
        Метод _update_bar устанавливает процент заполненности индикатора хода
        выполнения от 0 до 100. Его следует вызывать только из главного потока.
        """
        if pct == 100:
            self._load_test = None
            self._submit['text'] = 'Submit'
        else:
            self._pb['value'] = pct
            self.after(self._refresh_ms, self._poll_queue)

    def _queue_update(self, completed_requests: int, total_requests: int):
        """
        Этот метод является обратным вызовом, который передается нагрузочному
        тесту; он добавляет обновление индикатора в очередь.
        """
        self._queue.put(int(completed_requests / total_requests * 100))

    def _poll_queue(self):
        """Извлечь обновление индикатора из очереди. Если получилось, обновить индикатор."""
        if not self._queue.empty():
            percent_complete = self._queue.get()
            self._update_bar(percent_complete)
        else:
            if self._load_test:
                self.after(self._refresh_ms, self._poll_queue)

    def _start(self):
        """Начать нагрузочное тестирование и каждые 25 мс опрашивать очередь обновлений."""
        if self._load_test is None:
            self._submit['text'] = 'Cancel'
            test = StressTest(
                self._loop,
                self._url_field.get(),
                int(self._request_field.get()),
                self._queue_update,
            )
            self.after(self._refresh_ms, self._poll_queue)
            test.start()
            self._load_test = test
        else:
            self._load_test.cancel()
            self._load_test = None
            self._submit['text'] = 'Submit'


class ThreadedEventLoop(Thread):
    """Создать новый класс потока, в котором будет крутиться цикл событий asyncio."""
    def __init__(self, loop: AbstractEventLoop):
        super().__init__()
        self._loop = loop
        self.daemon = True

    def run(self):
        self._loop.run_forever()


loop = asyncio.new_event_loop()

asyncio_thread = ThreadedEventLoop(loop)
# Запустить новый поток, исполняющий цикл событий asyncio в фоновом режиме
asyncio_thread.start()

# Создать приложение Tkinter и запустить его главный цикл событий
app = LoadTester(loop)
app.mainloop()
