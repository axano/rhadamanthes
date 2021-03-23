
#include "binarytree.h"
#include "ID3.h"

#include <cassert>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <list>
#include <map>

void readQuestions(const char *filename, std::vector<std::string> &questions, std::list<std::string> &emails, std::vector<std::map<std::string, bool>> &answers)
{
    int nemails, nQuestions;

    std::ifstream in(filename);
    if (in)
    {
        in >> nemails;
        in >> nQuestions;

        std::string temp;
        std::getline(in, temp);

        questions.resize(nQuestions);
        for (int i = 0; i < nQuestions; i++)
        {
            std::getline(in, questions[i]);
        }

        answers.resize(nQuestions);

        std::string animal;
        for (int i = 0; i < nemails; i++)
        {
            in >> animal;

            emails.push_front(animal);

            for (int j = 0; j < nQuestions; j++)
            {
                in >> temp;
                answers[j][animal] = temp == "y";
            }
        }
    }
    else
    {
        std::cout << "Could not open file" << std::endl;
    }
}

int main()
{
    std::vector<std::string> questions;
    std::list<std::string> emails;
    std::vector<std::map<std::string, bool>> answers;
    readQuestions("emails_test.txt", questions, emails, answers);

    std::cout << "Loaded " << questions.size() << " questions" << std::endl;
    //for (auto it = questions.begin(); it != questions.end(); it++){
    //    std::cout << *it <<std::endl;
    //}

    std::cout << "Loaded " << emails.size() << " emails" << std::endl;
    //for (auto it = emails.begin(); it != emails.end(); it++){
    //    std::cout << *it <<std::endl;
    //}

    ID3Tree tree;
    bool success = tree.build(questions, emails, answers);

    std::cout << (success ? "Successfully built tree" : "Not enough information to build a tree") << std::endl;

    if (true)
    {
        std::cout << tree << std::endl;
        std::cout << "The height of the tree is: " << tree.height() << std::endl;
        std::cout << "The tree has " << tree.numberOfLeaves() << " leaves" << std::endl;
        std::cout << "The average depth of a leaf is " << tree.averageDepth() << std::endl;
        std::cout << "The tree has " << tree.numberOfSplits() << " questions" << std::endl;
    }

    return 0;
}