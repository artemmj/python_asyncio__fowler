import asyncio
from datetime import datetime, timedelta


class CircuitOpenException(Exception):
    pass


class CircuitBreaker:
    def __init__(self, callback,
        timeout: float,
        time_window: float,
        max_failures: int,
        reset_interval: float
    ):
        self.callback = callback
        self.timeout = timeout
        self.time_window = time_window
        self.max_failures = max_failures
        self.reset_interval = reset_interval
        self.last_request_time = None
        self.last_failure_time = None
        self.current_failures = 0

    async def request(self, *args, **kwargs):
        """Отправить запрос или сразу вернуть ошибку, если превышен счетчик ошибок."""
        if self.current_failures >= self.max_failures:
            if datetime.now() > self.last_request_time + timedelta(seconds=self.reset_interval):
                self._reset('Цепь переходит из разомкнутого состояния в замкнутое, сброс!')
                return await self._do_request(*args, **kwargs)
            else:
                print('Цепь разомкнута, быстрый отказ!')
                raise CircuitOpenException()
        else:
            lft = self.last_failure_time
            if lft and datetime.now() > lft + timedelta(seconds=self.time_window):
                self._reset('Интервал с момента первого сбоя, сброс!')
        print('Цепь замкнута, отправляю запрос!')
        return await self._do_request(*args, **kwargs)

    def _reset(self, msg: str):
        """Сбросить счетчик и время последнего отказа."""
        print(msg)
        self.last_failure_time = None
        self.current_failures = 0

    async def _do_request(self, *args, **kwargs):
        """
        Отправить запрос и следить за тем, сколько было ошибок и когда имела место последняя ошибка.
        """
        try:
            print('Отправляется запрос!')
            self.last_request_time = datetime.now()
            return await asyncio.wait_for(self.callback(*args, **kwargs),
            timeout=self.timeout)
        except Exception as e:
            self.current_failures = self.current_failures + 1
            if self.last_failure_time is None:
                self.last_failure_time = datetime.now()
            raise


async def main():

    async def slow_callback():
        await asyncio.sleep(2)

    cb = CircuitBreaker(slow_callback, 1.0, 5, 2, 5)

    for _ in range(4):
        try:
            await cb.request()
        except Exception as exc:
            pass

    print('Засыпаю на 5 с, чтобы прерыватель замкнулся...')
    await asyncio.sleep(5)

    for _ in range(4):
        try:
            await cb.request()
        except Exception as exc:
            pass


if __name__ == '__main__':
    asyncio.run(main())
