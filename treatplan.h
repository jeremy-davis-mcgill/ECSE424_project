#ifndef TREATPLAN_H
#define TREATPLAN_H
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <stdlib.h>
#include <stdio.h>
using namespace std;


// Added by Yenvi
const int MAXCOUNT=1000;
const int MAXPOSITION=6;


void split(const std::string& string_in,
          char delim,
          std::vector<std::string>& tokens_out)
{
    std::istringstream iss(string_in);
    std::string token;

    while (std::getline(iss, token, delim)) {
        tokens_out.push_back(token);
    }
}
int TransformToTable(string treatmentPlan, double weight[MAXCOUNT], double dwell_positions[MAXCOUNT][MAXPOSITION], int shield_angle[MAXCOUNT],
                    int catheter_number[MAXCOUNT],double relative_position[MAXCOUNT]) {


    std::vector<std::string> vector_out;

    std::ifstream file(treatmentPlan);
    std::string line;
    std::getline(file, line);
    std::getline(file, line);

    split(line, ' ', vector_out);
    int Control_Points = std::stoi (vector_out.at(0),nullptr,0);



    for (int i=0;i<Control_Points;i++){
        std::getline(file, line);
        std::getline(file, line);
        vector_out.clear();
        split(line, ' ', vector_out);
        weight[i] = std::stod (vector_out.at(2));
        std::getline(file, line);
        std::getline(file, line);
        vector_out.clear();
        split(line, ',', vector_out);
        dwell_positions[i][0]= std::stod (vector_out.at(0));
        dwell_positions[i][1]= std::stod (vector_out.at(1));
        dwell_positions[i][2]= std::stod (vector_out.at(2));
        dwell_positions[i][3]= std::stod (vector_out.at(3));
        dwell_positions[i][4]= std::stod (vector_out.at(4));
        dwell_positions[i][5]= std::stod (vector_out.at(5));

        std::getline(file, line);
        vector_out.clear();
        split(line, ',', vector_out);
        shield_angle[i] = std::stoi (vector_out.at(0),nullptr,0);

        std::getline(file, line);
        vector_out.clear();
        split(line, ',', vector_out);
        catheter_number[i] = std::stoi (vector_out.at(0),nullptr,0);

        std::getline(file, line);
        vector_out.clear();
        split(line, ',', vector_out);
        relative_position[i] = std::stod (vector_out.at(0));

    }


    return Control_Points;
}

void WriteWeightShield(int Control_Points, double weight[MAXCOUNT], int shield_angle[MAXCOUNT]) {

    ofstream myfile;
    myfile.open ("weight_shield_angle.txt");
    myfile << Control_Points;
    myfile << "\n";
    for (int i=0;i<Control_Points;i++){
        myfile << weight[i];
        myfile << " ";
        myfile << shield_angle[i];
        myfile << "\n";
    }

    myfile.close();
}

#endif // TREATPLAN_H
