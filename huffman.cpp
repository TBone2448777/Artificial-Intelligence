#include <cstdio>
#include <algorithm>

// Holds leaf values, letter, value, and probablity
class Node{
    public:
        char letter;
        float probability;
        Node *left = NULL;
        Node *right = NULL;
        Node(char val = '\0', float chance = 0){
            letter = val;
            probability = chance;
        };
};

// Just used old bubble sort code. Not super efficient but least headache to implement
int bubbleSort(Node *arrPtr, size_t len){
    // Iterate through this len times
    for (size_t i=0; i < len; i++){
        // Go through all adjacent pairs of the array and swap if the left side is larger than the right
        int errCount = 0;
        for (size_t j=0; j < len-1; j++){
            if ((arrPtr + j)->probability < (arrPtr + j + 1)->probability){
                Node temp = *(arrPtr + j);
                *(arrPtr + j) = *(arrPtr + j + 1);
                *(arrPtr + j + 1) = temp;
                errCount++;
            }
        }
        if (errCount == 0){
            break;
        }
    }
    return 0;
}

void huffman(char *letters, float *numbers, int arrSize){
    Node allNodes[arrSize];
    for (size_t i = 0; i < arrSize; i++){
        allNodes[i] = Node(*(letters + i), *(numbers + i));
    }
    Node *allNodePtr = allNodes;
    for (size_t i = 0; i < arrSize; i++){
        bubbleSort(allNodePtr, arrSize);
        Node *newNode = new Node;
        newNode->left = &allNodes[-2];
        newNode->right = &allNodes[-1];
        newNode->probability = newNode->left->probability + newNode->right->probability;
        allNodes[-2] = *newNode;
        arrSize--;
        printf("\n");
        for (size_t i = 0; i < arrSize; i++){
            printf("%c", allNodes[i].letter);
            printf("%f", allNodes[i].probability);
            printf("\n");
        }
    }
}

int main(){
    // Two options for charsets below. Comment out the one not desired to be used
    // Entire alphabet
    // char letters[] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'};
    // float numbers[] = {8.2, 1.5, 2.8, 4.3, 12.7, 2.2, 2.0, 6.1, 7.0, 0.15, 0.77, 4.0, 2.4, 6.7, 7.5, 1.9, 0.095, 6.0, 6.3, 9.1, 2.8, 0.98, 2.4, 0.15, 2.0, 0.074};
    // Just the top eight letters like specified in the assignment
    char letters[] = {'E', 'T', 'A', 'O', 'I', 'N', 'S', 'H'};
    float numbers[] = {12.7, 9.1, 8.2, 7.5, 7.0, 6.7, 6.3, 6.1};
    char *lettPtr = letters;
    float *numPtr = numbers;
    int size = sizeof(letters)/sizeof(letters[0]);
    huffman(lettPtr, numPtr, size);
    printf("\n");
}