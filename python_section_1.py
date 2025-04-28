def ListToDict(arr):
    hmap = {}
    for i in arr:
        x = len(i)
        if x in hmap:
            hmap[x].append(i)
        else:
            hmap[x] = [i]
    sorted_hmap = dict(sorted(hmap.items()))
    return sorted_hmap

def reverse_in_groups(lst, n):
    result = []
    length = len(lst)
    for i in range(0, length, n):
       
        group = []
        
        for j in range(min(n, length - i)):
            group.append(lst[i + j])
        
        
        for k in range(len(group) - 1, -1, -1):
            result.append(group[k])
    
    return result

def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, item in enumerate(v):
                items.extend(flatten_dict(item, f"{new_key}[{i}]", sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def permute_unique(nums):
    def backtrack(start):
        if start == len(nums):
            result.append(nums[:])
            return
        seen = set()
        for i in range(start, len(nums)):
            if nums[i] not in seen:
                seen.add(nums[i])
                nums[start], nums[i] = nums[i], nums[start]
                backtrack(start + 1)
                nums[start], nums[i] = nums[i], nums[start]

    nums.sort()
    result = []
    backtrack(0)
    return result
import re

def find_all_dates(text):
    date_patterns = r'\b(\d{2})-(\d{2})-(\d{4})\b|\b(\d{2})/(\d{2})/(\d{4})\b|\b(\d{4})\.(\d{2})\.(\d{2})\b'
    matches = re.findall(date_patterns, text)
    
    valid_dates = []
    for match in matches:
        if match[0]:  
            valid_dates.append(f"{match[0]}-{match[1]}-{match[2]}")
        elif match[3]:  
            valid_dates.append(f"{match[3]}/{match[4]}/{match[5]}")
        elif match[6]:  
            valid_dates.append(f"{match[6]}.{match[7]}.{match[8]}")

    return valid_dates
import polyline
import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def process_polyline(polyline_str):
    try:
        coordinates = polyline.decode(polyline_str)
        
        if not coordinates:
            raise ValueError("Decoded coordinates list is empty.")
        
        df = pd.DataFrame(coordinates, columns=['latitude', 'longitude'])
        
        distances = [0]
        for i in range(1, len(df)):
            lat1, lon1 = df.loc[i-1, 'latitude'], df.loc[i-1, 'longitude']
            lat2, lon2 = df.loc[i, 'latitude'], df.loc[i, 'longitude']
            dist = haversine(lat1, lon1, lat2, lon2)
            distances.append(dist)
        
        df['distance'] = distances
        return df
    
    except Exception as e:
        print(f"Error decoding polyline: {e}")
        return pd.DataFrame(columns=['latitude', 'longitude', 'distance'])

polyline_str = "_p~iF~ps|U_ulLnnqC_mqNvxq`@"
df = process_polyline(polyline_str)
print(df)

def transform_matrix(matrix):
    n = len(matrix)
    
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for i in range(n):
        matrix[i].reverse()

    transformed_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            row_sum = sum(matrix[i]) - matrix[i][j]
            col_sum = sum(matrix[x][j] for x in range(n)) - matrix[i][j]
            transformed_matrix[i][j] = row_sum + col_sum

    return transformed_matrix

import pandas as pd
import numpy as np

def check_time_completeness(df):
    day_name_to_num = {
        'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 
        'Friday': 4, 'Saturday': 5, 'Sunday': 6
    }
    
    df['startDay'] = df['startDay'].map(day_name_to_num)
    df['endDay'] = df['endDay'].map(day_name_to_num)

    df['startTime'] = pd.to_datetime(df['startTime'], format='%H:%M:%S').dt.time
    df['endTime'] = pd.to_datetime(df['endTime'], format='%H:%M:%S').dt.time
    
    expected_days = set(range(7))
    full_day_time_range = pd.date_range("00:00:00", "23:59:59", freq="1s").time

    grouped = df.groupby(['id', 'id_2'])
    
    def is_incomplete(group):
        days_covered = set(group['startDay']).union(set(group['endDay']))
        if days_covered != expected_days:
            return True
        
        for day in expected_days:
            times_for_day = group[(group['startDay'] == day) | (group['endDay'] == day)]
            if times_for_day.empty:
                return True
            time_covered = set()
            for _, row in times_for_day.iterrows():
                start_time = pd.Timestamp.combine(pd.Timestamp.today(), row['startTime'])
                end_time = pd.Timestamp.combine(pd.Timestamp.today(), row['endTime'])
                time_covered.update(pd.date_range(start_time, end_time, freq='1s').time)
            if set(full_day_time_range) != time_covered:
                return True
        
        return False

    result = grouped.apply(is_incomplete)
    return result

df = pd.read_csv('dataset-1.csv')
result = check_time_completeness(df)
print(result)


