import streamlit as st
import pickle
import pandas as pd

def estimate_price(data):
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)
             
    # as we only have one list of scalars, we must precise 
    # if it's a one-row or one-column DataFrame
    data_df = pd.DataFrame(data, index=[0]) 
    price = model.predict(data_df)
    
    st.session_state.price = float(price[0])
    return st.session_state.price

def display_price():
    mae = 57446
    min_price = str(round(st.session_state.price - mae))
    max_price = str(round(st.session_state.price + mae))
    price_to_display = min_price + " € - " + max_price + " €"
    return st.subheader(price_to_display)

def main():
    
    st.title("Real Estate Price Estimation")

    if "estimated_price" not in st.session_state:
        st.session_state.estimated_price = 0
    
    # Type of sale
    rent_or_buy = st.radio("Select one :", ["Buy","Rent"])
    
    if rent_or_buy == "Rent":
        TypeOfSale = {'Residential Monthly Rent' : 1}
        TypeOfSale_choice = 'Residential Monthly Rent'
        st.write("Our current estimations for renting are a bit off, sorry. Are you sure you don't want to buy ?")
    elif rent_or_buy == "Buy":
        TypeOfSale = {'Residential sale': 6, 'Homes to build': 5, 'Annuity (monthly amount)': 2, 'Annuity (with lump sum)': 4, 'Annuity (without lump sum)': 3}
        TypeOfSale_choice = st.selectbox('Type of sale : ', list(TypeOfSale.keys()))
    
    # BedroomCount
    BedroomCount = st.number_input("Number of bedrooms", min_value=0, max_value=39, value="min")
    
    
    # Property type
    property_types = {'House': 1, 'Apartment': 2}
    property_choice = st.radio("Select type of property : ", list(property_types.keys()))
    
    
    # Property subtype
    if property_choice == 'House' :
        property_subtypes = {"House" : 8, "Bungalow" : 9, "Country cottage" : 10, "Town House" : 11,
            "Chalet" : 12, "Villa" : 13,"Mixed-use building" : 16,"Apartment Block" : 17,"Farmhouse" : 18,
            "Pavilion" : 19, "Mansion" : 21, "Exceptional property" : 22, "Manor" : 23, "Castle" : 24, "Other" : 25}
        
        property_subtype_choice = st.selectbox("Select house subtype : ", list(property_subtypes.keys()))
        
    else :
        property_subtypes = {"Apartment" : 3,"Studio" : 1,"Kot" : 2,"Service Flat" : 4,"Ground floor" : 5,
                                "Loft" : 6,"Duplex" : 7,"Penthouse" : 14,"Triplex" : 15,"Show apartment" :20 }
        
        property_subtype_choice = st.selectbox("Select apartment subtype : ", list(property_subtypes.keys()))


    # Region
    regions = {'Wallonia' : 1, 'Flanders' : 2, 'Brussels' : 3}
    region_choice = st.selectbox("Select region", list(regions.keys()))

    
    # Province
    if region_choice == "Wallonia" :
        provinces = {'Hainaut' : 1,'Liège' : 2,'Luxembourg' : 3,'Namur' : 4,'Walloon Brabant' : 5}
        province_choice = st.selectbox("Select province : ", list(provinces.keys()))
    elif region_choice == "Flanders" :
        provinces = {'Limburg' : 6, 'East Flanders': 7, 'Flemish Brabant': 8, 'Antwerp': 9, 'West Flanders' : 10}
        province_choice = st.selectbox("Select province : ", list(provinces.keys()))
    elif region_choice == "Brussels" :
        provinces = {'Brussels' : 10}
        province_choice = st.selectbox("Select province : ", list(provinces.keys()))
    
    #State of building
    building_state = {'Leave blank' : 0, 'To restore' : 1, 'To renovate' : 2, 'To be done up' : 3,
                        'Good' : 4, 'As new' : 5, 'Just renovated' : 6}
    building_state_choice = st.selectbox("In what state is the property in?", list(building_state.keys()))
    
    # Kitchen
    kitchen = {'Leave blank': 0, 'Not installed': 1, 'Semi equipped': 3, 'Installed': 5, 'Hyper equipped': 7,
               '(American kitchen) Not installed': 2, '(American kitchen) Semi equipped' : 4, '(American kitchen) Installed' : 6, '(American kitchen) Hyper equipped': 8}
    kitchen_choice = st.selectbox("What is the type of kitchen ?", list(kitchen.keys()))
    
    # PEB
    PEB = {'Leave blank' : 0, 'A++': 9, 'A+': 8, 'A': 7, 'B': 6, 'C': 5, 'D': 4, 'E': 3, 'F': 2, 'G': 1}
    PEB_choice = st.selectbox('PEB', list(PEB.keys()))
    
    # Living Area
    LivingArea = st.number_input("Surface of living area", min_value=9, max_value=452230, value="min")
    
    # GardenArea
    GardenArea = st.number_input("Garden Area", min_value=0, max_value=100000, value="min")
    
    # Surface of plot
    if property_choice == 'House' :
        SurfaceOfPlot = st.number_input("Surface of the plot", min_value=0, max_value=366356)
    if property_choice == 'Apartment':
        SurfaceOfPlot = 0
        
    # Locality    
    with open('locality_dict.pkl', 'rb') as file:
        sorted_locality_dict = pickle.load(file)

    locality_choice = st.selectbox("Select locality (type first letters)", sorted(sorted_locality_dict.keys()))
    
    test_data = {
        "BedroomCount" : BedroomCount, 
        "TypeOfProperty" : property_types[property_choice], 
        "SubtypeOfProperty_num" : property_subtypes[property_subtype_choice], 
        "Region_num" : regions[region_choice], 
        "Province_num" : provinces[province_choice],
        "StateOfBuilding_num" : building_state[building_state_choice],
        "Kitchen_num" : kitchen[kitchen_choice],
        "PEB_num" : PEB[PEB_choice],
        "TypeOfSale_num" : TypeOfSale[TypeOfSale_choice],
        "LivingArea": LivingArea,
        "GardenArea" : GardenArea,
        "SurfaceOfPlot" : SurfaceOfPlot,
        "Locality_num" : sorted_locality_dict [locality_choice]
    }

    if st.button("Estimate price", type="primary",on_click=estimate_price,args=([test_data])) :
    #we put test_data into a list because args expects one value
        display_price()


if __name__ == '__main__':
    main()