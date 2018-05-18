import urllib2



def checkupdate(iot_id, address, delete):
	address = "http://" + address + "/sqlreq?iot_id=" + iot_id
	if delete == True:
		address = address + "&delete=True"
	try: 
		source = urllib2.urlopen(address).read()
		if source == "[]":
			return None
		else:
			return source
	except:
		print "error Cannot Reach Server"
		return None


def parse_server(table_info):
	table_info = table_info.split()
	table_info = table_info[1]
	table_info = table_info[2:-3]
	if not table_info.count("@") == 0:
		table_info = table_info.split("@")
	else:
		table_info = [table_info]
	return table_info






if __name__ == '__main__':
	print(parse("[(4, u'aaaaa393djdjeedd')]"))