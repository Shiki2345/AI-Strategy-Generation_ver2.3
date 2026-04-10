#include <iostream>
#include <memory>

enum class Color {
    RED,
    BLACK
};

template<typename T>
class RedBlackTree {
private:
    struct Node {
        T data;
        Color color;
        Node* left;
        Node* right;
        Node* parent;

        Node(const T& value) 
            : data(value), color(Color::RED), left(nullptr), right(nullptr), parent(nullptr) {}
    };

    Node* root;
    Node* nil;  // 哨兵节点，代表所有的叶子节点

    // 左旋转
    void leftRotate(Node* x) {
        Node* y = x->right;
        x->right = y->left;
        
        if (y->left != nil) {
            y->left->parent = x;
        }
        
        y->parent = x->parent;
        
        if (x->parent == nil) {
            root = y;
        } else if (x == x->parent->left) {
            x->parent->left = y;
        } else {
            x->parent->right = y;
        }
        
        y->left = x;
        x->parent = y;
    }

    // 右旋转
    void rightRotate(Node* y) {
        Node* x = y->left;
        y->left = x->right;
        
        if (x->right != nil) {
            x->right->parent = y;
        }
        
        x->parent = y->parent;
        
        if (y->parent == nil) {
            root = x;
        } else if (y == y->parent->left) {
            y->parent->left = x;
        } else {
            y->parent->right = x;
        }
        
        x->right = y;
        y->parent = x;
    }

    // 插入后修复红黑树性质
    void insertFixup(Node* z) {
        while (z->parent->color == Color::RED) {
            if (z->parent == z->parent->parent->left) {
                Node* y = z->parent->parent->right;  // 叔叔节点
                
                if (y->color == Color::RED) {
                    // 情况1：叔叔节点是红色
                    z->parent->color = Color::BLACK;
                    y->color = Color::BLACK;
                    z->parent->parent->color = Color::RED;
                    z = z->parent->parent;
                } else {
                    if (z == z->parent->right) {
                        // 情况2：叔叔是黑色，且z是右孩子
                        z = z->parent;
                        leftRotate(z);
                    }
                    // 情况3：叔叔是黑色，且z是左孩子
                    z->parent->color = Color::BLACK;
                    z->parent->parent->color = Color::RED;
                    rightRotate(z->parent->parent);
                }
            } else {
                Node* y = z->parent->parent->left;  // 叔叔节点
                
                if (y->color == Color::RED) {
                    // 情况1：叔叔节点是红色
                    z->parent->color = Color::BLACK;
                    y->color = Color::BLACK;
                    z->parent->parent->color = Color::RED;
                    z = z->parent->parent;
                } else {
                    if (z == z->parent->left) {
                        // 情况2：叔叔是黑色，且z是左孩子
                        z = z->parent;
                        rightRotate(z);
                    }
                    // 情况3：叔叔是黑色，且z是右孩子
                    z->parent->color = Color::BLACK;
                    z->parent->parent->color = Color::RED;
                    leftRotate(z->parent->parent);
                }
            }
        }
        root->color = Color::BLACK;
    }

    // 替换子树
    void transplant(Node* u, Node* v) {
        if (u->parent == nil) {
            root = v;
        } else if (u == u->parent->left) {
            u->parent->left = v;
        } else {
            u->parent->right = v;
        }
        v->parent = u->parent;
    }

    // 查找最小节点
    Node* minimum(Node* node) {
        while (node->left != nil) {
            node = node->left;
        }
        return node;
    }

    // 删除后修复红黑树性质
    void deleteFixup(Node* x) {
        while (x != root && x->color == Color::BLACK) {
            if (x == x->parent->left) {
                Node* w = x->parent->right;  // 兄弟节点
                
                if (w->color == Color::RED) {
                    // 情况1：兄弟节点是红色
                    w->color = Color::BLACK;
                    x->parent->color = Color::RED;
                    leftRotate(x->parent);
                    w = x->parent->right;
                }
                
                if (w->left->color == Color::BLACK && w->right->color == Color::BLACK) {
                    // 情况2：兄弟节点是黑色，且两个孩子都是黑色
                    w->color = Color::RED;
                    x = x->parent;
                } else {
                    if (w->right->color == Color::BLACK) {
                        // 情况3：兄弟节点是黑色，左孩子是红色，右孩子是黑色
                        w->left->color = Color::BLACK;
                        w->color = Color::RED;
                        rightRotate(w);
                        w = x->parent->right;
                    }
                    // 情况4：兄弟节点是黑色，右孩子是红色
                    w->color = x->parent->color;
                    x->parent->color = Color::BLACK;
                    w->right->color = Color::BLACK;
                    leftRotate(x->parent);
                    x = root;
                }
            } else {
                Node* w = x->parent->left;  // 兄弟节点
                
                if (w->color == Color::RED) {
                    // 情况1：兄弟节点是红色
                    w->color = Color::BLACK;
                    x->parent->color = Color::RED;
                    rightRotate(x->parent);
                    w = x->parent->left;
                }
                
                if (w->right->color == Color::BLACK && w->left->color == Color::BLACK) {
                    // 情况2：兄弟节点是黑色，且两个孩子都是黑色
                    w->color = Color::RED;
                    x = x->parent;
                } else {
                    if (w->left->color == Color::BLACK) {
                        // 情况3：兄弟节点是黑色，右孩子是红色，左孩子是黑色
                        w->right->color = Color::BLACK;
                        w->color = Color::RED;
                        leftRotate(w);
                        w = x->parent->left;
                    }
                    // 情况4：兄弟节点是黑色，左孩子是红色
                    w->color = x->parent->color;
                    x->parent->color = Color::BLACK;
                    w->left->color = Color::BLACK;
                    rightRotate(x->parent);
                    x = root;
                }
            }
        }
        x->color = Color::BLACK;
    }

