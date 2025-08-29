import asyncio
from datetime import datetime
from functools import partial

from aiohttp import ClientSession
from asgiref.sync import async_to_sync, sync_to_async
from django.http import HttpResponse
from django.shortcuts import render


async def requests_view(request):

    async def get_url_details(session: ClientSession, url: str):
        start_time = datetime.now()
        response = await session.get(url)
        response_body = await response.text()
        end_time = datetime.now()
        return {
            'status': response.status,
            'time': (end_time - start_time).total_seconds(),
            'body_length': len(response_body),
        }


    async def make_requests(url: str, request_num: int):
        async with ClientSession() as session:
            requests = [get_url_details(session, url) for _ in range(request_num)]
            results = await asyncio.gather(*requests, return_exceptions=True)
            failed_results = [str(result) for result in results if isinstance(result, Exception)]
            successful_results = [result for result in results if not isinstance(result, Exception)]
            return {
                'failed_results': failed_results,
                'successful_results': successful_results,
            }

    loop = asyncio.get_running_loop()
    print(id(loop))

    # url: str = request.GET['url']
    # request_num: int = int(request.GET['request_num'])
    # context = await make_requests(url, request_num)
    # return render(request, 'async_api/requests.html', context)

    url: str = request.GET['url']
    request_num: int = int(request.GET['request_num'])
    context = async_to_sync(partial(make_requests, url, request_num))()
    return render(request, 'async_api/requests.html', context)


async def sync_to_async_view(request):

    def sleep(seconds: int):
        import time
        time.sleep(seconds)

    sleep_time: int = int(request.GET['sleep_time'])
    num_calls: int = int(request.GET['num_calls'])
    thread_sensitive: str = request.GET['thread_sensitive']
    thread_sensitive = True if thread_sensitive.lower == 'true' else False

    function = sync_to_async(partial(sleep, sleep_time), thread_sensitive=thread_sensitive)
    await asyncio.gather(*[function() for _ in range(num_calls)])
    return HttpResponse('')
