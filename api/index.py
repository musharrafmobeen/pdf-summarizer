import string
from flask import Flask, request, jsonify, make_response
from PyPDF2 import PdfFileReader
from app import summarize

flask_app = Flask(__name__)


@flask_app.route("/summary", methods=["POST", "OPTIONS"])
def api_create_order():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    elif request.method == "POST":  # The actual request following the preflight
        print(request.files['file'])
        pdf = PdfFileReader(request.files['file'])
        txt = ''
        with open('Lecture Note.txt', 'w') as f:
            for page_num in range(pdf.numPages):
                # print('Page: {0}'.format(page_num))
                pageObj = pdf.getPage(page_num)
                # pdf.read()

                try:
                    txt = txt + pageObj.extractText()
                    # print(''.center(100, '-'))
                except:
                    pass
                # else:
                #     f.write('Page {0}\n'.format(page_num+1))
                #     f.write(''.center(100, '-'))
                #     f.write(txt)
        f.close()
        # s = ['a', 'b', 'c']
        # print(txt.replace('\n', ' '))
        # print(''.join(txt).replace('\n', " "))
        # print(''.join(s))
        text = ''.join(summarize(txt.replace('\n', ' ')))
        print(text)
        return _corsify_actual_response(jsonify({"summary": text}))
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == "__main__":
    flask_app.run(host='0.0.0.0', port=5000)
