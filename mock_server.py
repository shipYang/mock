from flask import Flask,request,make_response,jsonify
import string


app = Flask(__name__)


def read_mock():
    with open('/Users/YangYang/Desktop/mock_data.csv', 'r',encoding='utf-8') as f:
        return (generate_mock_data(line) for line in f.readlines())
#从文件中读取数据，并且返回，把返回的值用表达式传给generate_mock_data


def generate_mock_data(line):
    mock_data=line.strip('\n').strip("").split(',')
    return [mock_data[0],mock_data[1],mock_data[2],mock_data[3],mock_data[4],mock_data[5],mock_data[6]]
#把从文件获取的数据进行去除换行和空格后拆分成列表，并且把每一列返回

mock_data=read_mock()


def checkpath(path,request_param,request_header,method):
    method=method.lower()
    l = []
    for i in request_param:
        sub_request_param = [i]
        l.append(sub_request_param)
    if len(l) == 0:
        for j in mock_data:
            if path in j and method in j and request_header in j:
                return generate_response(j[5], j[4],j[6])
    else:
        format_reqparam = formate_params(l)  # 获取实际的请求参数,并进行格式化

        for j in mock_data:
            if path in j and (method in j) and (format_reqparam in j) and request_header in j:

                return generate_response(j[5],j[4],j[6])

#处理mock数据中预期的返回值
def generate_response(resp_body,cookie,http_status):
    resp=make_response(resp_body)
    resp.set_cookie('cookie',cookie)
    if http_status=='200':
       return resp
    else:
        return make_response(jsonify({'msg':'error'}),http_status)

#格式化处理实际请求的参数格式
def formate_params(value):

    result=''
    for i in range(len(value)):
        for j in range(len(value[i])):

            result = result + value[i][j][0] + '='
            result = result + value[i][j][1] + '&'

    return result[0:-1]



@app.route('/<path:path>/<path:path1>',methods=['POST','GET'])
def get_All_task(path,path1):
    npath='/'+path+'/'+path1

    request_param=request.values.items()
    request_header=request.headers.get('cookie')

    return checkpath(npath,request_param,request_header,request.method)


@app.route('/<path:path>',methods=['POST','GET'])
def get_task(path):
    npath = '/' + path

    request_param = request.values.items()
    request_header = request.headers.get('cookie')
    return checkpath(npath, request_param, request_header,request.method)


if __name__ == '__main__':
    app.run(debug=True,port=5000,threaded=True)
