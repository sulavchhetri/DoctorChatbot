from django.shortcuts import render
from django.http import JsonResponse
import numpy as np
import pandas as pd
import joblib
import os
from pathlib import Path

dataset_path = os.path.join(Path(__file__).parent.parent, "dataset")
sym_path = os.path.join(dataset_path, "symptom_severity.csv")
desc_path = os.path.join(dataset_path, "symptom_description.csv")
precaution_path = os.path.join(dataset_path, "symptom_precaution.csv")


sym = pd.read_csv(sym_path)
sym['Symptom'] = sym['Symptom'].str.replace('_', ' ')
desc = pd.read_csv(desc_path)
prev = pd.read_csv(precaution_path)


def home(request):
    return render(request, 'index.html')


def create(request):
    cls = joblib.load('model_joblib')

    lis = request.GET.getlist('queue[]')

    def predictions(s1, s2, s3, s4, s5='vomiting', s6='vomiting', s7='vomiting'):
        disease, description, precaution1, precaution2 = None, None, None, None
        l = [s1, s2, s3, s4, s5, s6, s7]
        x = np.array(sym['Symptom'])
        y = np.array(sym['weight'])
        for i in range(len(l)):
            for j in range(len(x)):
                if l[i] == x[j]:
                    l[i] = y[j]
        res = [l]
        pred = cls.predict(res)
        return pred[0]
    if len(lis) == 3:
        disease = predictions(lis[0], lis[1], lis[2])
        description = desc[desc['Disease'] == disease]['Description'].iloc[0]
        precaution1 = prev[prev['Disease'] == disease]['Precaution_1'].iloc[0]
        precaution2 = prev[prev['Disease'] == disease]['Precaution_2'].iloc[0]

    elif len(lis) == 4:

        disease = predictions(lis[0], lis[1], lis[2], lis[3])
        description = desc[desc['Disease'] == disease]['Description'].iloc[0]
        precaution1 = prev[prev['Disease'] == disease]['Precaution_1'].iloc[0]
        precaution2 = prev[prev['Disease'] == disease]['Precaution_2'].iloc[0]

    elif len(lis) == 5:

        disease = predictions(lis[0], lis[1], lis[2], lis[3], lis[4])
        description = desc[desc['Disease'] == disease]['Description'].iloc[0]
        precaution1 = prev[prev['Disease'] == disease]['Precaution_1'].iloc[0]
        precaution2 = prev[prev['Disease'] == disease]['Precaution_2'].iloc[0]
    elif len(lis) == 6:
        disease = predictions(lis[0], lis[1], lis[2], lis[3], lis[4], lis[5])
        description = desc[desc['Disease'] == disease]['Description'].iloc[0]
        precaution1 = prev[prev['Disease'] == disease]['Precaution_1'].iloc[0]
        precaution2 = prev[prev['Disease'] == disease]['Precaution_2'].iloc[0]
    elif len(lis) > 6:
        disease = predictions(lis[0], lis[1], lis[2],
                              lis[3], lis[4], lis[5], lis[6])
        description = desc[desc['Disease'] == disease]['Description'].iloc[0]
        precaution1 = prev[prev['Disease'] == disease]['Precaution_1'].iloc[0]
        precaution2 = prev[prev['Disease'] == disease]['Precaution_2'].iloc[0]

    print(disease,description)
    return JsonResponse({'disease': disease, 'precaution1': precaution1, 'precaution2': precaution2, 'description': description})
