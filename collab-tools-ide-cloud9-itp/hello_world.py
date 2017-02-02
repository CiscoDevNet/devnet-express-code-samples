from werkzeug.wrappers import Request, Response

@Request.application
def application(request):
    strAge = request.args['age']
    intAge = int(strAge)
    if (intAge > 30):
        return Response("Kids these days!")
    else:
        return Response("Never trust anyone over 30!")

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('0.0.0.0', 8080, application)
