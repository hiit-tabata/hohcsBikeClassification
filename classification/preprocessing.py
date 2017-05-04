import json
import numpy as np
from numpy import genfromtxt
from constant import LABEL_PATH, JSON_PATH
from io import BytesIO

def readLabelCsv():
    '''
        read the csv file export from the google sheet
    '''
    return np.genfromtxt(LABEL_PATH, 
                         delimiter=',', 
                         dtype=[('user','S60'),('recordid','|S60'),('clientid','|S60'),('date','S60'),('adult_','f8'),('walking_ability__high_performer_','f8'),('walking_ability__walk_unaided','f8'),('walking_ability__walk_with_stick','f8'),('walking_ability__walk_with_quadripod','f8'),('walking_ability__walk_with_frame','f8'),('walking_ability__chairbound_(can_not_walk)','f8'),('mobilize_from_chair__independent','f8'),('mobilize_from_chair__mild_assistance_','f8'),('mobilize_from_chair__heavy_assistance_/_cannot','f8'),('hip__stable_','f8'),('hip__stable_but_high_risk_feature_','f8'),('hip__functional_deficit_but_well_adapted','f8'),('hip__unstable_','f8'),('hip_2_pelvic_shift_','f8'),('hip_2_leave_sit_','f8'),('hip_2_pendulum_movement','f8'),('hip_disconnection__left_','f8'),('hip_disconnection__right_','f8'),('hip_disconnection__connected','f8'),('trunk_stable_','f8'),('trunk_stable_but_high_risk_feature','f8'),('trunk_functional_deficit_but_well_adapted','f8'),('trunk_unstable','f8'),('trunk_lean_stably_','f8'),('trunk_lean_evenly','f8'),('trunk_lean_left_predorminantly_','f8'),('trunk_lean_right_predominantly','f8'),('trunk_fall_like_pattern','f8'),('trunk_pendulum','f8'),('trunk_leave_the_lean','f8'),('trunk_disconnection__left_','f8'),('trunk_disconnection__right_','f8'),('trunk_disconnection__connected_','f8'),('bike__strong_','f8'),('bike__moderate_','f8'),('bike__weak__(cannot_walk)','f8'),('inattention__yes','f8'),('rest_yes','f8'),('fall__past_history_','f8'),('fall__recent_fall_','f8'),('fall__no_signficant_fall_history','f8'),('hospitalization__past_history','f8'),('hospitalization__recent_event_','f8'),('hospitalization__no_significant_history','f8'),('stroke__yes','f8'),('leg_surgery__yes_','f8'),('leg_coordinated','f8'),('leg_coordinated_most_of_the_time','f8'),('leg_not_coordinated','f8'),('dementia__yes','f8'),('fatigue_yes','f8'),('test_complete_yes','f8')],
                         skip_header=2, 
                         filling_values=0)

def readRecord(recordId):
    '''
        Read the json that save by nodejs
        return a dictionary and a numpy array of the data
    '''
    with open(JSON_PATH+str(recordId)+'.json') as data_file:    
        recordJson = json.load(data_file)
        csvDataStr = recordJson["data"]
        recordJson["data"] = ""
        arr = []
        csvData = json.loads(csvDataStr) 
        for row in csvData:
            arr.append([ row["timestamp"],
                        row["sensor1"],
                        row["sensor2"],
                        row["sensor3"],
                        row["sensor4"],
                        row["sensor5"],
                        row["sensor6"] ])
        return recordJson, np.array(arr)