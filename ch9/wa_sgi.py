# gunicorn
def application(env, start_response):
    start_response('200 OK', [{'json', 'Content-Type'}])
    return [b'{WSGI HELLO!}']


# uvicorn
async def application(scope, receive, send):
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [[b'content-type', b'json']]
    })
    await send({'type': 'http.response.body', 'body': b'{ASGI HELLO!}'})
