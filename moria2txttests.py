#!/usr/bin/env python
# Unit tests for moria2txt.py.

from moria2txt import *

def random_number_5_equals_4():
	randNum = randomNumber(5)
	if randNum != 4:
		print("FAILED: randomNumber unit test with input 5 failed to return correct value. Expected: 4, got: ", randNum)
	else:
		print("PASSED: Test randomNumber with input 5 should = 4, got: ", randNum)

def random_between_1_and_4500_equals_4241():
	randBNum = randomBetweenAB(1, 4500)
	if randBNum != 4241:
		print("FAILED: random_between_1_and_4500 unit test failed to return correct value. Expected: 4241, got: ", randBNum)
	else:
		print("PASSED: Test random_between_1_and_4500 with input 1 and 4500 should = 4241, got: ", randBNum)

def rnd_equals_1173064461():
	rndNum = int(rnd())
	if rndNum != 1173064461:
		print("FAILED: rnd unit test failed to return correct value. Expected: 1173064461, got: ", rndNum)
	else:
		print("PASSED: rnd should = 1173064461, got: ", rndNum)

def random_normal_distrubtion_equals_1414():
	rndNNum = randomNumberNormalDistribution(1424, 9)
	if rndNNum != 1414:
		print("FAILED: random_normal_distrubtion unit test with input 1424, 9 failed to return correct value. Expected: 1414, got: ", rndNNum)
	else:
		print("PASSED: random_normal_distrubtion with input 1424, 9 should = 1414, got: ", rndNNum)

def random_choice_equals_test4():
	rndChoice = RandomChoice(['test0', 'test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8'])
	if rndChoice != 'test4':
		print("FAILED: random_choice_equals unit test failed to return correct value. Expected: test4, got: ", rndChoice)
	else:
		print("PASSED: random_choice_equals should = test4, got: ", rndChoice)

def main():
	# Start by setting a seed of 500 to drive all tests.
	seedsInitialize(500)
	# seedsInitialize(24141) # Use to break the tests.
	# Bad practice but for now keep the test suite as individual functions and call individually.
	random_number_5_equals_4()
	rnd_equals_1173064461()
	random_between_1_and_4500_equals_4241()
	random_normal_distrubtion_equals_1414()
	random_choice_equals_test4()

main()