from multiprocessing.dummy import Pool as ThreadPool
import csv


def scrape(array, function, threads):
        # Define the number of threads
        pool = ThreadPool(threads)

        # Tell the user what is happening
        print("Scraping %s items using %s on %s threads." % (len(array), function, threads))

        # Calls get() and adds the filesize returned each call to an array called filesizes
        result = pool.map(function, array)
        pool.close()
        pool.join()
        return result


# Handle an error where data is not added ta the end of the CSV file.
def addNewLine(file):
    # Add a newline to the end of the file if there is not one
    with open(file, "r+") as f:
        f.seek(0, 2)
        if(f.read() != '\n'):
            f.seek(0, 2)
            f.write('\n')


def tabulate(csvFile, array):
    # Files must be in the csv directory inside the project folder
    # Opens the CSV file
    with open("csv/%s.csv" % (csvFile), 'a', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        # Adds a new line if there is not one present
        addNewLine("csv/%s.csv" % (csvFile))
        # Add the array passed in to the CSV file
        for i in range(0, len(array)):
            writer.writerow(array[i])
        print("Succesfully tabulated %s rows to %s.csv." % (len(array), csvFile))
    return True


def getExistingData(csvFile, rowNum):
    # Add the values in rowNum in csvFile to an array
    array = []
    print("Reading data from %s.csv." % (csvFile))
    with open("csv/%s.csv" % (csvFile), encoding='utf-8') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            array.append(row[rowNum])
    return array


def removeExistingData(existing, new):
    # Remove data we alredy have from the list of new data to parse
    for i in new[:]:
        if i in existing:
            new.remove(i)
    # Convert new values to a set to remove dupelicates, then back to a list
    new = list(set(new))
    print("%s new items to add." % (len(new)))
    return new


def unDimension(array, item):
    # Pulls specific items from an multi-dimensional array and returns them to one array
    result = []
    for i in range(0, len(array)):
        result.append(array[i][item])
    return result


def fixArray(array, value):
    # Used to clean match info results for matches with more than one map
    for i in range(0, len(array)):
        if len(array[i]) < value:
            for b in range(0, len(array[i])):
                array.append(array[i][b])
            array.remove(array[i])
    return array