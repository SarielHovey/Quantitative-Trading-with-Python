#include <cstdlib>
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <dirent.h>
#include <sys/types.h>
#include <vector>
#include <iomanip>
#include <ctime>

using namespace std;

string ipt = "\\\\path\\";
string history = "\\\\pathpath\\";

string get_path() {
    /*
    Used to get absolute filePath for ~/Downloads/ from sys env parameters
    return: string, filePath for directory ~/Downloads/
    */
    string otpt;
    string envParam = "username";
    string user = getenv(envParam.c_str());
    otpt = "C:\\Users\\" + user + "\\Downloads\\";
    return otpt;
}


vector<string> list_dir(const string& path, const string& filter) {
    /*
    Used to get filename for files like MW_ddmmyyyy.csv in a specific directory.
    param-path: std::string, directory path for files
    param-filter: std::string, filter to match filename
    return: std::vector<string>
    */
    int i = filter.size();
    vector<string> fileNames;
    struct dirent *entry;
    DIR *dir = opendir(path.c_str());

    if (dir == NULL) { std::cerr << "filePath not found!" << "\n"; }
    while ((entry = readdir(dir)) != NULL) {
        string temp = entry->d_name;
        if (temp.substr(0,i) == filter) {
            temp = path + temp;
            //cout << temp << endl;
            fileNames.push_back(temp);
        }
    }
    closedir(dir);
    return fileNames;
}


string get_prev_wday() {
    /*
    Used to get date of last working day
    return: std::string, in form of %d%m%Y
    */
    char buffer[9];
    time_t now = time(0);
    time_t yesterday;
    //string today = ctime(&now);
    //cout << "Current DateTime: " << today << "\n";
    tm* ltm = localtime(&now);
    //cout << "Day: " << ltm->tm_mday << " Hour: " << ltm->tm_hour << endl;
    int currentWday = ltm->tm_wday;
    if (currentWday != 1) {
        yesterday = now - (24*60*60);
    }
    else {
        yesterday = now - (3*24*60*60);
    }
    tm* ltm_y = localtime(&yesterday);
    strftime(buffer, 9, "%d%m%Y", ltm_y);
    return (string) buffer;
}


void read_and_write(const string& in, fstream& outfile, const string& out) {
    /*
    Used to extract contents from infile to outfile.
    param-in: std::string, input file name
    param-outfile: fstream object, output file
    return: void
    */
    ifstream infile;
    infile.open(in.c_str(), ios::in);

    string data;

    //cout << "Reading from input..." << "\n";
    while ( getline(infile, data) ) {
    //cout << data << endl;
    outfile << data << endl;
    }
    infile.close();
}


void merge_files(vector<string>& inList, const string& outName) {
    /*
    Read contents from inList and merge the contents into an output file.
    param-inList: vector<string> object, contains file path for input files
    param-outName: filename of the output file, like otpt.csv
    */
    fstream outfile;
    outfile.open(outName.c_str(), ios::out | ios::trunc);
    int cnt=0;
    for (vector<string>::iterator it=inList.begin(); it != inList.end(); it++) {
        //clog << *it << endl;
        cnt++;
        cout << "\r" << "Processing file [" << cnt << "/" << inList.size() << "]";
        read_and_write(*it, outfile, outName);
    }
    outfile.close();
}


stringstream _analyze_data(const string& in, const string& des, const string& prev_wday) {
    /*
    Used to find MW IDs that should be mapped into ODW.
    */
    ifstream infile;
    fstream outfile;
    vector<string> row;
    string line, word;
    stringstream mw_id;
    
    infile.open(in.c_str(), ios::in);
    outfile.open("result.txt", ios::out | ios::trunc);
    while ( getline(infile, line) ) {
        
        row.clear();
        istringstream s(line);
        while ( getline(s, word, ',') ) {
            row.push_back(word);
        }
        
        // a typical mw report consists of 25 columns
        if (row.size()==25 && row[19]=="Error") {
            istringstream rsps_time(row[23]);
            istringstream p_wday(prev_wday + " 00:00:00");
            
            struct tm tm1, tm2;
            
            rsps_time >> std::get_time(&tm1, "%d/%m/%Y %H:%M:%S");
            time_t rsps = mktime(&tm1);
            p_wday >> std::get_time(&tm2, "%d%m%Y %H:%M:%S");
            time_t yest = mktime(&tm2);
            bool ttt = (rsps>=yest);            
            if (ttt && (row[15] == "A" || row[15] == "B" || row[15] == "C") ) {
                outfile << row[0] << ",";
                outfile << row[23] << "\n";
                mw_id << row[0] << ";";
            }
        }
        
    }

    infile.close(); 
    outfile.close();
    return mw_id;
}


void daily_process() {
    /*
    Perform daily process.
    */
    string download = get_path();
    cout << "Reading files in " << download << "\n";

    //cout << "Size of fileNames: " << fileNames.size() << "\n";
    //cout << *fileNames.begin() << "\n";
    string fname = "MW_" + get_prev_wday() + ".csv";
    string cmd;
    cmd = "rename " + download + "ReportingHistory.csv" + " " + fname;
    system(cmd.c_str());
    cmd = "copy " + download + fname + " " + "\"" + history + "\"";
    system(cmd.c_str());
    cmd = "copy " + download + fname + " " + "\"" + ipt + "\"";
    system(cmd.c_str());
    
    stringstream otpt;
    otpt = _analyze_data(download + fname, ipt, get_prev_wday());
    cout << otpt << "\n";
}


void adhoc_process(const string& date) {
    string fname = "MW_" + date + ".csv";
    stringstream otpt;
    otpt = _analyze_data(history + fname, ipt, date);
    cout << otpt << "\n";
}

int main() {
    cout << "Control V2.0 powered by C++ -- Sariel Huang" << endl;
    cout << "-------------------------------------------------" << endl;
    cout << "Please insert number: " << endl;
    cout << "1 for daily process; " << "2 for periodic control; ";
    cout << "3 for ad hoc control; ";
    cout << "0 for exit." << endl;
    unsigned int temp = 0;
    string temp1;

    process:while (1) {
        cin >> temp;
        if (cin.fail()) {
            cin.clear();
            cin.sync();
            goto process;
        }
        if ( temp == 1) {
            daily_process();
            goto endProcess;
        }
        else if ( temp == 2) {
            cout << "Reading files in " << history << "\n";
            vector<string> fileNames;
            fileNames = list_dir(history, "MW");
            merge_files(fileNames, "otpt.csv");
            cout << "\n" << "Files merged into otpt.csv!" << "\n";
            goto endProcess;
        }
        else if ( temp == 3) {
            cout << "Please input Datetime ddmmyyyy: ";
            cin >> temp1;
            adhoc_process(temp1);           
            goto endProcess;
        }
        else if ( temp == 0) {
            goto endProcess;
        }
        else {
            goto process;
        }
    }

    endProcess:
        system("pause");
        return 0;
}
