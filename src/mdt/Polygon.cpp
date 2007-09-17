#include "Polygon.h"

Polygon::Polygon() {
  num_points = 0;
  x = NULL;
  y = NULL;
}

void Polygon::createRiverEdgePolygon() {

  num_points = 8;
  x = new double[num_points];
  y = new double[num_points];

  int n = 0;
  x[n] = 594811.; y[n++] = 114864.;
  x[n] = 594636.; y[n++] = 115636.;
  x[n] = 594578.; y[n++] = 115817.;
  x[n] = 594413.; y[n++] = 116531.;
  x[n] = 594351.; y[n++] = 116922.;
  x[n] = 594317.; y[n++] = 117316.;
  x[n] = 592637.; y[n++] = 117114.;
  x[n] = 593288.; y[n++] = 114309.;


}

int Polygon::pointInPolygon(double x_, double y_) {

  int inside = 0;
  int j = 0;
  for (int i=0; i<num_points; i++) {
    if (++j == num_points) j = 0;
    if ((y[i] < y_ && y[j] >= y_) || (y[j] < y_ && y[i] >= y_)) {
      if (x[i] + (y_-y[i])/(y[j]-y[i])*(x[j]-x[i]) < x_)
        inside = !inside;
    }
  }
  return inside;
}

Polygon::~Polygon() {
  if (x) delete [] x;
  if (y) delete [] y;
}