import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

global state

global numItemsScanned 

@ask.launch

def new_game():
	global state
	state = 0
	return question(render_template('welcome'))

@ask.intent("YesIntent")

def useYes():
	global state
	if state == 0:
		state = 1
		return question(render_template('user'))
	elif state == 1:
		state = 2
		return question(render_template('exist'))
	elif state == 2:
		state = 3
		return question(render_template('scan'))

@ask.intent("AnswerIntent", convert={'num': int})

def numItems(num):
	global state
	if state == 2:
		return statement(render_template('scan', num=num))
		numItemsScanned = num 
	return question(render_template('quit'))

@ask.intent("NoIntent")

def useNo():
	global state
	if state == 0:
		return question(render_template('nocout'))
	elif state == 1:
		return question(render_template('register'))
	return question(render_template('quit'))

# @ask.intent("StopIntent")

# def quitFunct():
# 	return

if __name__ == '__main__':

    app.run(debug=True)