import json
import psycopg2
from flask import Flask, request
from flask_restful import Api
from sqlalchemy import Column, String, Integer, Date, BOOLEAN, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from flask import jsonify
import os

# Line 13 -14 to initilise the app & api
app = Flask(__name__)
api = Api(app)

Base = declarative_base()
database_url = "postgresql://postgres:1990@localhost:5432/postgres"

# disable sqlalchemy pool using NullPool as by default Postgres has its own pool
engine = create_engine(database_url, echo=True, poolclass=NullPool)

conn = engine.connect()

Session = sessionmaker(bind=engine)
session = Session()

class ProductEnquiry(Base):
    __tablename__ = "productenquiry"
    customerName= Column("customer_name", String)
    mobileNumber = Column("mobile_number", Integer, primary_key=True)
    emailId = Column("email_id", String)
    vehicleModel=Column("vehicle_model",String)
    state=Column("state",String)
    district=Column("district",String)
    city=Column("city",String)
    existingVehicle=Column("existing_vehicle",String)
    wantTestDrive = Column("want_to_take_a_test_ride", BOOLEAN)
    dealerState=Column("dealer_state",String)
    dealerTown=Column("dealer_town",String)
    dealer=Column("dealer",String)
    briefAboutEnquery = Column("brief_about_enquiry", String)
    expectedDateOfPurchase=Column("expected_date_of_purchase", String)
    gender=Column("gender",String)
    age = Column("age", Integer)
    occupation=Column("occupation",String)
    intendedUsage=Column("intended_usage", String)


@app.route('/en-in/reach-us/product-enquiry', methods=['GET'])
def home():
    result = session.query(ProductEnquiry).all()
    print(type(result))
    result = [item.__dict__ for item in result]
    return str(result)

@app.route('/getSingleCustomerDetails', methods=['GET'])
def getSingleCustomerDetails():
    mobilenumber = request.args.get('mobilenumber')
    result = session.query(ProductEnquiry).filter(ProductEnquiry.mobileNumber==mobilenumber).all()
    print(type(result))
    result = [item.__dict__ for item in result]
    return str(result)

@app.route('/postrecords', methods=['POST'])
def home1():
    request_body = request.get_json(force=True)
    print("request_body->", request_body)
    print("enumerate(request_body)-->",enumerate(request_body))
    for index, item in enumerate(request_body):
        record = ProductEnquiry(customerName = item["customer_name"],
                                     mobileNumber = item["mobile_number"],
                                     emailId = item["email_id"],
                                     vehicleModel = item["vehicle_model"],
                                     state = item["state"],
                                     district = item["district"],
                                     city = item["city"],
                                     existingVehicle = item["existing_vehicle"],
				     wantTestDrive = item["want_to_take_a_test_ride"],
                                     dealerState = item["dealer_state"],
                                     dealerTown = item["dealer_town"],
                                     dealer = item["dealer"],
				     briefAboutEnquery = item["brief_about_enquiry"],
                                     expectedDateOfPurchase = item["expected_date_of_purchase"],
                                     gender = item["gender"],
				     age = item["age"],
                                     occupation = item["occupation"],
                                     intendedUsage = item["intended_usage"])

        session.add_all([record])
    session.commit()
    return ("data inserted")

@app.route('/deleteTheRecord', methods=['DELETE'])
def deleteTheRecord():
    mobilenumber = request.args.get('mobilenumber')
    result = session.query(ProductEnquiry).filter(ProductEnquiry.mobileNumber
                                                  ==mobilenumber).delete()
    session.commit() # Save  the changes
    return "{} record has been deleted successfully".format(mobilenumber)

app.run(debug=False)
