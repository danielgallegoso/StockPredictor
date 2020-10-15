import csv
import sys
import numpy



def aggregate_articles(reader):
	agg = {}
	for row in reader:
		if int(row[4]) < 5000:
			if agg.get(row[0]) is None:
				agg[row[0]] = {}
				agg[row[0]]["price_change"] = row[7]
				agg[row[0]]["positive_words"] = [int(row[1])]
				agg[row[0]]["negative_words"] = [int(row[2])]
				agg[row[0]]["company_mentioned"] = [int(row[3])]
				agg[row[0]]["total_words"] = [int(row[4])]
				agg[row[0]]["pos_neighbors"] = [int(row[5])]
				agg[row[0]]["neg_neighbors"] = [int(row[6])]
			else:
				agg[row[0]]["positive_words"].append(int(row[1]))
				agg[row[0]]["negative_words"].append(int(row[2]))
				agg[row[0]]["company_mentioned"].append(int(row[3]))
				agg[row[0]]["total_words"].append(int(row[4]))
				agg[row[0]]["pos_neighbors"].append(int(row[5]))
				agg[row[0]]["neg_neighbors"].append(int(row[6]))
	return agg




def main(argv):
	companies = ['aapl', 'msft', 'amzn', 'tsla']
	for company in companies:
		csvfile = open(company + '/sentiment.csv', 'rU')
		reader = csv.reader(csvfile, delimiter = ',', dialect=csv.excel_tab)
		next(reader, None)
		agg = aggregate_articles(reader)
		csvfile.close()
		csvfile = open(company + '/aggregated.csv', 'wb')
		writer = csv.writer(csvfile, delimiter = ',')
		writer.writerow(['date','price_change', 'pos', 'neg', 'name_mentioned', 'total','pos_neighbors', 'neg_neighbors'])
		for date in agg.keys():
			row = []
			row.append(date)
			row.append(agg[date]["price_change"])
			row.append(sum(agg[date]["positive_words"]))
			row.append(sum(agg[date]["negative_words"]))
			row.append(sum(agg[date]["company_mentioned"]))
			row.append(sum(agg[date]["total_words"]))
			row.append(sum(agg[date]["pos_neighbors"]))
			row.append(sum(agg[date]["neg_neighbors"]))
			writer.writerow(row)
		csvfile.close()






if __name__ == "__main__":
    main(sys.argv)