
import json
import cv2



with open("image_annotations.json", "r") as f:
    annotations = json.load(f)


all_ls=[]


for i in range(300):

    try:
        if annotations[0][f"Person{i+1}.jpg"]["filename"] == f"Person{i+1}.jpg":
            img=cv2.imread(f"Person{i+1}.jpg")
            img_height=img.shape[0]
            img_width=img.shape[1]

            attributes_ls=[]

            for z in annotations[0][f"Person{i+1}.jpg"]["regions"]:
                attributes_ls.append(z["region_attributes"]["skin_analysis"])
                all_ls.append(z["region_attributes"]["skin_analysis"])
            sort_ls=sorted(attributes_ls)

           


           
            unique_ls_sort=['Acne', 'Blemish', 'Clogged_Pores', 'Dark_Circles', 'Freckle_Beauty_Spot', 'Hyperpigmentation_Dark_Marks', 'Redness', 'Uneven_Skintone', 'Wrinkles_Fine_Lines']
            count_list=[]




            for y in range(9):
                count_list.append(y)

            class_zip=zip(count_list,unique_ls_sort)
            class_ls=list(class_zip)
            

            



            with open(f"Person{i+1}.txt", "w") as f:
                for m,n in enumerate(sort_ls): 
                    my_zip=zip(annotations[0][f"Person{i+1}.jpg"]["regions"][m]["shape_attributes"]["all_points_x"],annotations[0][f"Person{i+1}.jpg"]["regions"][m]["shape_attributes"]["all_points_y"])
                    my_list=list(my_zip)


                    for x in class_ls:
                        if x[1]==annotations[0][f"Person{i+1}.jpg"]["regions"][m]["region_attributes"]["skin_analysis"]:
                            final_list=[x[0]]




                    for j in my_list:
                        a=j[0]/img_width
                        b=j[1]/img_height
                        final_list.append(a)
                        final_list.append(b)
                    
                    
                    for value in final_list:
                        f.write(f"{value} ")
                    f.write("\n")
            f.close()



    except FileNotFoundError:

        print(f"Image file for Person{i+1}.jpg not found. Skipping this iteration.")

    except Exception as e:

        print(f"An error occurred for Person{i+1}.jpg: {e}")







                    


                    

                        




