from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates', static_folder='static_files')


@app.route('/')
def hello():
    return render_template('index.html')

# @app.route('/home/selection/', methods=['POST', 'GET'])
# def selection():
#     # return request.args

#     picked_dates = db.load_json('db.json')
#     alerts = []

#     if len(picked_dates[request.args['dateSelection']]['picked_by']) < 30:
#         for key, value in picked_dates.items():
#             if request.args['user_id'] in value['picked_by']:
#                 print('removed from', key)
#                 print(request.args['user_id'], 'from', value['picked_by'])
#                 value['picked_by'].remove(request.args['user_id'])

#         picked_dates[request.args['dateSelection']]['picked_by'].append(request.args['user_id'].upper())
#         picked_date = request.args['dateSelection'].upper()
#         db.save_json(picked_dates, 'db.json')
#     else: alerts.append('your selected date is fully booked')

#     # print(request.args['dateSelection'])
#     for key, value in picked_dates.items():
#         value['picked_by'] = [find_name(i) for i in value['picked_by']]
#     # print(picked_dates)

#     return render_template(
#         'home.html', 
#         user_id=request.args['user_id'], 
#         user_name=request.args['user_name_'], 
#         pick_db=picked_dates, 
#         alerts = alerts,
#         picked_date=picked_date,
#         user_pass=request.args['floatingPassword'])
