#!/usr/bin/env python
from flask import Flask, render_template, request, json, jsonify, make_response, url_for, abort, Blueprint, send_file, redirect, send_from_directory
from sqlalchemy import select, join, outerjoin, func, or_, and_
from app import db, app, mail
from forms import SignupForm
from itertools import chain
from collections import namedtuple
from app import settings
from json import dumps as json_dumps

import requests
import os
import tempfile
import random
from pyusps import address_information

from urllib import quote_plus
from datetime import datetime, timedelta, date

from StringIO import StringIO

from models import Product, ABVariant, SignUp

from dateutil import parser as dateparser

import flask_admin as admin

mod = Blueprint('apis', __name__)


@app.route('/api/product', methods=['DELETE', 'GET', 'POST', 'PUT'])
@app.route('/api/product/<int:product_id>', methods=['DELETE', 'GET', 'PUT'])
def products(product_id=None):
    if product_id:
        if request.method == 'DELETE':
            product.delete().where(Product.id == product_id).execute()

        elif request.method == 'GET':
            product = Product.get(id=product_id)
            return jsonify(get_attr(product))

        elif request.method == 'PUT':
            product = Product.get(id=product_id)
            product.update(**parse_attr(request)).execute()

    else:
        if request.method == 'GET': 
            product_objects = Product.query.all()
            products = []
            for product in product_objects:
                return jsonify(product.__dict__)
            return jsonify(products)

        elif request.method == 'POST':
            new_product = Product(**parse_attr(request))
            new_product.save()
            return jsonify(get_attr(new_product))

    return '', 200

@app.route('/api/variant', methods=['DELETE', 'GET', 'POST', 'PUT'])
@app.route('/api/variant/<int:variant_id>', methods=['DELETE', 'GET', 'PUT'])
def variants(variant_id=None):
    if variant_id:
        if request.method == 'DELETE':
            variant.delete().where(ABVariant.id == variant_id).execute()

        elif request.method == 'GET':
            variant = ABVariant.get(id=variant_id)
            return jsonify(get_attr(variant))

        elif request.method == 'PUT':
            variant = ABVariant.get(id=variant_id)
            variant.update(**parse_attr(request)).execute()

    else:
        if request.method == 'GET':
            return jsonify([get_attr(entry) for entry in ABVariant.select()])

        elif request.method == 'POST':
            new_variant = ABVariant(**parse_attr(request))
            new_variant.save()
            return jsonify(get_attr(new_variant))

    return '', 200
    
@mod.route('/api/signup', methods=['GET', 'POST'])
def api_signup():
    return json("");

