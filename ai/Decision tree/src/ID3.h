#ifndef ID3TREE
#define ID3TREE

#include <memory>
#include <vector>
#include <list>
#include <map>
#include <algorithm>
#include <iostream>

class ID3Node;

class ID3Tree : public std::unique_ptr<ID3Node>
{
public:
    using std::unique_ptr<ID3Node>::unique_ptr;
    using std::unique_ptr<ID3Node>::operator=;
    friend std::ostream &operator<<(std::ostream &os, const ID3Tree &tree);

    bool build(std::vector<std::string> &questions, std::list<std::string> &emails, std::vector<std::map<std::string, bool>> answers);
    int height();
    double averageDepth();
    int numberOfLeaves();
    int numberOfSplits();

private:
    bool build(
        std::vector<std::string> &questions,
        std::list<std::string> &emails,
        std::vector<std::map<std::string, bool>> &answers,
        std::vector<bool> usedQuestions);

    
    std::ostream& print(std::ostream& os, int level, const std::string &prefix) const;
    int internalPathLength();
};

class ID3Node
{
public:
    std::string value;
    ;
    ID3Tree left, right;
};

bool ID3Tree::build(std::vector<std::string> &questions, std::list<std::string> &emails, std::vector<std::map<std::string, bool>> answers)
{
    std::vector<bool> usedQuestions(questions.size(), false);
    return build(questions, emails, answers, usedQuestions);
}

bool ID3Tree::build(std::vector<std::string> &questions, std::list<std::string> &emails, std::vector<std::map<std::string, bool>> &answers, std::vector<bool> usedQuestions)
{
    if (emails.size() == 1)
    {
        // We are done, only one remaining animal, add a leaf
        *this = std::make_unique<ID3Node>();
        (*this)->value = *emails.begin();
        return true; // This branch is successful
    }

    // Look for the question that best splits the remaining emails
    int selectedQuestion = -1;
    int selectedQuestionScore = -1;

    for (unsigned int i = 0; i < questions.size(); i++)
    {
        if (!usedQuestions[i])
        {
            int countYes = 0;
            int countNo = 0;
            for (auto it = emails.begin(); it != emails.end(); it++)
            {
                if (answers[i][*it])
                {
                    countYes++;
                }
                else
                {
                    countNo++;
                }
            }
            int score = std::abs(countYes - countNo);
            if (selectedQuestionScore < 0 || score < selectedQuestionScore)
            {
                selectedQuestionScore = score;
                selectedQuestion = i;
            }
        }
    }
   

    if (selectedQuestion > -1)
    {
        // We found a question
        usedQuestions[selectedQuestion] = true;

        *this = std::make_unique<ID3Node>();

        (*this)->value = questions[selectedQuestion];

        std::list<std::string> emailsLeft;
        std::list<std::string> emailsRight;

        std::list<std::string>::iterator it = emails.begin();
        while (it != emails.end())
        {
            std::list<std::string>::iterator other = it;
            it++;
            if (answers[selectedQuestion][*other])
            {
                emailsLeft.splice(emailsLeft.begin(), emails, other);
            }
            else
            {
                emailsRight.splice(emailsRight.begin(), emails, other);
            }
        }



        if (emailsLeft.size() == 0 || emailsRight.size() == 0)
        {
            // One of the subtrees is empty, this was a useless question
            return build(questions, (emailsLeft.size() == 0 ? emailsRight : emailsLeft), answers, usedQuestions);
        }
        else
        {
            // Build the left and right tree recursively
            bool result = true;
            if (emailsLeft.size() > 0)
            {
                result = (*this)->left.build(questions, emailsLeft, answers, usedQuestions);
            }
            if (emailsRight.size() > 0)
            {
                result &= (*this)->right.build(questions, emailsRight, answers, usedQuestions);
            }

            return result;
        }
    }
    else
    {
        return false;
    }
}

int ID3Tree::height()
{
    if (!*this)
    {
        return 0;
    }
    return std::max((*this)->left.height(), (*this)->right.height()) + 1;
}

double ID3Tree::averageDepth()
{
    return (double)internalPathLength() / numberOfLeaves();
}

int ID3Tree::numberOfLeaves()
{
    if (!((*this)->left) && !((*this)->right))
    {
        return 1;
    }
    else
    {
        int sum = 0;
        if ((*this)->left)
        {
            sum += (*this)->left.numberOfLeaves();
        }
        if ((*this)->right)
        {
            sum += (*this)->right.numberOfLeaves();
        }
        return sum;
    }
}

int ID3Tree::internalPathLength()
{
    if (!*this)
    {
        return 0;
    }
    int sum = 0;
    if ((*this)->left)
    {
        sum += (*this)->left.numberOfLeaves() + (*this)->left.internalPathLength();
    }
    if ((*this)->right)
    {
        sum += (*this)->right.numberOfLeaves() + (*this)->right.internalPathLength();
    }
    return sum;
}

int ID3Tree::numberOfSplits()
{
    if (!((*this)->left) && !((*this)->right))
    {
        // this is a leave
        return 0;
    }
    // this is a split point
    int sum = 1;
    if ((*this)->left)
    {
        sum += (*this)->left.numberOfSplits();
    }
    if ((*this)->right)
    {
        sum += (*this)->right.numberOfSplits();
    }
    return sum;
}

std::ostream &operator<<(std::ostream &os, const ID3Tree &tree)
{
    os << tree->value << std::endl;
    if (tree->left)
    {
        tree->left.print(os, 0, "Y");
    }
    if (tree->right)
    {
        tree->right.print(os, 0, "N");
    }
    return os;
}

std::ostream &ID3Tree::print(std::ostream &os, int level, const std::string &prefix) const
{
    os << std::string(level, '\t') << "--" << prefix << "--> " << (*this)->value << std::endl;
    level++;
    if ((*this)->left)
    {
        (*this)->left.print(os, level, "Y");
    }
    if ((*this)->right)
    {
        (*this)->right.print(os, level, "N");
    }
    return os;
}

#endif