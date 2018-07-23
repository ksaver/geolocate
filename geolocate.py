#!/usr/bin/env python3

import argparse
import json
import requests
import socket
import sys


def get_country(ip_address):

	api_key = '30707f39960d942120ab1f9d0849ab2f'
	api_url = "http://api.ipstack.com/{}?access_key={}&format=2".\
		format(ip_address, api_key)
	
	location = ''
	try:
		socket.inet_aton(ip_address)
		r = requests.get(api_url)
		location = r.content.decode('utf-8')

	except Exception as e:
		print("Error: {}: {}".format(ip_address, e))
		return None

	return(location)


def main(args):

	ip_address_list = []
	sep = args.separator

	if args.ip:
		ip_address_list.extend(args.ip)

	elif args.filename:
		f = args.filename.read()
		ip_address_list.extend(f.split())

	for ip in ip_address_list:
		location_j = get_country(ip)

		if location_j:
			location = json.loads(location_j)
			country_name = location['country_name']
			country_code = location['country_code']
			country_flag = location['location']['country_flag']

			print("{1}{0}{2}{0}{3}{0}{4}".format(sep, ip, country_name, \
				country_code, country_flag))


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Geolocate IP addresses.')
	
	parser.add_argument('-a', '--address', dest='ip', nargs='+',
		help='IP Address.')

	parser.add_argument('-r', '--read-file', dest='filename',
		default=sys.stdin, type=argparse.FileType('r', encoding=('utf-8')),
		help='IP addresses file list.')

	parser.add_argument('-s', '--separator', default='\t',
            help="Separator to use. Default is '\t'.")

	args = parser.parse_args()

	main(args)