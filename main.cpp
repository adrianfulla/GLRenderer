#include <iostream>
#include <cstdio>
#include <fstream>

using namespace std;



byte color (int r,int g,int b) {
    int color[3];
    color[0] = (r * 256);
    color[1] = (g * 256);
    color[2] = (b * 256);


    return static_cast<byte>(sizeof(color));
}

class Renderer {
    public:
        int width, height;
        byte clearColor;
        byte currColor;
        byte pixels[][];

        Renderer(int x, int y) {
            this->width = x;
            this->height = y;



            this->clearColor = color(0,0,0);
            this->currColor = color(1,1,1);
            byte s[width][height];

            for (int i = 0; i < this->width; i++) {
                for (int j = 0; j < this->height; ++j) {
                    s[i][j] = clearColor;
                }
            }
            this->pixels = s;
        }

        /*int glFinish(const string& filename) {
            ofstream file(filename);

            file << char('B');
            file << char('M');
            file << long (long (14+40+(this->width * this->height * 3)));
            file << long (long (0));
            file << long (long (14+40));

            file << long (long (40));
            file << long (long (this->width));
            file << long (long (this->height));
            file << int (1);
            file << int (24);
            file << long (long (0));
            file << long (long (this->width * this->height * 3));
            file << long (long (0));
            file << long (long (0));
            file << long (long (0));
            file << long (long (0));

            for (int i = 0; i < this->width; ++i) {
                for (int j = 0; j < this->height; ++j) {

                }
            }

            return 0;
        }*/


};

int main() {
    printf("Hello World \n");
    Renderer rend(1080,1080);
    printf(reinterpret_cast<const char *>(rend.pixels));

    printf("salida");

    return 0;
}
