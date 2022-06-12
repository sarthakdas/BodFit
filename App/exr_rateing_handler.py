import pandas as pd
from exr_gen_handler import *
from muscle_energy_handler import *

class exrRating:
    def __init__(self):
        pass

    def ask_for_ratings(self,a,b,workout_plan):
        self.option_description()
        for index,row in workout_plan.iterrows():
            # print(index)
            rating = self.rateing(workout_plan.iloc[index]["Name"])
            b.set_and_rep_updater(rating,self.number_till_faliure(rating),workout_plan.iloc[index]["Name"])
            b.muscle_health_updater(a,rating,workout_plan.iloc[index])

    def rateing(self,workout_name):
        rating = input("rate:"+ str(workout_name))
        return int(rating)

    
    def option_description(self):
        print("""Rate the exersice \n
                1 - Failed 5 reps before limit \n
                2 - Failed 2 reps before limit\n
                3 - Perfect amount\n
                4 - Could do 2 reps above limit\n
                5 - Could do 5 reps above limit\n
            """)        

    def number_till_faliure(self,rating):
        if rating == 1:
            return -5
        elif rating == 2:
            return -2 
        elif rating == 3:
            return 0 
        elif rating == 4:
            return 2
        elif rating == 5:
            return 5

a = muscleHealth()
b = exrGen()
c = exrRating()


workout_plan = b.exr_gen(a)
print("===============================")
print(workout_plan)
print("===============================")

c.ask_for_ratings(a,b,workout_plan)


