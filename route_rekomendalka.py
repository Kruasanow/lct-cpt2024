def calculate_ranked_coefficients(data):
    ranked_data = {}
    for obj, values in data.items():
        print(values)
        actual, recommended, max_capacity = values
        diff_to_max = (max_capacity - actual) / max_capacity
        proximity_to_recommended = actual / recommended if actual <= recommended else recommended / actual
        final_coefficient = 0.6 * diff_to_max + 0.4 * (1 - proximity_to_recommended)
        ranked_data[obj] = {
            'coefficient': final_coefficient,
            'difference_to_max': max_capacity - actual
        }
    ranked_data = dict(sorted(ranked_data.items(), key=lambda item: item[1]['coefficient'], reverse=True))
    return ranked_data

# Входные данные
"""
'название объекта':     '[
                        кол-во людей, которые планируют посетить этот объект в этот день,
                        рекомендованное кол-во людей на этот день,
                        предельное кол-во людей в день
                        ]'
"""
# print(calculate_ranked_coefficients({'туробъект1': [80, 170, 150], 'туробъект2': [50, 70, 120], 'туробъект3': [70, 60, 90], 'туробъект4': [90, 90, 100], 'туробъект5': [101, 90, 100]}))
# Пример выхода
"""
{
    'объект2': {'coefficient': 0.6226190476190476, 'difference_to_max': 70},
    'объект3': {'coefficient': 0.6166666666666666, 'difference_to_max': 60},
    'объект1': {'coefficient': 0.5666666666666667, 'difference_to_max': 70},
    'объект4': {'coefficient': 0.37, 'difference_to_max': 10},
    'объект5': {'coefficient': 0.26032673267326734, 'difference_to_max': -1}
}
"""