    // 中序遍历辅助函数
    void inorderHelper(Node* node) const {
        if (node != nil) {
            inorderHelper(node->left);
            std::cout << node->data << "(" 
                      << (node->color == Color::RED ? "R" : "B") << ") ";
            inorderHelper(node->right);
        }
    }

    // 销毁树的辅助函数
    void destroyTree(Node* node) {
        if (node != nil) {
            destroyTree(node->left);
            destroyTree(node->right);
            delete node;
        }
    }

    // 查找节点
    Node* searchHelper(Node* node, const T& value) const {
        if (node == nil || value == node->data) {
            return node;
        }
        
        if (value < node->data) {
            return searchHelper(node->left, value);
        } else {
            return searchHelper(node->right, value);
        }
    }

public:
    RedBlackTree() {
        nil = new Node(T());
        nil->color = Color::BLACK;
        nil->left = nil->right = nil->parent = nil;
        root = nil;
    }

    ~RedBlackTree() {
        destroyTree(root);
        delete nil;
    }

    // 插入节点
    void insert(const T& value) {
        Node* z = new Node(value);
        z->left = nil;
        z->right = nil;
        
        Node* y = nil;
        Node* x = root;
        
        while (x != nil) {
            y = x;
            if (z->data < x->data) {
                x = x->left;
            } else {
                x = x->right;
            }
        }
        
        z->parent = y;
        
        if (y == nil) {
            root = z;
        } else if (z->data < y->data) {
            y->left = z;
        } else {
            y->right = z;
        }
        
        z->color = Color::RED;
        insertFixup(z);
    }

    // 删除节点
    void remove(const T& value) {
        Node* z = searchHelper(root, value);
        
        if (z == nil) {
            std::cout << "值 " << value << " 不存在于树中" << std::endl;
            return;
        }
        
        Node* y = z;
        Node* x;
        Color yOriginalColor = y->color;
        
        if (z->left == nil) {
            x = z->right;
            transplant(z, z->right);
        } else if (z->right == nil) {
            x = z->left;
            transplant(z, z->left);
        } else {
            y = minimum(z->right);
            yOriginalColor = y->color;
            x = y->right;
            
            if (y->parent == z) {
                x->parent = y;
            } else {
                transplant(y, y->right);
                y->right = z->right;
                y->right->parent = y;
            }
            
            transplant(z, y);
            y->left = z->left;
            y->left->parent = y;
            y->color = z->color;
        }
        
        delete z;
        
        if (yOriginalColor == Color::BLACK) {
            deleteFixup(x);
        }
    }

    // 查找节点
    bool search(const T& value) const {
        return searchHelper(root, value) != nil;
    }

    // 中序遍历
    void inorder() const {
        std::cout << "中序遍历: ";
        inorderHelper(root);
        std::cout << std::endl;
    }

    // 检查树是否为空
    bool isEmpty() const {
        return root == nil;
    }
};

// 测试程序
int main() {
    RedBlackTree<int> rbt;

    std::cout << "=== 红黑树测试程序 ===" << std::endl << std::endl;

    // 插入节点
    std::cout << "插入节点: 7, 3, 18, 10, 22, 8, 11, 26, 2, 6, 13" << std::endl;
    rbt.insert(7);
    rbt.insert(3);
    rbt.insert(18);
    rbt.insert(10);
    rbt.insert(22);
    rbt.insert(8);
    rbt.insert(11);
    rbt.insert(26);
    rbt.insert(2);
    rbt.insert(6);
    rbt.insert(13);

    rbt.inorder();
    std::cout << std::endl;

    // 查找节点
    std::cout << "查找 10: " << (rbt.search(10) ? "找到" : "未找到") << std::endl;
    std::cout << "查找 15: " << (rbt.search(15) ? "找到" : "未找到") << std::endl;
    std::cout << std::endl;

    // 删除节点
    std::cout << "删除节点 18" << std::endl;
    rbt.remove(18);
    rbt.inorder();
    std::cout << std::endl;

    std::cout << "删除节点 11" << std::endl;
    rbt.remove(11);
    rbt.inorder();
    std::cout << std::endl;

    std::cout << "删除节点 3" << std::endl;
    rbt.remove(3);
    rbt.inorder();
    std::cout << std::endl;

    // 尝试删除不存在的节点
    std::cout << "尝试删除不存在的节点 100" << std::endl;
    rbt.remove(100);
    std::cout << std::endl;

    return 0;
}
