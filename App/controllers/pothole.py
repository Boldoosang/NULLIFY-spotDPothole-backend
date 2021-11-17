from flask import Flask, request, session
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, current_user
from sqlalchemy.exc import IntegrityError, OperationalError
import json

from App.models import *


def getPotholeData():
    potholes = db.session.query(Pothole).all()
    potholeData = [p.toDict() for p in potholes]
    return json.dumps(potholeData), 200

def getIndividualPotholeData(id):
    pothole = db.session.query(Pothole).filter_by(potholeID=id).first()
    if not pothole:
        return {"error" : "No pothole data for that ID."}, 404

    potholeData = pothole.toDict()
    return json.dumps(potholeData), 200

def deletePothole(potholeID):
    pothole = db.session.query(Pothole).filter_by(potholeID=potholeID).first()
    if not pothole:
        return False
    else:
        try:
            db.session.delete(pothole)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False