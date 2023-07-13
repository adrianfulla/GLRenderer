#include <iostream>
#include <cstdio>
#include <vector>
#include <fstream>

using namespace std;



struct Color {
    unsigned char r;
    unsigned char g;
    unsigned char b;

    Color(int red, int green, int blue) {
        this->r = red;
        this->g = green;
        this->b = blue;
    }
};



struct Vect2 {
    int x;
    int y;
};

class Renderer {
    public:
        int width, height;
        Color clearColor = Color(0,0,0);
        Color currColor = Color('1','1','1');
        vector<vector<Color>> pixels;

        Renderer(int x, int y) {
            this->width = x;
            this->height = y;

            glClearColor(0,0,0);
            glClear();
            glColor(1,1,1);
        }

        void glClearColor(float r, float g, float b) {
            clearColor.r = static_cast<unsigned char>(b * 255);
            clearColor.g = static_cast<unsigned char>(g * 255);
            clearColor.b = static_cast<unsigned char>(r * 255);
        }

        void glColor(float r, float g, float b) {
            currColor.r = static_cast<unsigned char>(b * 255);
            currColor.g = static_cast<unsigned char>(g * 255);
            currColor.b = static_cast<unsigned char>(r * 255);
        }

        void glClear() {
            pixels.clear();
            for (int x = 0; x < width; x++) {
                vector<Color> column;
                for (int y = 0; y < height; y++) {
                    column.push_back(clearColor);
                }
                pixels.push_back(column);
            }
        }
        void glPoint(int x, int y, Color clr = Color('1','1','1')) {
            if (0 <= x && x < width && 0 <= y && y < height) {
                pixels[x][y] = clr;
            }
        }
    void glLine(Vect2 v0, Vect2 v1, Color clr = Color(1,1,1)) {
        int x0 = int(v0.x);
        int x1 = int(v1.x);
        int y0 = int(v0.y);
        int y1 = int(v1.y);
        if (x0 == x1 && y1 == y0) {
            glPoint(x0, y0);
            return;
        }
        int dx = abs(x1 - x0);
        int dy = abs(y1 - y0);
        bool steep = dy > dx;
        if (steep) {
            std::swap(x0, y0);
            std::swap(x1, y1);
        }
        if (x0 > x1) {
            std::swap(x0, x1);
            std::swap(y0, y1);
        }
    }


    void glFinish(const string& filename) {

        ofstream file(filename, ios::binary);

        file.write("B", 1);
        file.write("M", 1);
        file.write(reinterpret_cast<const char*>((14 + 40 + (this->width * this->height * 3))), sizeof(int));

        file.write(reinterpret_cast<const char*>(0), sizeof(int));
        file.write(reinterpret_cast<const char*>((14 + 40)), sizeof(int));

        file.write(reinterpret_cast<const char*>(40), sizeof(int));
        file.write(reinterpret_cast<const char*>((this->width)), sizeof(int));
        file.write(reinterpret_cast<const char*>((this->height)), sizeof(int));
        file.write(reinterpret_cast<const char*>(1), sizeof(short));
        file.write(reinterpret_cast<const char*>(24), sizeof(short));
        file.write(reinterpret_cast<const char*>(0), sizeof(int));
        file.write(reinterpret_cast<const char*>((this->width * this->height * 3)), sizeof(int));
        file.write(reinterpret_cast<const char*>(0), sizeof(int));
        file.write(reinterpret_cast<const char*>(0), sizeof(int));
        file.write(reinterpret_cast<const char*>(0), sizeof(int));
        file.write(reinterpret_cast<const char*>(0), sizeof(int));

        for (int y = 0; y < this->height; y++) {
            for (int x = 0; x < this->width; x++) {
                file.write(reinterpret_cast<const char*>(&(this->pixels[x][y])), sizeof(char));
            }
        }
    }


};

int main() {
    printf("Hello World \n");
    Renderer rend(1080,1080);

    rend.glPoint(250,250);
    rend.glFinish("output.bmp");

    printf("salida");

    return 0;
};