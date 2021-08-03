# Bicycle Manufacturing Schedule
from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpStatus, value, makeDict
from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/json-post', methods=['POST'])
def json_example():

    request_data = request.get_json()

    bike_types = None
    bike_profit = None
    parts_stock = None
    part_names = None
    bike_parts = None

    if request_data:
        if 'bike_types' in request_data:
            if (type(request_data['bike_types']) == list) and (len(request_data['bike_types']) > 0):
                bike_types = request_data['bike_types']
                print(bike_types)
                #bike_types = ["A", "B", "C", "D"]

        if 'bike_profit' in request_data:
            if (type(request_data['bike_profit']) == list) and (len(request_data['bike_profit']) > 0):
                bike_profit = request_data['bike_profit']
                print(bike_profit)
                #bike_profit = [45, 60, 55, 50]

        if 'parts_stock' in request_data:
            if (type(request_data['parts_stock']) == list) and (len(request_data['parts_stock']) > 0):
                parts_stock = request_data['parts_stock']
                print(parts_stock)
                #parts_stock = [180, 40, 60, 50, 40]

        if 'part_names' in request_data:
            if (type(request_data['part_names']) == list) and (len(request_data['part_names']) > 0):
                part_names = request_data['part_names']
                print(part_names)

                """
                part_names = [
                    "wheels",
                    "alloy_chassis",
                    "steel_chassis",
                    "hub_gears",
                    "derailleur_gears",
                ]
                """
        if 'bike_parts' in request_data:
            if (type(request_data['bike_parts']) == list) and (len(request_data['bike_parts']) > 0):
                bike_parts = request_data['bike_parts']
                print(bike_parts)

                """
                bike_parts = [  # part_names
                    # "wheels", "alloy_chassis", "steel_chassis", "hub_gears", "derailleur_gears"
                    [2, 1, 0, 1, 0],  # Bike type A
                    [2, 0, 1, 0, 1],  # Bike type B
                    [2, 1, 0, 0, 1],  # Bike type C
                    [2, 0, 1, 1, 0],  # Bike type D
                ]
                """
                # transpose the above array (you need to do this to write your constraint correctly)
                bike_parts = list(map(list, zip(*bike_parts)))

                # convert data into dicts
                dict_bike_profit = dict(zip(bike_types, bike_profit))
                dict_bike_stock = dict(zip(part_names, parts_stock))
                dict_bike_parts = makeDict([part_names, bike_types], bike_parts)

                prob = LpProblem("Profit Maximising", LpMaximize)

                # We can't sell half a bike, so the category for each bicycle type is an integer.
                x = LpVariable.dicts("x", bike_types, lowBound=0, cat="Integer")

                # Our objective is to maximise the profit
                prob += lpSum([dict_bike_profit[i] * x[i] for i in dict_bike_profit]), "Total Profit"

                # Constraints on available bike parts
                for i in dict_bike_parts:
                    prob += (
                        lpSum(dict_bike_parts[i][p] * x[p] for p in dict_bike_parts[i])
                        <= dict_bike_stock[i],
                        "availability_%s" % (i),
                    )

                # Print the problem
                print(prob)

                # Solve the problem
                prob.solve()
                print("Status : ", LpStatus[prob.status])

                # Print our changing cells
                for i in x:
                    print("Units of ", x[i], "= ", x[i].varValue)

                # Print our objective function value - Result (Target) cell
                print("Total Profit             = ", value(prob.objective))

                return '''
                    The total profit is: {}
                    '''.format(value(prob.objective))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
