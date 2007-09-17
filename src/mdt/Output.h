#ifndef OUTPUT_H_
#define OUTPUT_H_

#include<stdio.h>

#include "include/petsc.h"

#include "Grid.h"
#ifdef USE_HDF5
#include "HDF.h"
#endif

#define COLLECTIVE 1
#define INDEPENDENT 0

class Output {
public:
  Output(Grid *g);
  virtual ~Output();

  void printGMSGrid();
  void printGMSDataSet(char *filename, Vec v);
  void printBoundarySets();
  void writeIntVectorInNaturalOrder(FILE *fp, Vec v, int one_per_line);
  void printHDFMesh();

private:
  Grid *grid;

};

#endif /*OUTPUT_H_*/