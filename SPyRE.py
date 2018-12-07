from spyre import server

import pandas as pd
import json
import requests
import re
import os

class StockExample(server.App):
    title = "DataScience"

    inputs = [{        "type":'dropdown',
                    "label": 'Area',
                    "options" : [ {"label": "Vinnitska", "value":"1"},
                                  {"label": "Volinska", "value":"2"},
                                  {"label": "Dnipro", "value":"3"},
                                  {"label": "Donetska", "value":"4"},
                                  {"label": "Gitomirska", "value":"5"},
                                  {"label": "Ivano", "value":"8"},
                                  {"label": "Kyivska", "value":"9"}],
                    "key": 'provinceID',
                    "action_id": "update_data"},
          {        "type":'dropdown',
                    "label": 'Data type',
                    "options" : [ {"label": "VHI", "value":"VHI"},
                                 ],
                    "key": 'data',
                    "action_id": "update_data"}
                    ]

    controls = [{    "type" : "hidden",
                    "id" : "update_data"}]

    tabs = ["Plot", "Table"]

    outputs = [{ "type" : "plot",
                    "id" : "plot",
                    "control_id" : "update_data",
                    "tab" : "Plot"},
                { "type" : "table",
                    "id" : "table_id",
                    "control_id" : "update_data",
                    "tab" : "Table",
                    "on_page_load" : True }]
    def getData(self, params):
        provinceID = params['provinceID']
        datatype = params['data']
        api_url = 'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_provinceData.php?country=UKR&provinceID={}&year1=2018&year2=2018&type=Mean'.format(provinceID)
        vhiUrl = requests.get(api_url)
        normData = []
        data = str(vhiUrl.content).split('\n')[1:-1]

        for j in range(len(data)):
            data[j] = re.sub(',', ' ', data[j])
            data[j] = data[j].split(' ')
            data[j] = list(filter(lambda x: x != '', data[j]))
            data[j].insert(2, provinceID)
            data[j][0:3] = list(map(int, data[j][0:3]))
            data[j][3:] = list(map(float, data[j][3:]))
            normData.append(data[j])
        df = pd.DataFrame(normData, columns=['Year', 'Week', 'ProvinceID', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI'])
        return df


    def getPlot(self, params):
        datatype = params['data']
        df = self.getData(params)
        plt_obj = df.plot(x='Week', y=datatype)
        plt_obj.set_ylabel(datatype)
        fig = plt_obj.get_figure()
        return fig

app = StockExample()
app.launch( port=int(os.environ.get('PORT', '5000')))
