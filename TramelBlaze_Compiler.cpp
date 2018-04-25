#include <cstdlib>
#include <unistd.h>
#include <iostream>
#include <string>
#include <fstream>
#include <streambuf>

using namespace std;

string readFile(void);
void writeFile(string source);

//https://www.cprogramming.com/tutorial/lesson18.html
//Alex Allain
struct node
{
	int key_value;
	node *left;
	node *right;
};
class btree
{
public:
	btree();
	~btree();

	void insert(int key);
	node *search(int key);
	void destroy_tree();

private:
	void destroy_tree(node *leaf);
	void insert(int key, node *leaf);
	node *search(int key, node *leaf);

	node *root;
};
btree::btree()
{
	root = NULL;
}
void btree::destroy_tree(node *leaf)
{
	if (leaf != NULL)
	{
		destroy_tree(leaf->left);
		destroy_tree(leaf->right);
		delete leaf;
	}
}
void btree::insert(int key, node *leaf)
{
	if (key< leaf->key_value)
	{
		if (leaf->left != NULL)
			insert(key, leaf->left);
		else
		{
			leaf->left = new node;
			leaf->left->key_value = key;
			leaf->left->left = NULL;    //Sets the left child of the child node to null
			leaf->left->right = NULL;   //Sets the right child of the child node to null
		}
	}
	else if (key >= leaf->key_value)
	{
		if (leaf->right != NULL)
			insert(key, leaf->right);
		else
		{
			leaf->right = new node;
			leaf->right->key_value = key;
			leaf->right->left = NULL;  //Sets the left child of the child node to null
			leaf->right->right = NULL; //Sets the right child of the child node to null
		}
	}
}
node *btree::search(int key, node *leaf)
{
	if (leaf != NULL)
	{
		if (key == leaf->key_value)
			return leaf;
		if (key<leaf->key_value)
			return search(key, leaf->left);
		else
			return search(key, leaf->right);
	}
	else return NULL;
}
void btree::insert(int key)
{
	if (root != NULL)
		insert(key, root);
	else
	{
		root = new node;
		root->key_value = key;
		root->left = NULL;
		root->right = NULL;
	}
node *btree::search(int key)
	{
		return search(key, root);
	}
void btree::destroy_tree()
{
	destroy_tree(root);
}

string readSourceText() {
	string source;
	ifstream txt("file.txt");

	if (!(txt.is_open())) {
		cout << "Unable to open file." << endl;
		return 0; //end program if file doesn't open
	}
	
	//allocate string variable size from file
	txt.seekg(0, ios::end);
	source.reserve(txt.tellg());
	txt.seekg(0, ios::beg);
	

	//read file into string variable
	source.assign((istreambuf_iterator<char>(txt)),
		istreambuf_iterator<char>());
	txt.close();
	return source;
}
void writeSourceText(string source) {
	ofstream text("file.txt");
	text << source;
	text.close();
}