#put path here
import unittest
import sys
import time
import awsdog
import boto3
from datadog import initialize, api


class TestAwsdogMethods(unittest.TestCase):
	
	def test_check_metric_metrcis_are_equal(self):
		self.assertTrue(awsdog.check_metric(['host0','host1'],['host0','host1'],'some env'))
		
	def test_check_metric_metrics_are_not_equal(self):
		self.assertFalse(awsdog.check_metric(['host0'],[],'some env'))

	def test_check_metric_input_type_error_1st_arg(self):
		with self.assertRaises(TypeError):
			awsdog.check_metric(1,['host'],'env')

	def test_check_metric_input_type_error_2nd_arg(self):
		with self.assertRaises(TypeError):
			awsdog.check_metric(['host'],1,'env')
	
	def test_check_metric_input_type_error(self):
		with self.assertRaises(NameError):
			awsdog.check_metric(['host'],['host'],env)
	
	def test_check_metric_none_1st_arg_value(self):
		x = None
		with self.assertRaises(TypeError):
			awsdog.check_metric(x,['host'],'env')
			
	def test_check_metric_none_2nd_arg_value(self):
		x = None
		with self.assertRaises(TypeError):
			awsdog.check_metric(['host'],x,'env')


			
			
if __name__ == '__main__':
	unittest.main()