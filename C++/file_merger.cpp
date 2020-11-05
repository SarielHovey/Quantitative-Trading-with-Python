#include <iostream>
#include <fstream>
#include <string>
#include <dirent.h>
#include <sys/types.h>
#include <list>
using namespace std;


list<string> list_dir(const string& path) {
    /*
    Used to get filename for files like Sa_ddmmyyyy.csv in a specific directory.
    param-path: std::string, directory path for files
    return: std::list<string>
    */
    list<string> fileNames;
    struct dirent *entry;
    DIR *dir = opendir(path.c_str());
    
    if (dir == NULL) { cerr << "filePath not found!" << "\n"; }
    while ((entry = readdir(dir)) != NULL) {
        string temp = entry->d_name;
        if (temp.substr(0,2) == "Sa") {
            temp = path + temp;
            fileNames.push_back(temp);
        }
    }
    closedir(dir);
    return fileNames;
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


int main() {
    cout << "File merger V1.0 powered by C++ -- Sariel Huang" << endl;
    string ipt = "//sample.net/sample dir1/sample dir2/";
    cout << "Reading files in " << ipt << "\n";
    
    list<string> fileNames;
    fileNames = list_dir(ipt);
    merge_files(fileNames, "otpt.csv");
    cout << "\n" << "Files merged into optp.csv!" << "\n";
    system("pause");
}
