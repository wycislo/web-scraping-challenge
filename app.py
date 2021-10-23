# flask app to render html on local machines.
# also will load data to mongo

from flask import Flask, render_template, redirect
import pymongo
import scrape_mars
