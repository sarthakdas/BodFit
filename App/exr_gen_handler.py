import pandas as pd
from muscle_energy_handler import *
from random import randint

class exrGen:
    def __init__(self):
        self.exr_data = pd.read_csv(r'Dataset/simple_exr.csv')
        self.exr_data.drop([])
        self.exr_data.set_index("Name",inplace = True)
        # self.exr_data = self.secondary_muscle_handler(self.exr_data)

    def exr_gen(self,a):
        # TODO why doesnt this work with a.muscles_to_work_out()
        muscle_catagory = a.muscle_category()
        selected_rows = self.exr_data["Category"] == muscle_catagory
        filtered_df = self.exr_data[selected_rows]
        valid_muscles = a.muscles_to_work_out()
        boolean_series = filtered_df["main_muscle"].isin(valid_muscles)
        valid_exersices = filtered_df[boolean_series]
        valid_muscles_in_category = self.valid_muscles_in_category(valid_exersices)

        valid_exersices_copy = valid_exersices.copy().reset_index()
        valid_exersices = self.secondary_muscle_handler(valid_exersices_copy)


        workout_plan = []

        for muscle in valid_muscles_in_category:
            selected_rows = valid_exersices["main_muscle"] == muscle
            muscle_filtered_df = valid_exersices[selected_rows]
            number = randint(0, len(muscle_filtered_df.index)-1)
            chosen_exr = muscle_filtered_df.iloc[number]
            workout_plan.append(list(chosen_exr))

        list_of_used_secondary_muscles = self.set_of_secondary_muscles(workout_plan,valid_exersices.columns.values)

        for index,row in valid_exersices.iterrows():
            count = 0
            muscles_in_curr_ex = valid_exersices.iloc[index]["secondary_muscle"] 
            for muscle in muscles_in_curr_ex:
                if muscle in list_of_used_secondary_muscles:
                    pass
                else: 
                    count += 1
            
            if count >= 2:
                workout_plan.append(list(valid_exersices.iloc[index]))
                for secondary_muscle in valid_exersices.iloc[index]["secondary_muscle"]:
                    list_of_used_secondary_muscles.add(secondary_muscle)

        # print("Hello:",workout_plan)
        workout_plan = pd.DataFrame(workout_plan, columns= valid_exersices.columns.values)
        # print(workout_plan)
        return workout_plan

    def set_of_secondary_muscles(self,workout_plan,headers):

        workout_plan = pd.DataFrame(workout_plan, columns = headers)

        list_of_used_secondary_muscles = []
        for index,row in workout_plan.iterrows():
            secondary_muscles = workout_plan.iloc[index]["secondary_muscle"]
            if secondary_muscles != ['0']:
                for muscle in secondary_muscles:
                    list_of_used_secondary_muscles.append(muscle)
        
        list_of_used_secondary_muscles = set(list_of_used_secondary_muscles)

        return list_of_used_secondary_muscles

    def secondary_muscle_handler(self,df):
        for index,row in df.iterrows():
            print(index)
            print(df.loc[index]["secondary_muscle"].split())
            print(df.at[index,"secondary_muscle"].split())
            df.at[index,"secondary_muscle"] = df.at[index, "secondary_muscle"].split()
        return df

    def valid_muscles_in_category(self,df):
        muscle_categories = set(df["main_muscle"])
        return muscle_categories

    def set_and_rep_updater(self,rating,n_till_fail,workout):
        exr = self.exr_data.loc[workout]
        if rating == 1 or rating == 2:
            if int(exr["reps"]) > (6 + n_till_fail):
                self.exr_data.at[workout,'reps'] = int(exr['reps']) + n_till_fail
            elif int(exr["reps"]) < (6 + n_till_fail):
                self.exr_data.at[workout,'reps'] = 8
                self.exr_data.at[workout,'weight'] = int(exr['weight']) - 2.5 
        elif rating == 4 or rating == 5:
            if (int(exr["reps"]) + n_till_fail) > 12:
                self.exr_data.at[workout,'reps'] = 8
                self.exr_data.at[workout,'weight'] = int(exr['weight']) + 2.5 
            elif (int(exr["reps"]) + n_till_fail) < 12:
                self.exr_data.at[workout,'reps'] = int(exr['reps']) + n_till_fail
                

        self.exr_data.to_csv("./Dataset/simple_exr.csv")

    def muscle_health_updater(self,a,rating,workout):
        m_muscle = workout["main_muscle"]
        s_muscles = workout["secondary_muscle"]
        print(s_muscles)
        print(m_muscle)
        if rating == 1: 
            m_amount = -30
            s_amount = -20
        elif rating == 2:
            m_amount = -20
            s_amount = -17
        elif rating == 3:
            m_amount = -17.5
            s_amount = -15
        elif rating == 4:
            m_amount = -15
            s_amount = -13
        elif rating == 5:
            m_amount = -10
            s_amount = -10
        a.muscle_useage_update(m_muscle, m_amount)
        for muscles in s_muscles:
            if muscles == '0':
                pass
            else: 
                print(muscles)
                a.muscle_useage_update(muscles, s_amount)

a = muscleHealth()
d = exrGen()
print(d.exr_gen(a))
# print(d.exr_data.loc['Dips - Triceps Version\n'])