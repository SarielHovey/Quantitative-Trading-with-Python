#include <cstdlib>
#include <iostream>
#include <fstream>
#include <string>
#include <dirent.h>
#include <sys/types.h>
#include <list>
#include <ctime>
using namespace std;


string ipt = "//sample/dir1/dir2/";
string history = "//sample.com/dir1/dir2/test space/";

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


list<string> list_dir(const string& path, const string& filter) {
    /*
    Used to get filename for files like Sa_ddmmyyyy.csv in a specific directory.
    param-path: std::string, directory path for files
    param-filter: std::string, filter to match filename
    return: std::list<string>
    */
    int i = filter.size();
    list<string> fileNames;
    struct dirent *entry;
    DIR *dir = opendir(path.c_str());

    if (dir == NULL) { cerr << "filePath not found!" << "\n"; }
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


void merge_files(list<string>& inList, const string& outName) {
    /*
    Read contents from inList and merge the contents into an output file.
    param-inList: list<string> object, contains file path for input files
    param-outName: filename of the output file, like otpt.csv
    */
    fstream outfile;
    outfile.open(outName.c_str(), ios::out | ios::trunc);
    int cnt=0;
    for (list<string>::iterator it=inList.begin(); it != inList.end(); it++) {
        //clog << *it << endl;
        cnt++;
        cout << "\r" << "Processing file [" << cnt << "/" << inList.size() << "]";
        read_and_write(*it, outfile, outName);
    }
    outfile.close();
}


void analyze_data(const string& in) {
    /*
    Used to count lines of record for different filters,
    result will be written into result.txt.
    param-in: string, path for input file
    */
    ifstream infile;
    fstream outfile;
    string data;
    infile.open(in.c_str(), ios::in);
    outfile.open("result.txt", ios::out | ios::trunc);
    unsigned int total=0, f1=0, f2=0, f3=0, f4=0, f5=0;
    while ( getline(infile, data) ) {
        if (data.find("F1") != std::string::npos) {
            total += 1;
            f1 += 1;
        }
        else if (data.find("F2") != std::string::npos) {
            total += 1;
            f1 += 1;
        }
        else if (data.find("F3") != std::string::npos) {
            total += 1;
            f2 += 1;
        }
        else if (data.find("F4") != std::string::npos) {
            total +=1;
            f3 +=1;
        }
        else if (data.find("F5") != std::string::npos) {
            total +=1;
            f4 +=1;
        }
        else if (data.find("F6") != std::string::npos) {
            total +=1;
            f5 +=1;
        }
        else {
            continue;
        }
    }
    infile.close();

    outfile << "Test V1.0" << "\n";
    outfile << "-------------------------------------------------" << "\n";
    outfile << "Total lines of record: " << total << endl;
    outfile << "-->F1: " << f1 << endl;
    outfile << "-->F2: " << f2 << endl;
    outfile << "-->F3: " << f3 << endl;
    outfile << "-->F4: " << f4 << endl;
    outfile << "-->F5: " << f5 << endl;
    outfile << "-------------------------------------------------" << endl;
    outfile.close();
}


void daily_process() {
    /*
    Perform daily process.
    */
    string download = get_path();
    cout << "Reading files in " << download << "\n";

    //cout << "Size of fileNames: " << fileNames.size() << "\n";
    //cout << *fileNames.begin() << "\n";
    string fname = "Sa_" + get_prev_wday() + ".csv";
    string cmd;
    cmd = "rename " + download + "SampleSample.csv" + " " + fname;
    system(cmd.c_str());
    cmd = "copy " + download + fname + " " + "\"" + history + "\"";
    system(cmd.c_str());
    cmd = "copy " + download + fname + " " + "\"" + ipt + "\"";
    system(cmd.c_str());
    analyze_data(download + fname);
    system("dir \\\\sample\\dir1\\dir2 >> result.txt");
}


int main() {
    cout << "Test V1.0" << endl;
    cout << "-------------------------------------------------" << endl;
    cout << "Please insert number: " << endl;
    cout << "1 for daily process; " << "2 for periodic control; " << "\n";
    cout << "0 for exit." << endl;
    unsigned int temp = 0;

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
            list<string> fileNames;
            fileNames = list_dir(history, "Sa");
            merge_files(fileNames, "otpt.csv");
            cout << "\n" << "Files merged into otpt.csv!" << "\n";
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
