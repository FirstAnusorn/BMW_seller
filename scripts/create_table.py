from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base
import pandas as pd

def create_table(db_file):
    engine = create_engine(f'sqlite:///{db_file}')
    Base = declarative_base()
    
    # Define the table structures
    class Table_car_cleaned(Base):
        __tablename__ = 'cars_cleaned'
        
        Car_ID = Column(Integer, primary_key=True)
        Model = Column(String)
        Year = Column(String)
        Region = Column(String)
        Color = Column(String)
        Fuel_Type = Column(String)
        Transmission = Column(String)
        Engine_Size_L = Column(Float)
        Mileage_KM = Column(Float)
        Price_USD = Column(Float)
        Sales_volume = Column(Float)
        Sales_Classification = Column(String)
        Mileage_Mile = Column(Float)
        Price_THB = Column(Float)
        Car_Age = Column(Integer)
        Revenue = Column(Float)
    
    class Table_car_summary(Base):
        __tablename__ = 'sales_summary'
        
        Summary_ID = Column(Integer, primary_key=True)
        Car_ID = Column(Integer, ForeignKey('cars_cleaned.Car_ID'))
        Region = Column(String)
        Fuel_Type = Column(String)
        Year = Column(String)
        Total_Sales_Volume = Column(Float)
        Total_Revenue_USD = Column(Float)
        Average_Price_USD = Column(Float)
    
    # Create tables in the database
    Base.metadata.create_all(engine)