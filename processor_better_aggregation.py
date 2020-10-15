import csv
import sys

def get_future_date(date, num_days):
	day = int(date[-2:])
	month = int(date[5:7])
	year = int(date[:4])
	if month is 11 and day + num_days > 13:
		return None
	if day + num_days > 31:
		return str(year) + '-' + str(month+1) + '-0' + str(day+num_days-31)
	if day+num_days < 10:
		day = '0'+str(day+num_days)
	else:
		day = str(day+num_days)
	return str(year) + '-' + str(month) + '-' + day



def aggregate_the_aggregate(reader):
	agg = {}
	for row in reader:
		days = [row[0], get_future_date(row[0],1)]
		for i in xrange(0,len(days)):
			day = days[i]
			if day != None:
				if agg.get(day) is None:
					agg[day] = {}
				if i is 0:
					agg[day]['price_change'] = float(row[1])
				agg[day]['pos'+str(i)] = int(row[2])
				agg[day]['neg'+str(i)] = int(row[3])
				agg[day]['name_mentioned'+str(i)] = int(row[4])
				agg[day]['total'+str(i)] = int(row[5])
				agg[day]['pos_neighbors'+str(i)] = int(row[6])
				agg[day]['neg_neighbors'+str(i)] = int(row[7])
	return agg




def main(argv):
	companies = ['aapl', 'msft', 'amzn', 'tsla']
	for company in companies:
		csvfile = open(company + '/aggregated.csv', 'rU')
		reader = csv.reader(csvfile, delimiter = ',', dialect=csv.excel_tab)
		next(reader, None)
		agg = aggregate_the_aggregate(reader)
		csvfile.close()
		csvfile = open(company + '/better1.csv', 'wb')
		writer = csv.writer(csvfile, delimiter = ',')
		header = agg['2015-10-23'].keys()
		writer.writerow(['date']+header)
		for date in agg.keys():
			if agg[date].get("price_change") is None:
				continue
			row = []
			row.append(date)
			flag = False
			for i in xrange(0,len(header)):
				if agg[date].get(header[i]) is None:
					flag = True
				else:
					row.append(agg[date][header[i]])
			if flag is True:
				continue
			writer.writerow(row)
		csvfile.close()






if __name__ == "__main__":
    main(sys.argv)