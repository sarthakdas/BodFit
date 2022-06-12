from random import randint
import pandas as pd
import operator
from datetime import date

class muscleHealth:
    def __init__(self):
        self.muscle_data = pd.read_csv(r'Dataset/muscle_health.csv')
        self.muscle_data.set_index("Muscle Name",inplace = True)
    
    def muscle_to_work_out(self):
        tranning_category = muscleHealth.muscle_category()
        return tranning_category
    
    def muscle_category(self):
        muscle_categories = set(self.muscle_data["Category"])

        muscle_category_health = {}
        for category in muscle_categories:
            selected_rows = self.muscle_data["Category"] == category
            df = self.muscle_data[selected_rows]
            average_health = df["Health"].mean()
            muscle_category_health[category] = average_health

        return max(muscle_category_health.items(), key=operator.itemgetter(1))[0]

    def muscle_regen(self):
        for index,row in self.muscle_data.iterrows():
            if row["Date Last Updated"] != date.today():
                self.muscle_useage_update(row["Muscle Name"],5)
            
    def muscle_useage_update(self,muscle,amount,today=date.today()):
        muscle_health_value = self.muscle_data.loc[muscle]["Health"]
        if (muscle_health_value == 100 and amount > 0) or (muscle_health_value == 0 and (amount < 0)):
            pass
        else:
            self.muscle_data.at[muscle,"Health"] = self.muscle_data.loc[muscle]["Health"] + amount
            self.muscle_data.at[muscle,'Date Last Updated'] = today
        self.muscle_data.to_csv("./Dataset/muscle_health.csv")

    def muscles_to_work_out(self):
        valid_muscles = []
        for index,row in self.muscle_data.iterrows():
            if int(row["Health"]) < 50 :
                pass
            else:
                valid_muscles.append(str(index))

        return valid_muscles

    def abs_valid(self,muscle):
        muscle_condition = self.muscle_data["Muscle Name"] == "Abdominals"
        index = self.muscle_data.index[muscle_condition]
        muscle_health_value = int(self.muscle_data.iloc[index]["Health"])
        if muscle_health_value > 70:
            return True
        else:
            return False
        

d = muscleHealth()
print(d.muscles_to_work_out())