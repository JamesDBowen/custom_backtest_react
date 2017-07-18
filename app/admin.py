#!/usr/bin/env python
from flask import Flask, render_template, request, json, jsonify, make_response, url_for, abort, Blueprint, send_file, redirect, send_from_directory
from sqlalchemy import select, join, outerjoin, func, or_, and_
from app import db, app
from app import settings
from json import dumps as json_dumps

from app import models

from dateutil import parser as dateparser

import flask_admin as admin
from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters

mod = Blueprint('admin_tools', __name__)

# Create admin
admin = admin.Admin(app, name='Smoke Marketing', template_mode='bootstrap3')

# Add views
admin.add_view(sqla.ModelView(models.Profile, db.session))
admin.add_view(sqla.ModelView(models.Series, db.session))

#admin.add_view(sqla.ModelView(models.User))
#admin.add_view(sqla.ModelView(models.Product))
#admin.add_view(sqla.ModelView(models.Customer))
